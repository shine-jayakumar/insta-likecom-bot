""" 
    applogger.py - class to maintain logs

    insta-likecom-bot v.3.0.5
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
import sys
from modules.constants import LOGS_DIR
from colorama import init as colorama_init
from colorama import Fore, Style


colorama_init(autoreset=True)


class ColoredFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._level_colors = {
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "DEBUG": Fore.BLUE
            # "INFO": Fore.WHITE,
            # "CRITICAL": Fore.RED + Style.BRIGHT
        }
    
    def format(self, record):
        color = self._level_colors.get(record.levelname, "")
        if not color:
            return logging.Formatter.format(self, record)
        
        record.name = color + record.name
        record.levelname = color + record.levelname
        record.msg = color + record.msg
        return logging.Formatter.format(self, record)
    

class AppLogger:

    def __init__(self, name):

        # ====================================================
        # Setting up logger
        # ====================================================
        self.logdir = LOGS_DIR
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists(self.logdir):
            os.mkdir(self.logdir)

        logfname = os.path.join(self.logdir, f'ilcbot_{datetime.now().strftime("%Y_%m_%d")}.log')

        formatter = logging.Formatter("[%(asctime)s]:[%(name)s]:[%(funcName)s:%(lineno)s]:[%(levelname)s]:%(message)s")
        file_handler = TimedRotatingFileHandler(logfname, when='midnight')
        file_handler.setFormatter(formatter)

        stdout_formatter = ColoredFormatter("[*] => %(message)s")
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(stdout_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stdout_handler)
    
    def getlogger(self):
        """
        Returns the logger object
        """
        return self.logger


if __name__ == '__main__':
    pass