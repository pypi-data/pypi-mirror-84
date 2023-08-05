# -*- coding: utf-8 -*-
"""
Automatic-Setup UnitTest Environment.
"""
# print(f"{'@'*50} {__name__}")
import os
import sys
# import pprint
# pp = pprint.PrettyPrinter(indent=2)
# ============================================================
os.environ['PJTS_PATH'] = f"{os.environ['HOME']}/pjts"
PJT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['KR_TZONE'] = '9'
# ============================================================
# for i, k in enumerate(sorted(os.environ), start=1):
#     print(f"{'-'*50} {i}/{len(os.environ)}")
#     print(f"{k} : {os.environ[k]}")
# ============================================================
pkgs = ['ipy']
for p in pkgs:
    sys.path.append(f"{os.environ['PJTS_PATH']}/{p}")
