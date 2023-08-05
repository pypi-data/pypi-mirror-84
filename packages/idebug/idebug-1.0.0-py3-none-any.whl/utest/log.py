# print(f"{'@'*50} {__name__}")
from utest import testenv
# ============================================================ Python.
import unittest
import os
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=2)
import logging
from importlib import reload
# ============================================================ External-Library.
import pandas as pd
# ============================================================ My-Library.
# ============================================================ Project.
import idebug as dbg
# ============================================================ Constant.


class TestModel:
    def __init__(self):
        print(__class__)
        self.df = pd.DataFrame()
    def __str__(self):
        return f"__name__ : {__name__}"



class TestCase(unittest.TestCase):

    @dbg.utest
    def test01__console(self):
        dbg.console({'a':1, 'b':2})
        dbg.console(f"{'*'*50} {__name__}.test01__console")

    @dbg.utest
    def test02__loop(self):
        len = 30
        for i in range(1,31):
            var = f"fuck{i}."
            dbg.loop(i, len, var, __name__, linetype='-')

    @dbg.utest
    def test03__print_dict(self):
        a = 1
        b = 2
        df = pd.DataFrame()
        dbg.print_dict(locals())

    @dbg.utest
    def test04__printer(self):
        a = 1
        b = 2
        df = pd.DataFrame()
        dbg.printer(locals())
        dbg.printer(f"\n\n non dict values")

    @dbg.utest
    def test05__exception(self):
        a = {'A':1, 'B':2}
        b = 2
        df = pd.DataFrame()
        dbg.exception(locals(), __name__)


# ============================================================
"""실행."""
# ============================================================
if __name__ == "__main__":
    unittest.main(module='__main__',
                defaultTest=None,
                argv=None,
                testRunner=None,
                testLoader=unittest.defaultTestLoader,
                exit=True,
                verbosity=2,
                failfast=None,
                catchbreak=None,
                buffer=None,
                warnings=None)
