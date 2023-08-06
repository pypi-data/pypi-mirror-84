# -*- coding: utf-8 -*-
"""
scrip for customized primitives
"""

import pandas as pd
import numpy as np
import featuretools as ft
from featuretools.primitives import make_agg_primitive, make_trans_primitive
from featuretools.variable_types import Text, Numeric, Categorical, Boolean, Index, DatetimeTimeIndex, Datetime, TimeIndex, Discrete, Ordinal

def enc(col):

    en = 0 if len(col)==0 else 1

    return en

def min_date(col):

    return pd.to_datetime(np.min(col))

def max_date(col):

    return pd.to_datetime(np.max(col))

def n_uni(col):

    return len(set(col))

def f1s(col):

    return col.tolist()[0]

def max_boo(col):

    return np.nanmax(col)

def sum_boo(col):
    return np.sum(col)


def weekday(vals):

    return vals.dt.weekday.values

def is_weekend(vals):

    return vals.dt.weekday.values>4

 
def partofaday(col):
    out=[]
    for c in col:
        if c:
            #h = int(c[:2])
            h = c//100
            if 5<=h<12:
                p='Morning'
            elif 12<=h<17:
                p='Afternoon'
            elif 17<=h<21:
                p='Evening'
            else:
                p='Night'
        else:
            p='Null'
        out.append(p)

    return out
    
def sea_son(vals):
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    out = []
    for v in vals:
        doy = v.timetuple().tm_yday

    # winter = everything else

        if doy in spring:
            season = 'spring'
        elif doy in summer:
            season = 'summer'
        elif doy in fall:
            season = 'fall'
        else:
            season = 'winter'
        out.append(season)
    return out
    

def week_days(vals):
    out = []
    for v in vals:
        out.append(str(v.weekday()))
    return out

def rate(bol1, bol2):
    '''
    Finds the mean of non-null values of a feature that occurred on Sundays
    '''
    return sum(bol1)/sum(bol2) if sum(bol2) else 0

def big_age(values,time=None):
    out = (time-values.iloc[0])/ np.timedelta64(1, 'Y')
    return out
    
def small_age(values,time=None):
    out = (time-values.iloc[-1])/ np.timedelta64(1, 'Y')
    return out

max_age = make_agg_primitive(function=big_age,
        input_types=[DatetimeTimeIndex],
        return_type=Numeric,
        name='MaxAge',
        description="max age till cutoff",
        uses_calc_time=True)
        
min_age = make_agg_primitive(function=small_age,
        input_types=[DatetimeTimeIndex],
        name='MinAge',
        return_type=Numeric,
        description="min age till cutoff",
                            uses_calc_time=True)
rates = make_agg_primitive(function=rate,
                          input_types=[Boolean,Boolean],
                                 return_type=Numeric)

    
seasons = make_trans_primitive(function=sea_son,
                             input_types=[Datetime],
                             return_type=Categorical,
                             name='Seasons')
    
PartDay = make_trans_primitive(function=partofaday,
                               input_types=[Numeric],
                               return_type=Categorical)


enco = make_agg_primitive(function=enc,

                               input_types=[Index], #the reason why using Index is because actually we will count 'index' on 'Where' condition;

                               return_type=Numeric,

                         name='If',stack_on_self=False)

min_d = make_agg_primitive(function=min_date,

                          input_types=[Datetime],

                          return_type=Numeric,name='Min',stack_on_self=False)

max_d = make_agg_primitive(function=max_date,

                          input_types=[Datetime],

                          return_type=Numeric,name='Max',stack_on_self=False)#,name='Max')

u_uniq = make_agg_primitive(function=n_uni,

                          input_types=[Discrete],

                          return_type=Numeric,name='Unique',stack_on_self=False)#,name='Max')

f1st = make_agg_primitive(function=f1s,

                               input_types=[Categorical],

                               return_type=Categorical,name='First')

max_bol = make_agg_primitive(function=max_boo,

                            input_types=[Boolean],

                            return_type=Boolean,

                            name='MaxBol',stack_on_self=False)

sum_bol = make_agg_primitive(function=sum_boo,
                            input_types=[Boolean],
                            return_type=Numeric,
                            name='SumBol',stack_on_self=False)

week_day = make_trans_primitive(function=week_days,
                             input_types=[Datetime],
                             return_type=Categorical,
                             name='Week_day')

 

is_weekend = make_trans_primitive(function=is_weekend,

                             input_types=[Datetime],

                             return_type=Numeric,

                             name='Is_weekend')
