import importlib, os, time, argparse, sys

# TARCHs path
PATH = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(1, PATH)

import dataUtils as dut

DataModule = dut.DataModule

parser = argparse.ArgumentParser(description='Tardigrade Architecture Data Processing (TARCH)')
parser.add_argument('-nd', '--no-drop', type=str, action='append', default=None,
                    choices=dut.dataDropKey.keys(),
                    help='type of data to prevent dropping (default: %(default)s)')

parser.add_argument('-ll', '--logging-level', type=str, action='store', default="INFO",
                    choices=["NONE", "DEBUG", "INFO", "WARNING", "DATADROP", "ERROR", "CRITICAL"],
                    help='what types of messages should be logged to console (default: %(default)s)')

parser.add_argument('--file-logging-level', type=str, action='store', default="DEBUG",
                    choices=["NONE", "DEBUG", "INFO", "WARNING", "DATADROP", "ERROR", "CRITICAL"],
                    help='what types of messages should be logged to log file (default: %(default)s)')

parser.add_argument('--log-file', const=str, action='store_const', default="tarch.log",
                    help='file to log to (default: %(default)s)')



def fullSplitPath(path):
    """
    :param path: relative path (eg. "./hello/also here/file")
    :type path: str

    :returns: ["hello", "also here", "file"]
    :rtype: list
    """
    pathList = []
    splitPath = os.path.split(path)
    if splitPath[0] == ".":
        return splitPath[1]
    subs = fullSplitPath(splitPath[0])
    pathList.extend([subs] if isinstance(subs, str) else subs)
    pathList.append(splitPath[1])
    return pathList


def getDataModules(path):
    """
    :param path:
    :type path: str

    :returns: list of tuples of imported data modules
    """
    modules = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if "__pycache__" in root:
                continue
            try:
                if ".py" in file:
                    moduleImportString = "modules."+file.replace(".py", "")
                    module = importlib.import_module(moduleImportString)
                    try:
                        try:
                            module = module.exportedClass()
                        except TypeError as e:
                            dut.l.critical(f"Error importing module {module}")
                            dut.l.critical(e)
                            dut.l.critical("Exiting...")
                            exit(1)
                        modules.append(module)
                    except AttributeError:
                        pass
            except Exception as e:
                raise e
    return list(filter(lambda m: m.run, modules))  # remove modules with run set to false


def toposort(dependencyTopology):
    """
    toposort (dict): dictonary of objects and tuples of mutual dependencies on said objects
    returns:
        list of objects sorted by dependency such that dependencies are satisfied in order [0]=>[n]
    """

    orderedModules = []
    while len(dependencyTopology.keys()) > 0:
        # get node with no dependencies (node with in-degree 0)
        for module, dependencies in dependencyTopology.items():
            if dependencies == ():
                # remove node
                orderedModules.append(module)
                dependencyTopology.pop(module)
                break
        else:
            raise Exception("Invalid dependency structure found in modules, no correct execution scheme can be "
                            "identified.")
        # update unsatisfied dependencies
        for module, dependencies in dependencyTopology.items():
            dependencyTopology[module] = tuple(d for d in dependencies if not d == orderedModules[-1])
    return orderedModules


def sortDataModules(unsortedModules):
    """
    unsortedModules (list): list of tuples of objects and tuple of dependencies (eg. as given by getDataModules)

    returns:
        list of objects sorted by dependencies such that if executed in orhttps://clockify.me/projectsder (list[0]=>list[n]) all dependencies are satisfied
    exception ??:
        no possible ordering satisfies dependency tree
    """
    dependencyTopology = {}
    for module in unsortedModules:
        dependencyTopology[module.name()] = module.depends
    order = toposort(dependencyTopology)
    return [{module.name(): module for module in unsortedModules}[name] for name in order]


class MasterFrameClass():
    def __init__(self):
        self.frames = []
        self.frameNames = []

    def storeComponent(self, data, generator, source):
        self.addNewFrame(generator, data)

    def getFrame(self, framename):
        try:
            return self.frames[self.frameNames.index(framename)]
        except ValueError as e:
            if framename not in self.frameNames:
                dut.l.critical(f"Frame {framename} doesn't exist.")
            raise e

    def updateFrame(self, framename, updatedFrame):
        self.frames[self.frameNames.index(framename)] = updatedFrame

    def export(self, path):
        # TODO: write this,, better.
        for key in self.frameNames:
            with open(os.path.join(path, key + ".csv"), "w") as f:
                f.write(self.frames[self.frameNames.index(key)].to_csv())

    def addNewFrame(self, frameName, frame):
        self.frames.append(frame.copy())
        self.frameNames.append(frameName)

if __name__ == "__main__":
    CWD = os.getcwd()
    sys.path.insert(1, CWD)
    args = parser.parse_args()
    dut.logFilename = dut.getFile(args.log_file)
    if args.no_drop is not None:
        dut.ignoreDrop = args.no_drop # implement arg actions

    dut.l.info("Loading Modules...")

    dataModules = getDataModules(CWD+"/modules")
    dataModules = sortDataModules(dataModules)

    MasterFrame = MasterFrameClass()
    for dataModule in dataModules:
        timeStart = time.time()
        dut.l.info("Running {0}...".format(dataModule.name()))
        dataModule.importData(MasterFrame)
        #dataModule.setCheckpoint()
        dataModule.prepareData()
        #dataModule.logChanges()
        dataModule.annotateData()
        dataModule.mergeData(MasterFrame)
        MasterFrame.storeComponent(dataModule.data, generator=dataModule.name(), source=dataModule.source())
        dut.l.info("{} finished! (took {}ms)".format(dataModule.name(), round(1000 * (time.time() - timeStart))))

    dut.l.info("Exporting data...")
    if not os.path.exists(CWD+"/exports"):
        os.mkdir("exports")
    MasterFrame.export(CWD+"/exports")
    dut.l.info("All done! Exiting...")
