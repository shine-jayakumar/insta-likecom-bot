# profile.py
# Profile class to parse and hold credentials and settings

import json
import os
from modules.applogger import AppLogger
from instafunc import (
    parse_inlast, parse_targets_multi, 
    parse_delay, is_hashtag_present,
    load_comments, load_matchtags)

from typing import Dict, List


logger = AppLogger('profile').getlogger()


def to_int(val, field:str = '') -> int:
    """ Returns val as int """
    if not val:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str) and val.isnumeric():
        return int(val)
    raise TypeError(f"Invalid value for {field}")


def to_list(val, splitby: str = '') -> List:
    """ Returns val as list """
    if isinstance(val, list):
        return val
    if splitby and isinstance(val, str):
        return val.split(splitby)
    return list(val)


def defaultval(val, default=None):
    """ Returns default value in absence of val """
    return val if val else default


class Profile:

    def __init__(self, args = None, profile_path: str = '') -> None:
        
        if not any([args, profile_path]):
            raise Exception('Profile path or parsed argument parameter is required')
        
        self.args = vars(args)
        self.profileargs = self.load_profile(profile_path)

        if not self.profileargs:
            raise Exception('Invalid profile file')

        self.username: str  = ''
        self.password = ''
        self.target: List[str] = []

        self.numofposts: int = None
        self.postscript: str = ''
        
        self.findfollowers: bool = None
        self.followersamount: int = None

        self.likecomments: int = None
        
        self.inlast: str = ''

        self.viewstory: bool = None
        self.likestory: int = float('inf')
        self.commentstory: int = float('inf')
        self.onlystory: bool = None

        self.mostrecent: bool = None
        self.reloadrepeat: int = None

        self.matchtags: List[str] = []
        self.ignoretags: List[str] = []
        self.matchtagnum: int = 3
        self.matchalltags: bool = None

        self.comments: List[str] = []
        self.onecomment: str = ''
        self.nocomments: bool = None

        self.brprofile: str = None
        self.eltimeout: int = None
        self.delay: str = None

        self.browser: str = 'chrome'
        self.headless: bool = None

        self.profile: str = ''
       
    def load_profile(self, path: str) -> Dict:
        """
        Reads profile and loads variables
        """        
        try:       
            profile = {}   
            with open(path) as fh:
                profile = json.load(fh)
            if not profile:
                raise Exception('Invalid profile file')
            return profile
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} - {str(ex)}')
            return {}

    def load_credentials(self) -> None:
        """
        Loads credentials from parsed arguments or profile file
        """
        if self.profile:
            self.username = self.profile.get('username', None)
            self.password = self.profile.get('password', None)
        else:
            self.username = self.args.username
            self.password = self.args.password

        if not all([self.username, self.password]):
            raise Exception('Username and Password parameter cannot be blank')
    
    def load_target(self) -> None:
        """
        Loads targets from profile path or parsed arguments
        """
        if self.profile:
            self.target = parse_targets_multi(targetlist=self.profile.target)
        else:
            self.target = parse_targets_multi(targetlist=self.args.target)
        if not self.target:
            raise Exception('Target cannot be blank')
    
    def load_numposts(self) -> None:
        """
        Loads number of posts
        """
        if self.profile:
            self.numofposts = to_int(self.profile.get('numofposts', None))
        else:
            self.numofposts = self.args.numofposts

    def load_postscript(self) -> None:
        """
        Loads postscript
        """
        if self.profile:
            self.postscript = self.profile.get('postscript', None)
        else:
            self.postscript = self.args.postscript
    
    def load_findfollowers(self) -> None:
        """ Loads findfollowers """

        def is_hashtag_present(targets: List):
            for target in targets:
                if target.startswith('#'):
                    return True
            return False
        
        if self.profile:
            self.findfollowers = self.profile.get('findfollowers', None)
        else:
            self.findfollowers = self.args.findfollowers
        if self.findfollowers and is_hashtag_present(self.target):
            raise Exception("Cannot use 'findfollowers' option with tags")
    
    def load_followersamount(self) -> None:
        """ Loads followersamount """
        if self.profile:
            self.followersamount = to_int(self.profile.get('followersamount', None))
        else:
            self.followersamount = self.args.followersamount

    def load_likecomments(self) -> None:
        """ Loads likecomments """
        if self.profile:
            self.likecomments = to_int(self.profile.get('likecomments', None))
        else:
            self.likecomments = self.args.likecomments
    
    def load_inlast(self) -> None:
        """ Loads inlast filter """
        if self.profile:
            self.inlast = self.profile.get('inlast', '')
        else:
            self.inlast = self.args.inlast
    
    def load_viewstory(self) -> None:
        """ Loads viewstory """
        if self.profile:
            self.viewstory = self.profile.get('viewstory', None)
        else:
            self.viewstory = self.args.viewstory

    def load_likestory(self) -> None:
        """ Loads likestory """
        if self.profile:
            self.likestory = to_int(self.profile.get('likestory', None))
        else:
            self.likestory = self.args.likestory

    def load_commentstory(self) -> None:
        """ Loads commentstory """
        if self.profile:
            self.commentstory = to_int(self.profile.get('commentstory', None))
        else:
            self.commentstory = self.args.commentstory
    
    def load_onlystory(self) -> None:
        """ Loads onlystory """
        if self.profile:
            self.onlystory = self.profile.get('onlystory', None)
        else:
            self.onlystory = self.args.onlystory
    
    def load_mostrecent(self) -> None:
        """ Loads mostrecent """
        if self.profile:
            self.mostrecent = self.profile.get('mostrecent', None)
        else:
            self.mostrecent = self.args.mostrecent
    
    def load_reloadrepeat(self) -> None:
        """ Loads reloadrepeat """
        if self.profile:
            self.reloadrepeat = to_int(self.profile.get('reloadrepeat', None))
        else:
            self.reloadrepeat = self.args.reloadrepeat

    def load_matchtags(self) -> None:
        """ Loads matchtags """
        if self.profile:
            self.matchtags = to_list(self.profile.get('matchtags', ''), splitby=',')
        else:
            self.matchtags = load_matchtags(self.args.matchtags)\
                  if self.args.matchtags else None            
    
    def load_matchtagnum(self) -> None:
        """ Loads matchtagnum """
        if self.profile:
            self.matchtagnum = to_int(self.profile.get('matchtagnum', 3))
        else:
            self.matchtagnum = self.args.matchtagnum if \
                self.args.matchtagnum else 3
    
    def load_matchalltags(self) -> None:
        """ Loads matchalltags """
        if self.profile:
            if self.matchtagnum:
                raise Exception("'matchtagnum' and 'matchtagall' cannot be used together")
            self.matchalltags = self.profile.get('matchalltags', None)
        else:
            self.matchalltags = self.args.matchalltags
    
    def load_comments(self) -> None:
        """ Loads comments """
        if self.profile:
            self.comments = to_list(self.profile.get('comments', ''))
        else:
            self.comments = self.args.comments
        if self.comments:
            self.comments = load_comments(self.comments)
    
    def load_onecomment(self) -> None:
        """ Loads onecomment """
        if self.profile:
            self.onecomment = self.profile.get('onecomment', '')
        else:
            self.onecomment = self.args.onecomment
    
    def load_nocomments(self) -> None:
        """ Loads nocomments """
        if self.profile:
            if self.onecomment:
                raise Exception("'onecomment' cannot be used with 'nocomments'")
            if self.comments:
                raise Exception("'comments' cannot be used with 'nocomments'")
            self.nocomments = self.profile.get('nocomments', None)
        else:
            self.nocomments = self.args.nocomments
    



    
    
    

    


        

        




