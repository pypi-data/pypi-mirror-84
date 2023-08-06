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
Module defining classes to represent the Result class and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
from abc import ABCMeta, abstractmethod
from enum import Enum


class ResultStatusCode(Enum):
    """
    Enumerations representing the ResultStatusCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    CONDITIONAL_SUCCESS = 'ConditionalSuccess'
    ERROR = 'Error'


class ResultStatusSubCode(Enum):
    """
    Enumerations representing the ResultStatusSubCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    MISSING_REQUEST = 'MissingRequest'
    MISSING_SATELLITES = 'MissingSatellites'
    INVALID_BEGIN_TIME = 'InvalidBeginTime'
    INVALID_END_TIME = 'InvalidEndTime'
    INVALID_SATELLITE = 'InvalidSatellite'
    INVALID_TIME_RANGE = 'InvalidTimeRange'
    INVALID_RESOLUTION_FACTOR = 'InvalidResolutionFactor'
    MISSING_OUTPUT_OPTIONS = 'MissingOutputOptions'
    MISSING_COORD_OPTIONS = 'MissingCoordOptions'
    MISSING_COORD_SYSTEM = 'MissingCoordSystem'
    INVALID_COORD_SYSTEM = 'InvalidCoordSystem'
    MISSING_COORD_COMPONENT = 'MissingCoordComponent'
    MISSING_GRAPH_OPTIONS = 'MissingGraphOptions'
    MISSING_COORDINATE_SYSTEM = 'MissingCoordinateSystem'
    MISSING_COORDINATE_COMPONENT = 'MissingCoordinateComponent'
    SERVER_ERROR = 'ServerError'


class Result(metaclass=ABCMeta):
    """
    Class representing a Result from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Notes
    -----
    Although this class is essentially a dictionary, it was defined as a
    class to make certain that it matched the structure and key names
    of a Request from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    It also needs to function as a base class for the concrete
    sub-classes of a Request.

    Properties
    ----------
    status_code
        Result status code.
    status_sub_code
        Result status sub-code.
    status_text
        Result status text.
    """
    @abstractmethod
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str]):
        """
        Creates an object representing a Result from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        status_code
            Result status code value.
        status_sub_code
            Result status subcode value.
        status_text
            Status text.
        """
        self._status_code = status_code
        self._status_sub_code = status_sub_code
        self._status_text = status_text


    @property
    def status_code(self):
        """
        Gets the status_code value.

        Returns
        -------
        str
            status_code value.
        """
        return self._status_code


    @status_code.setter
    def status_code(self, value):
        """
        Sets the status_code value.

        Parameters
        ----------
        value
            status_code value.
        """
        self._status_code = value



    @property
    def status_sub_code(self):
        """
        Gets the status_sub_code value.

        Returns
        -------
        str
            status_sub_code value.
        """
        return self._status_sub_code


    @status_sub_code.setter
    def status_sub_code(self, value):
        """
        Sets the status_sub_code value.

        Parameters
        ----------
        value
            status_sub_code value.
        """
        self._status_sub_code = value



    @property
    def status_text(self):
        """
        Gets the status_text value.

        Returns
        -------
        str
            status_text value.
        """
        return self._status_text


    @status_text.setter
    def status_text(self, value):
        """
        Sets the status_text value.

        Parameters
        ----------
        value
            status_text value.
        """
        self._status_text = value


#    @staticmethod
#    def get_result(
#            xml: str
#        ) -> Result:
#        """
#        Produces a Result from the given xml representation of a Result.
#
#        Parameters
#        ----------
#        xml
#            XML representation of a Result.
#        Returns
#        -------
#        Result
#            Result representation of given xml.
#        Raises
#        ------
#        ValueError
#            If the given xml is not a valid XML representation of Result.
#        """
#        result = ET.fromstring(xml)
#
#        self._status_code = int(result.find(\
#            '{http://sscweb.gsfc.nasa.gov/schema}StatusCode').text)
#        self._status_sub_code = int(result.find(\
#            '{http://sscweb.gsfc.nasa.gov/schema}StatusSubCode').text)
#
#        for text in result.findall(\
#            '{http://sscweb.gsfc.nasa.gov/schema}StatusText'):
#            self._status_text.append(text.text)


class FileDescription:
    """
    Class representing a FileDescription from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    name
        Name of file (usually a URL).
    mime_type
        MIME type of file.
    length
        Length of file in bytes.
    last_modified
        Time when file was last modified.
    """
    def __init__(
            self,
            name: str,
            mime_type: str,
            length: int,
            last_modified: datetime):
        """
        Creates a FileDescription object.

        Parameters
        ----------
        name
            Name of file (usually a URL).
        mime_type
            MIME type of file.
        length
            Length of file in bytes.
        last_modified
            Time when file was last modified.
        """
        self._name = name
        self._mime_type = mime_type
        self._length = length
        self._last_modified = last_modified

    @property
    def name(self):
        """
        Gets the name value.

        Returns
        -------
        str
            name value.
        """
        return self._name


    @name.setter
    def name(self, value):
        """
        Sets the name value.

        Parameters
        ----------
        value
            name value.
        """
        self._name = value


    @property
    def mime_type(self):
        """
        Gets the mime_type value.

        Returns
        -------
        str
            mime_type value.
        """
        return self._mime_type


    @mime_type.setter
    def mime_type(self, value):
        """
        Sets the mime_type value.

        Parameters
        ----------
        value
            mime_type value.
        """
        self._mime_type = value


    @property
    def length(self):
        """
        Gets the length value.

        Returns
        -------
        str
            length value.
        """
        return self._length


    @length.setter
    def length(self, value):
        """
        Sets the length value.

        Parameters
        ----------
        value
            length value.
        """
        self._length = value


    @property
    def last_modified(self):
        """
        Gets the last_modified value.

        Returns
        -------
        str
            last_modified value.
        """
        return self._last_modified


    @last_modified.setter
    def last_modified(self, value):
        """
        Sets the last_modified value.

        Parameters
        ----------
        value
            last_modified value.
        """
        self._last_modified = value


class FileResult(Result):
    """
    Class representing a FileResult from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    files
        References to the files containing the requested data.
    """
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str],
            files: List[FileDescription]):
        """
        Creates an object representing a FileResult from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        status_code
            Result status code value.
        status_sub_code
            Result status subcode value.
        status_text
            Status text.
        files
            List of files.
        """
        super().__init__(status_code, status_sub_code, status_text)
        self._files = files


    @property
    def files(self):
        """
        Gets the files value.

        Returns
        -------
        str
            files value.
        """
        return self._files


    @files.setter
    def files(self, value):
        """
        Sets the files value.

        Parameters
        ----------
        value
            files value.
        """
        self._files = value
