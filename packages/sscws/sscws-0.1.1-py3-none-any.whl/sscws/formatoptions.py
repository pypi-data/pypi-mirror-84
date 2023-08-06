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
Module defining classes to represent the output format option classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

from enum import Enum


class DateFormat(Enum):
    """
    Enumerations representing the DateFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    YYYY_DDD = 'yyyy_ddd'
    YY_MM_DD = 'yy_mm_dd'
    YY_MMM_DD = 'yy_Mmm_dd'
    YY_CMMM_DD = 'yy_CMMM_dd'


class DegreeFormat(Enum):
    """
    Enumerations representing the DegreeFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    DECIMAL = 'Decimal'
    MINUTES = 'Minutes'
    MINUTES_SECONDS = 'MinutesSeconds'


class DistanceFormat(Enum):
    """
    Enumerations representing the DistanceFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    RE = 'Re'
    KM = 'Km'
    INTEGER_KM = 'IntegerKm'
    SCIENTFIC_NOTATION_KM = 'ScientificNotationKm'


class LatLonFormat(Enum):
    """
    Enumerations representing the LatLonFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    LAT_90_LON_360 = 'Lat90Lon360'
    LAT_90_LON_180 = 'Lat90Lon180'
    LAT_90_SN_LON_180_WE = 'Lat90SnLon180We'


class TimeFormat(Enum):
    """
    Enumerations representing the TimeFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    HH_HHHH = 'hh_hhhh'
    HH_MM_SS = 'hh_mm_ss'
    HH_MM = 'hh_mm'
