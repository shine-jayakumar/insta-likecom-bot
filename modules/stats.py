""" 
    stats.py - Stats class to keep track of activity

    insta-likecom-bot v.3.0.6
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

from datetime import datetime
import json
import os
import sys
from threading import Thread
import signal
from modules.exceptions import LimitsExceededError
from modules.applogger import AppLogger


logger = AppLogger('Stats').getlogger()


class Stats:    

    def __init__(self, limits: dict):

        self.accounts: int = 0
        self.private_accounts: int = 0

        # post
        self.likes: int = 0 
        self.comments: int = 0
        self.comment_likes: int = 0
        
        # stories
        self.stories: int = 0
        self.story_likes: int = 0
        self.story_comments: int = 0

        # reels
        self.reels: int = 0       
        self.reel_likes: int = 0
        self.reel_comments: int = 0
        self.reel_comment_likes: int = 0

        self.tref = datetime.now().timestamp()

        self.limits = limits
        self.session_st = datetime.now().timestamp()

        self._init()
        self._init_statsmon()

    def _init(self) -> None:
        """
        Creates stats directory if doesn't exist
        """
        statsdir = 'stats'
        if not os.path.exists(statsdir):
            os.mkdir(statsdir)

        fpath = os.path.join(statsdir, f'{datetime.now().strftime("%Y_%m_%d")}.json')
        if os.path.exists(fpath):
            with open(fpath) as limits_fh:
                limits = json.load(limits_fh)
                for k,v in limits.items():
                    setattr(self, k, v)
            return
        
        self.save()
    
    def save(self) -> None:
        """
        Saves current stats to file
        """
        fpath = os.path.join('stats', f'{datetime.now().strftime("%Y_%m_%d")}.json')
        with open(fpath, 'w') as json_fh:
            exclude_keys = ['limits', 'session_st']
            stats_vars = {k:v for k,v in vars(self).items() if k not in exclude_keys}
            json.dump(stats_vars, json_fh)
    
    def _update_tref(self) -> None:
        """
        Updates the time reference
        """
        self.tref = datetime.now().timestamp()
    
    def _witin_limits(self, limits: dict) -> bool:
        """
        Checks if actions are within limits
        """
        for action, limit in limits.items():
            cur_val = getattr(self, action)
            if cur_val > limit:
                return False
        return True
            
    def _init_statsmon(self):
        """
        Monitors stats
        """
        if os.name == 'nt':
            signal.signal(signal.SIGABRT, handler=self._sighandler)
        else:
            signal.signal(signal.SIGUSR1, handler=self._sighandler)
        thread = Thread(target=self._stasmon, daemon=True)
        thread.start()

    def _stasmon(self):
        """
        Initiates stats monitor
        """
        SIGRAISED = False

        def raisesig():
            nonlocal SIGRAISED
            if not SIGRAISED:
                if os.name == 'nt':
                    signal.raise_signal(signal.SIGABRT)
                else:
                    signal.raise_signal(signal.SIGUSR1)
                SIGRAISED = True

        while True:
            cur_ts = datetime.now().timestamp()

            # session timeout
            if all([
                self.limits.get('session_timeout', -1) > 0,
                cur_ts - self.session_st > self.limits.get('session_timeout', -1)
                ]):
                raisesig()
                break

            # check daily limits
            if not self._witin_limits(limits=self.limits['daily']):
                raisesig()
                break

            # check hourly limits
            if cur_ts - self.tref < 3600:
                if not self._witin_limits(limits=self.limits['hourly']):
                    raisesig()                
                    break
            else:
                self._update_tref()
                self.save()
    
    def _sighandler(self, signum, frame):
        """ Signal handler """
        self.save()
        logger.error(f'{LimitsExceededError.__name__}: One of the actions has exceeded the daily/hourly limit')
        sys.exit()

    def log(self):
        """ Logs the current stats """
        exclude_keys = ['limits', 'session_st']
        stats_vars = {k:v for k,v in vars(self).items() if k not in exclude_keys}
        for k,v in stats_vars.items():
            logger.info(f'[{k}]: {v}')
    
    def __str__(self):
        exclude_keys = ['limits','tref']
        stats_vars = {k:v for k,v in vars(self).items() if k not in exclude_keys}
        stats = '--------------- Stats -----------------\n'
        for k,v in stats_vars.items():
            stats += f'{k:<22}: {v}' + '\n'
        stats += '--------------------------------------'
        return stats


if __name__ == '__main__':
    pass




    


