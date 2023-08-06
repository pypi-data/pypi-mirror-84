# Copyright 2020-present, Mayo Clinic Department of Neurology
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from datetime import datetime, timedelta
from pandas._libs.tslibs.timestamps import Timestamp
from dateutil import tz
import pandas as pd
import numpy as np
from copy import deepcopy
from tqdm import tqdm


def _convert_to_timestamp(x):
    if isinstance(x, (datetime, Timestamp)):
        assert x.tzinfo, '[TIMEZONE ERROR] We allow operating with timezone-aware datatypes. This helps preventing inconsistency and errors.'
        return x.timestamp()
    if isinstance(x, (float, int)): return x
    raise TypeError('[TYPE ERROR]: input variable has to be of a type pandas Timestamp, datetime, float, or int. However ' + type(x) + ' recieved.')


def _convert_to_datetime_utc(x):
    if isinstance(x, (datetime, Timestamp)):
        assert x.tzinfo, '[TIMEZONE ERROR] We allow operating with timezone-aware datatypes. This helps preventing inconsistency and errors.'
        x = x.timestamp()
    if isinstance(x, (float, int)):
        utc = datetime.utcfromtimestamp(x)
        utc = utc.replace(tzinfo=tz.tzutc())

        return utc
    raise TypeError('[TYPE ERROR]: input variable has to be of a type pandas Timestamp, datetime, float, or int. However ' + type(x) + ' recieved.')


def _convert_to_pandas_timestamp_utc(x):
    if isinstance(x, (datetime, Timestamp)):
        assert x.tzinfo, '[TIMEZONE ERROR] We allow operating with timezone-aware datatypes. This helps preventing inconsistency and errors.'
        x = x.timestamp()
    if isinstance(x, (float, int)):
        utc = datetime.utcfromtimestamp(x)
        utc = utc.replace(tzinfo=tz.tzutc())
        utc = Timestamp(utc)
        return utc
    raise TypeError('[TYPE ERROR]: input variable has to be of a type pandas Timestamp, datetime, float, or int. However ' + type(x) + ' recieved.')


def _convert_to_utc(x):
    x = _convert_to_datetime_utc(x)
    return x


def _convert_to_local(x):
    x = _convert_to_datetime_utc(x)
    x = x.astimezone(tz.tzlocal())
    return x


def _convert_to_timezone(x, tzinfo):
    x = _convert_to_datetime_utc(x)
    x = x.astimezone(tzinfo)
    return x


def time_to_timezone(dfHyp, tzinfo):
    def convert(x, col_key):
        return _convert_to_timezone(x[col_key], tzinfo)

    dfHyp['start'] = dfHyp.apply(lambda x: convert(x, 'start'), axis=1)
    dfHyp['end'] = dfHyp.apply(lambda x: convert(x, 'end'), axis=1)
    return dfHyp


def time_to_local(dfHyp):
    def convert(x, col_key):
        return _convert_to_local(x[col_key])

    dfHyp['start'] = dfHyp.apply(lambda x: convert(x, 'start'), axis=1)
    dfHyp['end'] = dfHyp.apply(lambda x: convert(x, 'end'), axis=1)
    return dfHyp


def time_to_utc(dfHyp):
    def convert(x, col_key):
        return _convert_to_utc(x[col_key])

    dfHyp['start'] = dfHyp.apply(lambda x: convert(x, 'start'), axis=1)
    dfHyp['end'] = dfHyp.apply(lambda x: convert(x, 'end'), axis=1)
    return dfHyp


def time_to_timezone(dfHyp, tzinfo):
    def convert(x, col_key):
        return _convert_to_timezone(x[col_key], tzinfo)

    dfHyp['start'] = dfHyp.apply(lambda x: convert(x, 'start'), axis=1)
    dfHyp['end'] = dfHyp.apply(lambda x: convert(x, 'end'), axis=1)
    return dfHyp


def time_to_timestamp(dfHyp):
    def convert(x, col_key):
        return _convert_to_timestamp(x[col_key])

    dfHyp['start'] = dfHyp.apply(lambda x: convert(x, 'start'), axis=1)
    dfHyp['end'] = dfHyp.apply(lambda x: convert(x, 'end'), axis=1)
    return dfHyp


def create_duration(dfHyp):
    def duration(x):
        return _convert_to_timestamp(x['end']) - _convert_to_timestamp(x['start'])
    dfHyp['duration'] = dfHyp.apply(lambda x: duration(x), axis=1)
    return dfHyp


