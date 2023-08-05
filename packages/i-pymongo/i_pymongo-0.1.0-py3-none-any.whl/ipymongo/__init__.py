# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
from ipymongo import client
# ============================================================ Python.
import os
# ============================================================ ExternalPackages.
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
# ============================================================ MyPackages.
import idebug as dbg
# ============================================================ Constant.
# ============================================================ APIs.
from ipymongo.model import Model

from ipymongo.database import list_collection_names
from ipymongo.database import list_collections
from ipymongo.database import command_collstats
from ipymongo.database import command_connpoolstats
from ipymongo.database import search_collections
from ipymongo.database import drop_all_tables
