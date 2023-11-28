""" 
    applogger.py - class to maintain logs

    insta-likecom-bot v.3.0.3
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


class AppLogger:

    def __init__(self, name):

        # ====================================================
        # Setting up logger
        # ====================================================
        self.logdir = 'logs'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not os.path.exists(self.logdir):
            os.mkdir(self.logdir)

        logfname = os.path.join(self.logdir, f'ilcbot_{datetime.now().strftime("%Y_%m_%d")}.log')

        formatter = logging.Formatter("[%(asctime)s]:[%(name)s]:[%(funcName)s:%(lineno)s]:[%(levelname)s]:%(message)s")
        file_handler = TimedRotatingFileHandler(logfname, when='midnight')
        file_handler.setFormatter(formatter)

        stdout_formatter = logging.Formatter("[*] => %(message)s")
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(stdout_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stdout_handler)
    
    def getlogger(self):
        """
        Returns the logger object
        """
        return self.logger
