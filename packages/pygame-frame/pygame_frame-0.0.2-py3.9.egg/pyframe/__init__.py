__version__ = "0.0.2"
try :
    import pyframe.constants as constants
    import pyframe.functions as functions
    import pyframe.classes as classes
    import pyframe.exception as exception
except :
    print("PYFRAME ERROR: Impossible d'importer correctement la lib")