#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ft times
"""
from featuretools.primitives import TimeSinceLast, TimeSinceFirst, AvgTimeBetween, TimeSince,TimeSincePrevious

class time_unit:
    def __init__(self,units):
        self.units = units
        #time_unit.a = self.unit
        time_unit.time_since_last = TimeSinceLast(unit = self.units+'s')
        time_unit.time_since_first = TimeSinceFirst(unit = self.units+'s')
        time_unit.avg_time_between = AvgTimeBetween(unit = self.units+'s')
        time_unit.time_since = TimeSince(unit = self.units+'s')
        time_unit.time_since_previous = TimeSincePrevious(unit = self.units+'s')

#t = time_unit('Y')
