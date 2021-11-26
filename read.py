import json
from pathlib import Path

import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.precision', 8)
pd.set_option('display.width', None)


def read(path, value, key='code'):
    '''
    path = Path('~/path/to/file/that/has/json/on/each/line').expanduser()
    read(path, 'something')
    '''
    if not value:
        return pd.DataFrame()
    with open(path, 'r', encoding='utf-8') as f:
        xs = []
        for line in f:
            row = json.loads(line)
            if row.get(key) == value:
                del row[key]
                row.pop('message', None)
                xs.append(row)
    ys = pd.DataFrame(xs)
    if 'time' in ys.columns:
        ys['time'] = pd.to_datetime(ys['time'])
        ys = ys.sort_values('time')
    return ys
