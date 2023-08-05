# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import pprint
pp = pprint.PrettyPrinter(indent=2)
import inspect
# ============================================================ ExternalPackages.
import pandas as pd
# ============================================================ MyPackages.
import idebug as dbg
# ============================================================ IntraPackage.
# ============================================================ Constant.


# ============================================================
"""Model."""
# ============================================================
class CollectionOperators:
    def find_tbl(self, filter=None, projection=None):
        return find_tbl(self.tbl, filter, projection)
    def load_tbl(self, filter=None, projection=None):
        self.df = find_tbl(self.tbl, filter, projection)
        return self
    def find_limit(self, filter=None, projection=None, n=1):
        return find_limit(self.tbl, filter=filter, projection=projection, n=n)
    def docs_count(self):
        return docs_count(self.tbl)
    def n_returned(self, cursor):
        return n_returned(cursor)
    def update_one(self, filter, update, upsert=False):
        return update_one(self.tbl, filter, update, upsert)
    def update_many(self, filter, update, upsert=False):
        return update_many(self.tbl, filter, update, upsert)
    def replace_one(self, filter, replacement, upsert=False):
        return replace_one(self.tbl, filter, replacement, upsert)
    def update_addToData(self, filter, data, upsert=False):
        return update_addToData(self.tbl, filter, data, upsert)
    def update_pushToData(self, filter, data, upsert=False):
        return update_pushToData(self.tbl, filter, data, upsert)
    def update_one_schema(self, upsert=False):
        return update_one_schema(self, upsert)
    def update_doc(self, filter, upsert=False):
        return update_doc(self, filter, upsert)
    def insert_many(self, data):
        return insert_many(self.tbl, data)
    def insert_doc(self):
        return insert_doc(self)
    def delete_one(self, filter):
        return delete_one(self.tbl, filter)
    def delete_many(self, filter):
        return delete_many(self.tbl, filter)
# ============================================================
"""Schema."""
# ============================================================
def n_returned(cursor):
    cnt = cursor.explain()['executionStats']['nReturned']
    dbg.printer(f"cursor.explain()['executionStats']['nReturned'] : {cnt}")
    return cnt

def docs_count(tbl):
    cursor = tbl.find({}, {'_id'})
    cnt = cursor.count()
    print(f"n_documents : {'{:,}'.format(cnt)}")
    return cnt
# ============================================================
"""Qeury."""
# ============================================================
@dbg.fruntime
def find_tbl(tbl, filter=None, projection=None):
    cursor = tbl.find(filter, projection)
    return pd.DataFrame(list(cursor))

def find_limit(tbl, filter=None, projection=None, n=1):
    cursor = tbl.find(filter, projection).limit(n)
    return pd.DataFrame(list(cursor))
# ============================================================
"""Insert."""
# ============================================================
@dbg.fruntime
def insert_doc(cls):
    try:
        cls.schematize()
        InsertOneResult = cls.tbl.insert_one(cls.doc)
    except Exception as e:
        raise
    else:
        pp.pprint(InsertOneResult.raw_result)
        del(cls.doc['_id'])
    finally:
        return cls

@dbg.fruntime
def insert_many(tbl, data):
    try:
        InsertManyResult = tbl.insert_many(data, ordered=True, bypass_document_validation=False, session=None)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        # 예외적으로 무조건 찍는다. 왜냐, 한번만 로그 찍으니까.
        dbg.clsattrs(InsertManyResult)
# ============================================================
"""Update."""
# ============================================================
@dbg.fruntime
def update_one(tbl, filter, update, upsert=False):
    try:
        UpdateResult = tbl.update_one(filter, update, upsert,
                                    bypass_document_validation=False, collation=None,
                                    array_filters=None, session=None)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        dbg.printer(filter)
        dbg.clsattrs(UpdateResult)

@dbg.fruntime
def update_many(tbl, filter, update, upsert=False):
    try:
        UpdateResult = tbl.update_many(filter, update, upsert,
                                    array_filters=None, bypass_document_validation=False,
                                    collation=None, session=None)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        dbg.clsattrs(UpdateResult)

@dbg.fruntime
def replace_one(tbl, filter, replacement, upsert=False):
    try:
        UpdateResult = tbl.replace_one(filter, replacement, upsert,
                                    bypass_document_validation=False,
                                    collation=None, session=None)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        dbg.clsattrs(UpdateResult)

@dbg.fruntime
def update_doc(cls, filter, upsert=False):
    cls.schematize()
    update_one(cls.tbl, filter, {'$set':cls.doc}, upsert)

@dbg.fruntime
def update_addToData(tbl, filter, data, upsert=False):
    tbl.update_one(filter=filter,
                    update={'$addToSet':{'data':{'$each':data}}},
                    upsert=upsert)

@dbg.fruntime
def update_pushToData(tbl, filter, data, upsert=False):
    update_one(tbl=tbl,
            filter=filter,
            update={'$push':{'data':{'$each':data}}},
            upsert=upsert)

@dbg.fruntime
def static_update_addToData(cls, upsert=False):
    update_one(cls.tbl,
            {c:getattr(cls, c) for c in cls.id_cols},
            {'$addToSet':{'data':{'$each':cls.data}}},
            upsert)


@dbg.fruntime
def update_one_schema(cls, upsert=False):
    update_one(cls.tbl,
            {e:getattr(cls,e) for e in cls.id_cols},
            {'$set':{e:getattr(cls,e) for e in cls.schema}},
            upsert)

# ============================================================
"""Delete."""
# ============================================================
@dbg.fruntime
def delete_one(tbl, filter):
    try:
        UpdateResult = tbl.delete_one(filter)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        dbg.clsattrs(UpdateResult)

@dbg.fruntime
def delete_many(tbl, filter):
    try:
        UpdateResult = tbl.delete_many(filter)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        dbg.clsattrs(UpdateResult)

@dbg.fruntime
def remove_in_nested_data(cls, cond={'trd_dd':'2100/01/01'}):
    cls.update_one({c:getattr(cls, c) for c in cls.id_cols},
                    {'$pull':{'data':cond}})
