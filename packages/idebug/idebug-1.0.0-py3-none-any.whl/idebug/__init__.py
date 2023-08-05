# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
# ============================================================ PackageInspector.
try:
    os.environ['LOG_PATH']
except Exception as e:
    print(f"""
        Read README.md
        You must setup LOG_PATH.
        {e}
    """)
    raise
# ============================================================ Temp.
from idebug import pkgs
# ============================================================ APIs.
# from idebug.console import clsattrs, clsdict, Loop, Looper, printfuncinit, fruntime, utestfunc, objsize, printdf, printiter, printexcep
from idebug.log import *
from idebug import log
# from idebug.DataStructure import *
# from idebug.html import *
# from idebug.iinspect import *
# from idebug.mongo import *
# from idebug.performance import Function
