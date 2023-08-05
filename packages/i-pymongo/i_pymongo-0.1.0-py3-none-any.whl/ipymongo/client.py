# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
# ============================================================ ExternalPackages.
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
# ============================================================ MyPackages.
import idebug as dbg
# ============================================================ Constant.
# ============================================================
"""Database-Client."""
# ============================================================
try:
    client = MongoClient(host='localhost', port=27017,
                        document_class=dict, tz_aware=True, connect=True, maxPoolSize=None, minPoolSize=100,
                        connectTimeoutMS=60000, waitQueueMultiple=None, retryWrites=True)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
except ConnectionFailure as cf:
    dbg.exception("""
    = = = = = Guide = = = = =
    1. Run MongoDB :
        mongod --dbpath /usr/local/var/mongodb
        or
        mongod --config /usr/local/etc/mongod.conf
    """, __name__)
    dbg.printer(locals(), console=True)
    raise
else:
    dbg.printer(f"{'+'*50} {__name__}\n{client}", console=True)
# ============================================================
# try:
#     os.environ['MONGO_DBNAME']
# except Exception as e:
#     dbg.exception("""
#         = = = = = Guide = = = = =
#         Setup below in the terminal :
#             export MONGO_DBNAME=project_name (For Terminal)
#             %env MONGO_DBNAME=project_name (For Jupyter notebook)
#     """, __name__)
#     raise
# else:
#     db = client[os.environ['MONGO_DBNAME']]
#     dbg.printer(f"{'+'*50} {__name__}\n{db}", console=True)
