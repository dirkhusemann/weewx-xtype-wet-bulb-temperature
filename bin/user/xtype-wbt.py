#!/usr/bin/env python3

import math

import weewx
import weewx.units
import weewx.xtypes
from weewx.units import ValueTuple

def assert_prereq(record, typ):
    if typ not in record or record[typ] is None:
        raise weewx.CannotCalculate(obs_type)

def value_tuple_for(typ):
    unit_group = weewx.units.getStandardUnitType(record['usUnits'], typ)
    # ... then form the ValueTuple.
    value_tuple = ValueTuple(record[typ], *unit_group)
    return value_tuple
    
def value_unit(typ, unit):
    vt = value_tuple_for(typ)
    vu = weewx.units.convert(vt, unit)
    return vu[0]


class WetBulbTemperature(weewx.xtypes.XType):

    def __init__(self, algorithm='full'):
        self.algorithm = algorithm.lower()

    def get_scalar(self, obs_type, record, db_manager):
        # We only know how to calculate 'wet_bulb_temperature'. For everything else, raise an exception UnknownType
        if obs_type != 'wet_bulb_temperature':
            raise weewx.UnknownType(obs_type)

        assert_prereq(record, 'outTemp')
        assert_prereq(record, 'outHumidity')
        assert_prereq(record, 'barometer')

        # We have everything we need. Start by forming a ValueTuple for the outside temperature.
        # To do this, figure out what unit and group the record is in ...

        outTemp_C = value_unit('outTemp', 'degree_C')
        outHumidity_percent = value_type_for('outHumidity', 'percent')
        barometer_hPa = value_type_for('barometer', 'hPa')

        wbt_C = outTemp_C * math.atan(0.151977 * math.sqrt(outHumidity_percent + 8.313659)) + \
            math.atan(outTemp_C + outHumidity_percent) - \
            math.atan(outHumidity_percent - 1.676331) + 0.00391838 * \
            math.pow(outHumidity_percent, 1.5) * \
            math.atan(0.023101 * outHumidity_percent) - 4.686035

        wbt_vt = ValueTuple(wbt_C, 'degree_C', 'group_temperature')
        # If we got this far, we were able to calculate a value. Return it.
        return wbt_vt

