#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2017 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from ..df.backends.pd.types import _np_to_df_types
from ..df.backends.odpssql.types import df_type_to_odps_type
from ..df import types


def pd_type_to_odps_type(dtype, col_name, unknown_as_string=None):
    import numpy as np

    if dtype in _np_to_df_types:
        df_type = _np_to_df_types[dtype]
    elif dtype == np.datetime64(0, 'ns'):
        df_type = types.timestamp
    elif unknown_as_string:
        df_type = types.string
    else:
        raise ValueError('Unknown type {}, column name is {},'
                         'specify `unknown_as_string=True` '
                         'or `as_type` to set column dtype'.format(dtype, col_name))

    return df_type_to_odps_type(df_type)


def use_odps2_type(func):
    def wrapped(*args, **kwargs):
        from odps import options
        old_value = options.sql.use_odps2_extension
        options.sql.use_odps2_extension = True

        old_settings = options.sql.settings
        options.sql.settings = old_settings or {}
        options.sql.settings.update({'odps.sql.hive.compatible': True})
        options.sql.settings.update({'odps.sql.decimal.odps2': True})
        try:
            func(*args, **kwargs)
        finally:
            options.sql.use_odps2_extension = old_value
            options.sql.settings = old_settings

    return wrapped


def convert_pandas_object_to_string(df):
    import pandas as pd
    import numpy as np

    def convert_to_string(v):
        if v is None or pd.isna(v):
            return None
        else:
            return str(v)

    object_columns = [c for c, t in df.dtypes.iteritems() if t == np.dtype('O')]
    for col in object_columns:
        df[col] = df[col].map(convert_to_string)
    return df
