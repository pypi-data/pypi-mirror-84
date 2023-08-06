#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2013-2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Package for accessing the Satellite Situation Center (SSC) web services
https://sscweb.gsfc.nasa.gov/WebServices/REST/.
"""

#import os
import platform
import xml.etree.ElementTree as ET
import logging
from typing import Dict, List, Tuple, Union
import requests
import dateutil.parser

from sscws import __version__
from sscws.coordinates import CoordinateSystem, CoordinateComponent
from sscws.outputoptions import CoordinateOptions, OutputOptions
from sscws.regions import FootpointRegion, Hemisphere, SpaceRegion
from sscws.request import DataRequest, SatelliteSpecification
from sscws.timeinterval import TimeInterval



class SscWs:
    """
    Class representing the web service interface to NASA's
    Satelite Situation Center (SSC) <https://sscweb.gsfc.nasa.gov/>.

    Notes
    -----
    The logger used by this class has the class' name (SscWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.

    This class is dependent upon xml.etree.ElementTree which is
    vulnerable to an "exponential entity expansion" and "quadratic blowup
    entity expansion" XML attack.  However, this class only receives XML
    from the (trusted) SSC server so these attacks are not a threat.  See
    the xml.etree.ElementTree "XML vulnerabilities" documentation for
    more details.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            endpoint=None,
            timeout=None,
            proxy=None,
            ca_certs=None,
            disable_ssl_certificate_validation=False):
        """
        Creates an object representing the SSC web services.

        Parameters
        ----------
        endpoint
            URL of the SSC web service.  If None, the default is
            'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'.
        timeout
            Number of seconds to wait for a response from the server.
        proxy
            HTTP proxy information.  For example,
            proxies = {
              'http': 'http://10.10.1.10:3128',
              'https': 'http://10.10.1.10:1080',
            }
            Proxy information can also be set with environment variables.
            For example,
            $ export HTTP_PROXY="http://10.10.1.10:3128"
            $ export HTTPS_PROXY="http://10.10.1.10:1080"
        ca_certs
            Path to certificate authority (CA) certificates that will
            override the default bundle.
        disable_ssl_certificate_validation
            Flag indicating whether to validate the SSL certificate.
        """

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(logging.NullHandler())

        self.retry_after_time = None

        self.logger.debug('endpoint = %s', endpoint)
        self.logger.debug('ca_certs = %s', ca_certs)
        self.logger.debug('disable_ssl_certificate_validation = %s',
                          disable_ssl_certificate_validation)

        if endpoint is None:
            self._endpoint = 'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'
        else:
            self._endpoint = endpoint
        self._user_agent = 'sscws/' + __version__ + ' (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; '+ platform.platform() + ')'
        self._request_headers = {
            'Content-Type' : 'application/xml',
            'Accept' : 'application/xml',
            'User-Agent' : self._user_agent
        }
        self._session = requests.Session()
        self._session.headers.update(self._request_headers)

        if ca_certs is not None:
            self._session.verify = ca_certs

        if disable_ssl_certificate_validation is True:
            self._session.verify = False

        if proxy is not None:
            self._proxy = proxy

        self._timeout = timeout

    # pylint: enable=too-many-arguments

    def __del__(self):
        """
        Destructor.  Closes all network connections.
        """

        self.close()


    def close(self) -> None:
        """
        Closes any persistent network connections.  Generally, deleting
        this object is sufficient and calling this method is unnecessary.
        """
        self._session.close()


    def get_observatories(
            self
        ) -> List[Dict]:
        """
        Gets a description of the available SSC observatories.

        Returns
        -------
        List
            An array of ObservatoryDescription dictionaries where the
            structure of the dictionary mirrors ObservatoryDescription in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """
        url = self._endpoint + 'observatories'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatory_response = ET.fromstring(response.text)

        observatories = []

        for observatory in observatory_response.findall(\
                '{http://sscweb.gsfc.nasa.gov/schema}Observatory'):

            observatories.append({
                'Id': observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Id').text,
                'Name': observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Name').text,
                'Resolution': int(observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Resolution').text),
                'StartTime': dateutil.parser.parse(observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}StartTime').text),
                'EndTime': dateutil.parser.parse(observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}EndTime').text),
                'ResourceId': observatory.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}ResourceId').text
            })

        return observatories


    def get_ground_stations(
            self
        ) -> List[Dict]:
        """
        Gets a description of the available SSC ground stations.

        Returns
        -------
        List
            An array of GroundStations dictionaries where the
            structure of the dictionary mirrors GroundStations in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """
        url = self._endpoint + 'groundStations'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        ground_station_response = ET.fromstring(response.text)

        ground_stations = []

        for ground_station in ground_station_response.findall(\
                '{http://sscweb.gsfc.nasa.gov/schema}GroundStation'):

            location = ground_station.find(\
                '{http://sscweb.gsfc.nasa.gov/schema}Location')
            latitude = float(location.find(\
                '{http://sscweb.gsfc.nasa.gov/schema}Latitude').text)
            longitude = float(location.find(\
                '{http://sscweb.gsfc.nasa.gov/schema}Longitude').text)

            ground_stations.append({
                'Id': ground_station.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Id').text,
                'Name': ground_station.find(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Name').text,
                'Location': {
                    'Latitude': latitude,
                    'Longitude': longitude
                }
            })

        return ground_stations


    def get_locations(
            self,
            param1: Union[List[str], DataRequest],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> Tuple[int, Dict]:
        """
        Gets the specified locations.  Complex requests (requesting
        magnetic field model values) require a single DataRequest
        parameter.  Simple requests (for only x, y, z, lat, lon,
        local_time) require at least the first two paramters.

        Parameters
        ----------
        param1
            A locations DataRequest or a list of satellite names.
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.
        Returns
        -------
        Dict
            Dictionary whose struture mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        Raises
        ------
        ValueError
            If param1 is not a DataRequest and time_range is missing or
            time_range does not contain valid values.
        """

        if isinstance(param1, DataRequest):
            request = param1
        else:
            sats = []
            for sat in param1:
                sats.append(SatelliteSpecification(sat, 1))

            if time_range is None:
                raise ValueError('time_range value is required when ' +
                                 '1st is not a DataRequest')

            if isinstance(time_range, list):
                time_interval = TimeInterval(time_range[0], time_range[1])
            else:
                time_interval = time_range

            if coords is None:
                coords = [CoordinateSystem.GSE]

            coord_options = []
            for coord in coords:
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.X))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.Y))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.Z))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.LAT))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.LON))
                coord_options.append(
                    CoordinateOptions(coord, CoordinateComponent.LOCAL_TIME))

            request = DataRequest(None, time_interval, sats, None,
                                  OutputOptions(coord_options), None, None)

        return self.__get_locations(request)


    def __get_locations(
            self,
            request: DataRequest
        ) -> Tuple[int, Dict]:
        """
        Gets the given locations DataRequest.

        Parameters
        ----------
        request
            A locations DataRequest.
        Returns
        -------
        Dict
            Dictionary whose struture mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """
        url = self._endpoint + 'locations'

        self.logger.debug('request url = %s', url)

        xml_data_request = request.xml_element()

        response = self._session.post(url,
                                      data=ET.tostring(xml_data_request),
                                      timeout=self._timeout)
        if response.status_code != 200:

            try:
                # requires version 3.9
                ET.indent(xml_data_request)
            except AttributeError:
                pass
            self.logger.debug('request XML = %s', ET.tostring(xml_data_request))

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return (response.status_code, None)

        result_element = ET.fromstring(response.text).find(\
                             '{http://sscweb.gsfc.nasa.gov/schema}Result')

        return (response.status_code, self.__get_result(result_element))


    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    def __get_result(
            self,
            result_element: ET
        ) -> Dict:
        """
        Creates a dict representation of a DataResult from an ElementTree
        representation.

        Parameters
        ----------
        result_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree DataResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """

        #try:
        #    # requires version 3.9
        #    ET.indent(result_element)
        #except AttributeError:
        #    pass
        #self.logger.debug('result_element XML = %s',
        #                  ET.tostring(result_element))

        result = {
            'StatusCode': result_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}StatusCode').text,
            'StatusSubCode': result_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}StatusSubCode').text,
            'Data': []
        }

        data_i = -1

        for data_element in result_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Data'):

            data_i += 1

            coords_element = data_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Coordinates')

            if coords_element is None:
                # Is this the correct result for this case???
                result['Data'].append({
                    'Id': data_element.find(\
                              '{http://sscweb.gsfc.nasa.gov/schema}Id').text
                })
                continue

            coordinates = {
                'CoordinateSystem': CoordinateSystem(coords_element.find(\
                   '{http://sscweb.gsfc.nasa.gov/schema}CoordinateSystem').text),
                'X': [],
                'Y': [],
                'Z': [],
                'Latitude': [],
                'Longitude': [],
                'LocalTime': []
            }
            result['Data'].append({
                'Id': data_element.find(\
                          '{http://sscweb.gsfc.nasa.gov/schema}Id').text,
                'Coordinates': coordinates,
                'Time': [],
                'BTraceData': [],
                'RadialLength': [],
                'MagneticStrength': [],
                'NeutralSheetDistance': [],
                'BowShockDistance': [],
                'MagnetoPauseDistance': [],
                'DipoleLValue': [],
                'DipoleInvariantLatitude': [],
                'SpacecraftRegion': [],
                'RadialTracedFootpointRegions': [],
                'BGseX': [],
                'BGseY': [],
                'BGseZ': [],
                'NorthBTracedFootpointRegions': [],
                'SouthBTracedFootpointRegions': []
            })

            for x_coord in coords_element.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}X'):

                result['Data'][data_i]['Coordinates']['X'].append(\
                    float(x_coord.text))

            for y_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Y'):

                result['Data'][data_i]['Coordinates']['Y'].append(\
                    float(y_coord.text))

            for z_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Z'):

                result['Data'][data_i]['Coordinates']['Z'].append(\
                    float(z_coord.text))

            for lat_coord in coords_element.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Latitude'):

                result['Data'][data_i]['Coordinates']['Latitude'].append(\
                    float(lat_coord.text))

            for lon_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Longitude'):

                result['Data'][data_i]['Coordinates']['Longitude'].append(\
                    float(lon_coord.text))

            for lt_coord in coords_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}LocalTime'):

                result['Data'][data_i]['Coordinates']['LocalTime'].append(\
                    float(lt_coord.text))

            for time in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}Time'):

                result['Data'][data_i]['Time'].append(\
                    dateutil.parser.parse(time.text))

            for b_trace_data in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BTraceData'):

                result['Data'][data_i]['BTraceData'].append({
                    'CoordinateSystem': CoordinateSystem(b_trace_data.find(\
                         '{http://sscweb.gsfc.nasa.gov/schema}CoordinateSystem').text),
                    'Hemisphere': Hemisphere(b_trace_data.find(\
                         '{http://sscweb.gsfc.nasa.gov/schema}Hemisphere').text),
                    'Latitude': [],
                    'Longitude': [],
                    'ArcLength': []
                })
                for lat in b_trace_data.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Latitude'):

                    result['Data'][data_i]['BTraceData'][-1]['Latitude'].append(\
                        float(lat.text))

                for lon in b_trace_data.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}Longitude'):

                    result['Data'][data_i]['BTraceData'][-1]['Longitude'].append(\
                        float(lon.text))

                for arc_length in b_trace_data.findall(\
                    '{http://sscweb.gsfc.nasa.gov/schema}ArcLength'):

                    result['Data'][data_i]['BTraceData'][-1]['ArcLength'].append(\
                         float(arc_length.text))

            for radial_length in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}RadialLength'):

                result['Data'][data_i]['RadialLength'].append(\
                    float(radial_length.text))

            for magnetic_strength in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}MagneticStrength'):

                result['Data'][data_i]['MagneticStrength'].append(\
                    float(magnetic_strength.text))

            for neutral_sheet_distance in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}NeutralSheetDistance'):

                result['Data'][data_i]['NeutralSheetDistance'].append(\
                    float(neutral_sheet_distance.text))

            for bow_shock_distance in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BowShockDistance'):

                result['Data'][data_i]['BowShockDistance'].append(\
                    float(bow_shock_distance.text))

            for magneto_pause_distance in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}MagnetoPauseDistance'):

                result['Data'][data_i]['MagnetoPauseDistance'].append(\
                    float(magneto_pause_distance.text))

            for dipole_l_value in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}DipoleLValue'):

                result['Data'][data_i]['DipoleLValue'].append(\
                    float(dipole_l_value.text))

            for dipole_invariant_latitude in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}DipoleInvariantLatitude'):

                result['Data'][data_i]['DipoleInvariantLatitude'].append(\
                    float(dipole_invariant_latitude.text))

            for spacecraft_region in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}SpacecraftRegion'):

                result['Data'][data_i]['SpacecraftRegion'].append(\
                    SpaceRegion(spacecraft_region.text))

            for radial_footpoint_region in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}RadialTracedFootpointRegions'):

                result['Data'][data_i]['RadialTracedFootpointRegions'].append(\
                    FootpointRegion(radial_footpoint_region.text))

            for b_gse_x in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BGseX'):

                result['Data'][data_i]['BGseX'].append(\
                    float(b_gse_x.text))

            for b_gse_y in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BGseY'):

                result['Data'][data_i]['BGseY'].append(\
                    float(b_gse_y.text))

            for b_gse_z in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}BGseZ'):

                result['Data'][data_i]['BGseZ'].append(\
                    float(b_gse_z.text))

            for b_traced_footpoint_region in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}NorthBTracedFootpointRegions'):

                result['Data'][data_i]['NorthBTracedFootpointRegions'].append(\
                    FootpointRegion(b_traced_footpoint_region.text))

            for b_traced_footpoint_region in data_element.findall(\
                   '{http://sscweb.gsfc.nasa.gov/schema}SouthBTracedFootpointRegions'):

                result['Data'][data_i]['SouthBTracedFootpointRegions'].append(\
                    FootpointRegion(b_traced_footpoint_region.text))

        #print(result)

        return result
    # pylint: enable=too-many-locals
    # pylint: enable=too-many-branches
