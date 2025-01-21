from datetime import datetime
from colorama import Fore, Back, Style

from classes import singleton
from enum import Enum

class LogLevel(Enum):
    ERROR = 1
    WARNING = 2
    DEBUG = 3
    INFO = 4

def cyan(text):
    print(Fore.CYAN + text + Fore.RESET)

def yellow(text):
    print(Fore.YELLOW + text + Fore.RESET)

def orange(text):
    print(Fore.LIGHTRED_EX + text + Fore.RESET)

def red(text):
    print(Fore.RED + text + Fore.RESET)


level_to_color = {
    LogLevel.ERROR: red,
    LogLevel.WARNING: orange,
    LogLevel.DEBUG: yellow,
    LogLevel.INFO: cyan
}

log_level = LogLevel.INFO


@singleton
class Logger:
    def log(self, level, message):
        message = "{}: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M"), message)
        if level in level_to_color:
            level_to_color[level](message)
        else:
            print(message)

    def error(self, message):
        if log_level.value >= LogLevel.ERROR.value:
            self.log(LogLevel.ERROR, message)

    def warning(self, message):
        if log_level.value >= LogLevel.WARNING.value:
            self.log(LogLevel.WARNING, message)

    def debug(self, message):
        if log_level.value >= LogLevel.DEBUG.value:
            self.log(LogLevel.DEBUG, message)

    def info(self, message):
        if log_level.value >= LogLevel.INFO.value:
            self.log(LogLevel.INFO, message)
