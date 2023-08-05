# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
import inspect
# ============================================================ ExternalPackages.
import pandas as pd
# ============================================================ MyPackages.
import idebug as dbg
# ============================================================ IntraPackage.
# ============================================================ Constant.

# ============================================================
"""DataHandler."""
# ============================================================
@dbg.fruntime
def backup_tbl(tbl, filepath):
    try:
        os.makedirs(os.path.dirname(filepath))
    except Exception as e:
        pass
    dbg.printer(f"filepath : {filepath}")
    cursor = tbl.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv(filepath, index=False)#, columns=self.dataschema
