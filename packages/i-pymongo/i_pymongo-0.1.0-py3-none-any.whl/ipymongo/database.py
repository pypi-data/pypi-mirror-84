# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import re
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ ExternalPackages.
from pymongo import MongoClient, ASCENDING, DESCENDING
# ============================================================ MyPackages.
import idebug as dbg
# ============================================================ IntraPackage.
# ============================================================ Constant.

#============================================================
#============================================================
@dbg.fruntime
def list_collection_names(db):
    tbls = db.list_collection_names()
    return sorted(tbls)


@dbg.fruntime
def list_collections(db):
    cursor = db.list_collections()
    dbg.clsdict(cls=cursor)
    return cursor


@dbg.fruntime
def command_collstats(db, tblname):
    response = db.command('collstats', tblname)
    dbg.clsdict(cls=response)
    return response


@dbg.fruntime
def command_connpoolstats(db):
    pp.pprint(db.command({'connPoolStats':1}))


@dbg.fruntime
def search_collections(regex):
    tbls = list_collection_names()
    p = re.compile(regex)
    tables = []
    for tbl in tbls:
        if p.search(string=tbl) is not None:
            tables.append(tbl)
    return tables


@dbg.fruntime
def drop_all_tables(db):
    tblnames = db.list_collection_names()
    for tblname in tblnames:
        print(f"\n Dropped tblname : {tblname}")
        db[tblname].drop()
