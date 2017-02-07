import datetime

from lib.Configuration import Configuration

CONFIG = Configuration()

def getInstance():
    return LoggerSingleton()

class LoggerSingleton:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """
            
        def __init__(self):
            self.path = CONFIG.get_LoggingPath()

        def log(self, message, level):
            time_str = str(datetime.datetime.now()).split(" ")
            path = self.path + "logfile-" + time_str[0] + ".log"
            with open(path, 'a') as f:
                f.write('[' + level + '][' + time_str[1] + '] ' + message + '\n')

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if LoggerSingleton.__instance is None:
            # Create and remember instance
            LoggerSingleton.__instance = LoggerSingleton.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_LoggerSingleton__instance'] = LoggerSingleton.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
