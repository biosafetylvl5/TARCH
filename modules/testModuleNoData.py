"""
name: TestModuleNoData
author: Gwyn Uttmark
production: False

docstring: This module is for testing, it imports no data and performs no operations.
"""

try:
    from . import dataUtils as dut
except ImportError:
    import dataUtils as dut


class TestClass(dut.DataModule):
    def __init__(self):
        super().__init__()
        self.depends = ()
        self.run = False

    @staticmethod
    def name():
        return "TestModule"

    @staticmethod
    def source():
        return None

    @staticmethod
    def productionReady():
        return None

    def importData(self):
        pass

    def prepareData(self):
        pass

    def describeData(self):
        pass

    def annotateData(self):
        pass

    def mergeData(self, MasterFrame):
        pass


exportedClass = TestClass