def create_day_indexes(dfHyp, hour=12):
    if not isinstance(dfHyp, pd.DataFrame):
        raise AssertionError('[INPUT ERROR]: Variable dfHyp must be of a type pandas.DataFrame.')

    for row in dfHyp.iterrows():
        if not isinstance(row[1]['start'], (Timestamp, datetime)):
            raise AssertionError('[INPUT ERROR]: columns \'start \' & \'end\' must be timezone-aware format variables such as datetime or pandas-based Timestamp')

        if not row[1]['start'].tzinfo:
            raise AssertionError('[INPUT ERROR]: columns \'start \' & \'end\' must be timezone-aware format variables such as datetime or pandas-based Timestamp')

    if not isinstance(hour, int):
            raise AssertionError('[INPUT ERROR]: hour variable must be of an integer type!')

    if hour < 0 or hour > 23:
        raise ValueError(
            '[VALUE ERROR] - An input variable hour_cut indicating at which hour days are separated from each other must be on the range between 0 - 23. Pasted value: ',
            hour)

    dfHyp = dfHyp.sort_values('start').reset_index(drop=True)
    day_idx = 0
    day_idxes = [day_idx]
    for idx in range(1, dfHyp.__len__()):
        t1 = dfHyp['start'][idx-1]
        t2 = dfHyp['start'][idx]
        if hour == 0:
            ref = datetime(t1.year, t1.month, t1.day+1, hour, 00, 00, tzinfo=dfHyp.start[0].tzinfo)
        else:
            ref = datetime(t1.year, t1.month, t1.day, hour, 00, 00, tzinfo=dfHyp.start[0].tzinfo)

        if t1.timestamp() < ref.timestamp() <= t2.timestamp():
            day_idx += 1
        day_idxes.append(day_idx)
    dfHyp['day'] = day_idxes
    return dfHyp


def merge_annotations(df):
    new_df = pd.DataFrame()
    for idx, row in enumerate(df.iterrows()):
        appbl = True
        if idx > 0:
            if new_df.iloc[-1].annotation == row[1].annotation and new_df.iloc[-1].end == row[1].start:
                appbl = False

        if appbl == True:
            new_df = new_df.append(row[1], ignore_index=True)
        else:
            new_df.loc[new_df.__len__() - 1, 'end'] = row[1].end
        new_df.loc[new_df.__len__() - 1, 'duration'] = (new_df.loc[new_df.__len__() - 1, 'end'] - new_df.loc[new_df.__len__() - 1, 'start']).seconds
    return new_df


def tile_row(row, dur_threshold):
    outp = []
    start_time = row['start']
    end_time = row['end']
    curr_time = row['start']
    delta = timedelta(seconds=dur_threshold)

    for idx in range(int(np.ceil(row['duration']/dur_threshold))):
        row_ = row.copy(deep=True)
        row_['start'] = curr_time
        curr_time += delta
        row_['end'] = curr_time
        row_['duration'] = (row_['end'] - row_['start']).seconds
        outp += [row_]

    outp[-1]['end'] = end_time
    outp[-1]['duration'] = (outp[-1]['end'] - outp[-1]['start']).seconds
    return outp


def tile_annotations(df, dur_threshold):
    if not isinstance(df, pd.DataFrame):
        raise AssertionError('[INPUT ERROR]: Variable dfAnnotations must be of type pandas.DataFrame.')

    if not isinstance(dur_threshold, (int, float)):
        raise AssertionError(
            '[INPUT ERROR]: dur_threshold must be float or int format giving the maximum duration of a single annotation. All anotations above this duration threshold will be tiled.')

    if np.isnan(dur_threshold) or np.isinf(dur_threshold) or dur_threshold <= 0:
        raise AssertionError('[INPUT ERROR]: dur_threshold must be a valid number bigger than 0, not nan and not inf')

    outp = []
    for row in tqdm(list(df.iterrows())):
        row = row[1]
        outp += tile_row(row, dur_threshold)
    return pd.DataFrame(outp).reset_index(drop=True)


def filter_by_duration(dfAnnotations, duration):
    if not isinstance(dfAnnotations, pd.DataFrame):
        raise AssertionError('[INPUT ERROR]: Variable dfAnnotations must be of a type pandas.DataFrame.')

    if not isinstance(duration, (int, float)):
        raise AssertionError(
            '[INPUT ERROR]: duration must be float or int format giving the maximum duration of a single annotation. All anotations above this duration threshold will be tiled.')

    if np.isnan(duration) or np.isinf(duration) or duration <= 0:
        raise AssertionError('[INPUT ERROR]: duration must be a valid number bigger than 0, not nan and not inf')

    dfAnnotations = dfAnnotations.loc[dfAnnotations['duration'] == duration].reset_index(drop=True)
    return dfAnnotations


def filter_by_key(dfAnnotations, key, value):
    return dfAnnotations.loc[dfAnnotations[key] != value].reset_index(drop=True)




