"""
name: TestModuleNoData
author: Gwyn Uttmark
production: False

docstring: This module is for testing, it imports no data and performs no operations.
"""

try:
    from tarch import datamodule
    from main import dut
except ImportError:
    import sys
    sys.path.insert(1, "./../../")
    from main import DataModule
    from main import dut


import pandas as pd

class TestClass(DataModule):
    def __init__(self):
        super().__init__()
        self.depends = ()
        self.run = True
        self.l = dut.getLogger(self)

    @staticmethod
    def name():
        return "TestModule"

    @staticmethod
    def source():
        return None

    @staticmethod
    def productionReady():
        return None

    def importData(self, MasterFrame):
        self.l.info("'Importing' data... (jk, this is just a test)")

    def prepareData(self):
        self.data = pd.DataFrame(["this is a TEST!!"])

    def describeData(self):
        pass

    def annotateData(self):
        pass

    def mergeData(self, MasterFrame):
        pass


exportedClass = TestClass
