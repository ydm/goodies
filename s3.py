import os
import re

import awswrangler as wr
import boto3
import pandas as pd


default_profile = None


def arguments(*segments, defaults=None, **kwargs):
    path = os.path.join(*segments)
    if not path.startswith('s3://'):
        path = f's3://{path}'

    defaults = defaults or {}
    profile = kwargs.pop('profile', default_profile)
    if 'boto3_session' not in kwargs and profile:
        defaults['boto3_session'] = boto3.Session(profile_name=profile)
    defaults.update(kwargs)

    return path, defaults


def delete_object(path, **kwargs):
    path, kwargs = arguments(path, **kwargs)
    return wr.s3.delete_objects(path, **kwargs)


def get_latest_partition(prefix, partition_key='date', **kwargs):
    path, kwargs = arguments(prefix, **kwargs)
    xs = wr.s3.list_directories(path, **kwargs)

    def key(x):
        return pd.to_datetime(re.search(f'{partition_key}=([^/]+)', x).group(1))

    ys = sorted(xs, key=key)
    if ys:
        return ys[-1]


def match_partition(prefix, dt, partition_key='date', **kwargs):
    """
    Works with the presumption
    """
    dt = pd.to_datetime(dt)

    path, kwargs = arguments(prefix, **kwargs)
    xs = wr.s3.list_directories(path, **kwargs)

    def extract_dt(x):
        return pd.to_datetime(re.search(f'{partition_key}=([^/]+)', x).group(1))

    for x in xs:
        if dt == extract_dt(x):
            return x


def read(path, **kwargs):
    defaults = {
        'ignore_index': False,
        'dataset': True,
    }
    parse_dates = kwargs.pop('parse_dates', [])
    path, kwargs = arguments(path, defaults=defaults, **kwargs)
    data = wr.s3.read_parquet(path, **kwargs)
    for column in parse_dates:
        data[column] = pd.to_datetime(data[column])
    return data


def read_partition(path, date, **kwargs):
    partition = pd.to_datetime(date).strftime('date=%Y-%m-%d %H:%M:%S')
    path, kwargs = arguments(path, partition, **kwargs)
    return read(path, **kwargs)


def write(data, path, **kwargs):
    defaults = {
        'index': True,
        'compression': 'gzip',
        'dataset': True,
        'use_threads': True,
    }
    path, kwargs = arguments(path, defaults=defaults, **kwargs)
    # Partition by date by default.
    if 'partition_cols' not in kwargs:
        dates = ['date']  # ['date', 'datetime', 'time']
        cols = [c for c in dates if c in data.columns][:1]
        if cols:
            kwargs['partition_cols'] = cols
    return wr.s3.to_parquet(data, path, **kwargs)
