# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
import re
import inspect
# ============================================================ ExternalPackages.
import pandas as pd
from pandas.io.json import json_normalize
from bson.objectid import ObjectId
# ============================================================ MyPackages.
import idebug as dbg
from ipy import idatetime
# ============================================================ IntraPackage.
from ipymongo import client
from ipymongo import collection as coll
# ============================================================ Constant.


# ============================================================
"""DataModel."""
# ============================================================
p_id = re.compile('id$|Id$')
p_dt = re.compile('^dt$')

class Model(coll.CollectionOperators):
    """Model = Collectioin.
    오직 데이터베이스 테이블에 대한 작업만.
    df(ModelData) 에 대한 핸들링은 여기서 절대 금지.
    """
    def __init__(self, dbname):
        self.db = client.client[dbname]
    def modeling(self, cls):
        try:
            self.tbl = self.db[cls.__name__]
        except Exception as e:
            dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
            raise
        finally:
            return self
    def schematize(self):
        try:
            self.doc = {}
            for attr in list(self.__dict__):
                if attr in self.schema:
                    self.doc[attr] = getattr(self, attr)
        except Exception as e:
            dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
        finally:
            return self
    def clean_filter(self, **filter):
        """데이터 타입만 청소한다."""
        for k, v in filter.items():
            if p_id.search(k) is not None:
                if isinstance(v, ObjectId):
                    pass
                elif isinstance(v, str):
                    v = ObjectId(v)
                else:
                    raise
            elif p_dt.search(k) is not None:
                v = idatetime.parse(v)
            else:
                pass
        return filter
    def data_normalize(self):
        if len(self.df) is 0:
            dbg.printer(self.df)
        else:
            meta = list(self.df.columns)
            meta.remove('data')
            # dbg.printer(f"meta : {meta}")
            df = json_normalize(self.df.to_dict('records'), 'data', meta)
            if len(df) is 0:
                dbg.printer(df)
            else:
                pass
            self.df = df
        return self
    def tz_convert(self, df, tz='Asia/Seoul'):
        try:
            df.dt = df.dt.dt.tz_convert(tz=tz)
        except Exception as e:
            dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
            raise
        finally:
            return df
