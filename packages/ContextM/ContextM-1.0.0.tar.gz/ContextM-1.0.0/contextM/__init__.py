### IMPORTS                     ###
    ## Dependencies                 ##
import decorate_all_methods
    ## Dependencies                 ##
import abc
### IMPORTS                     ###
### CONSTANTS                   ###
class _:
    """ Do Not Disturb """
    def __init__(self):
        assert __name__ == "__main__", "Access Denied" as Exception
        self.EXCLUDE = ['__init__']
### CONSTANTS                   ###
### CLASSES                     ###
@decorate_all_methods.decorate_all_methods(abc.abstractmethod, [_().EXCLUDE])
class ContextManager(abc.ABC):
    """
    The base contextM class for creating Context Managers
    """
    def __init__(self, *a, **kw): NotImplemented
    def __enter__(self): raise NotImplementedError
    def __exit__(self, *args, **kwargs): raise NotImplementedError
### CLASSES                     ###