""" 
    profile.py - Profile class

    insta-likecom-bot v.3.0.5
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

import json
from modules.applogger import AppLogger
from modules.exceptions import *
from modules.constants import COMMENTS
from typing import List, Tuple
import re
from os.path import exists as pathexists


logger = AppLogger('profile').getlogger()


class Profile:
    """
    Profile class to parse command-line arguments and
    arguments in profile json file
    """

    def dupargs_validator(func):
        """
        Duplicate argument validator
        """
        def validator(self, *args, **kwargs):
            profileargs = func(self, *args, **kwargs)
            if profileargs:
                dupargs = []
                for arg, val in profileargs.items():
                    arg_in_cmdargs = self.args.get(arg, None)
                    if val and arg_in_cmdargs and arg_in_cmdargs != val:
                        dupargs.append(arg)
                if dupargs:
                    raise DuplicateArgumentError(f'Duplicate instances of arguments: {dupargs}')
            return profileargs
        return validator
    
    def __init__(self, args = None) -> None:
        """
        Loads arguments from command-line arguments and profile json file
        and create a profile
        """        
        if not args:
            raise Exception('Argument parameter is required')
        
        self.args = vars(args)
        self.profileargs = self._load_profile(self.args.get('profile',''))
        self._load_params()
        self._init_args()

        if not all([self.username, self.password, self.target]):
            raise MandatoryParamsMissingError('Manadatory params - username, password, target missing')

        if self.findfollowers and is_hashtag_present(self.target):
            raise ConflictingParamsError(f"'findfollowers' cannot be used with hashtags")
       
    @dupargs_validator
    def _load_profile(self, path: str) -> dict:
        """
        Reads profile and loads variables
        """        
        if not path:
            return {}
        profile = {}
        try:       
            with open(path) as fh:
                profile = json.load(fh)
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} - {str(ex)}')

        if not profile:
            raise InvalidProfileFileError(f'Invalid profile file - {path}')
        
        return profile
    
    def _load_params(self) -> None:
        if self.args:
            for param, value in self.args.items():
                setattr(self, param, value)

        if self.profileargs:
            for param, value in self.profileargs.items():
                setattr(self, param, value)

    def _init_args(self) -> None:
        """ Runs methods to initialize args """
        args = list(self.args.keys())
        args = [arg for arg in args if arg not in ('profile', 'username', 'password')]
        for arg in args:
            parser_func = getattr(self, f'_parse_{arg}', None)
            if parser_func:
                parser_func()

        self.__dict__.pop('args', None)
        self.__dict__.pop('profileargs', None)

    def _parse_target(self) -> None:
        """ Loads target """
        if self.target:
            if isinstance(self.target, str):
                # get targets from file if --target arg contains a file path
                targets_from_file = parse_targets_multi(fname=self.target)
                self.target = targets_from_file if targets_from_file else [self.target]
            elif isinstance(self.target, list):
                self.target: List[str] = [str(target).strip() for target in self.target if target]

    def _parse_numofposts(self) -> None:
        """ Parses numofposts """
        if self.numofposts:
            self.numofposts: int = to_int(self.numofposts, 'numofposts')
    
    def _parse_postscript(self) -> None:
        """ Loads postscript """
        if self.postscript:
            self.postscript = str(self.postscript)
    
    def _parse_findfollowers(self) -> None:
        """ Parses findfollowers """
        if self.findfollowers:
            self.findfollowers: bool = True
    
    def _parse_followersamount(self) -> None:
        """ Parses followersamount """
        if self.followersamount:
            self.followersamount: int = to_int(self.followersamount, 'followersamount')
    
    def _parse_viewstory(self) -> None:
        """ Parses viewstory """
        if self.viewstory:
            self.viewstory: bool = True
    
    def _parse_likestory(self) -> None:
        """ Parses likestory """
        if self.likestory:
            self.likestory: int = to_int(self.likestory, 'likestory')
        else:
            self.likestory = 0
    
    def _parse_commentstory(self) -> None:
        """ Parses commentstory """
        if self.commentstory:
            self.commentstory: int = to_int(self.commentstory, 'commentstory')
        else:
            self.commentstory = 0

    def _parse_onlystory(self) -> None:
        """ Parses onlystory """
        if self.onlystory:
            self.onlystory: bool = True
    
    def _parse_skipcommented(self) -> None:
        """ Parses skipcommented """
        if self.skipcommented:
            self.skipcommented: bool = True
    
    def _parse_comments(self) -> None:
        """ Loads comments """
        if self.comments:
            if isinstance(self.comments, str):
                self.comments: List[str] = load_comments(self.comments)
            elif isinstance(self.comments, list):
                self.comments: List[str] = [str(cmt).strip() for cmt in self.comments]
        else:
            self.comments: List[str] = COMMENTS
    
    def _parse_onecomment(self) -> None:
        """ Loads onecomment """
        if self.onecomment:
            self.onecomment = str(self.onecomment)

    def _parse_nocomments(self) -> None:
        """ Loads nocomments """
        if self.nocomments:
            self.nocomments: bool = True
    
    def _parse_matchtags(self) -> None:
        """ Load matchtags """
        if self.matchtags:
            if isinstance(self.matchtags, str):
                tags_from_file = load_tags(self.matchtags)
                if tags_from_file:
                    self.matchtags: List[str] = tags_from_file
                else:
                    self.matchtags = [self.matchtags]
            elif isinstance(self.matchtags, list):
                self.matchtags = [str(tag).strip() for tag in self.matchtags]
        else:
            self.matchtags: List[str] = []
    
    def _parse_ignoretags(self) -> None:
        """ Loads ignoretags """
        if self.ignoretags:
            if isinstance(self.ignoretags, str):
                tags_from_file = load_tags(self.ignoretags)
                if tags_from_file:
                    self.ignoretags: List[str] = tags_from_file
                else:
                    self.ignoretags = [self.ignoretags]
            elif isinstance(self.ignoretags, list):
                self.ignoretags: List[str] = [str(tag).strip() for tag in self.ignoretags]
        else:
            self.ignoretags: List[str] = []

    def _parse_matchtagnum(self) -> None:
        """ Loads matchtagnum """
        if self.matchtagnum:
            self.matchtagnum: int = to_int(self.matchtagnum, 'matchtagnum')
            if self.matchtags and self.matchtagnum > len(self.matchtags):
                raise ValueError("'matchtagnum' cannot be greater than number of matchtags")
        if self.matchalltags:
            self.matchtagnum: int = len(self.matchtags)
        else:
            self.matchtagnum: int = 3
    
    def _parse_matchalltags(self) -> None:
        """ Loads matchalltags """
        if self.matchalltags:
            self.matchalltags: bool = True

    def _parse_likecomments(self) -> None:
        """ Loads likecomments """
        if self.likecomments:
            self.likecomments: int = to_int(self.likecomments, 'likecomments')
    
    def _parse_mostrecent(self) -> None:
        """ Loads mostrecent """
        if self.mostrecent:
            self.mostrecent: bool = True
    
    def _parse_reloadrepeat(self) -> None:
        """ Loads reloadrepeat """
        if self.reloadrepeat:
            self.reloadrepeat: int = to_int(self.reloadrepeat, 'reloadrepeat')
        
    def _parse_inlast(self) -> None:
        """ Loads inlast """
        if self.inlast:
            self.inlast_multiplier: int = None
            self.inlast_tparam: str = None
            parsed_inlast = parse_inlast(self.inlast)
            if not parsed_inlast:
                raise ValueError(f"Invalid value '{self.inlast}' received for 'inlast' parameter")
            self.inlast_multiplier, self.inlast_tparam = parsed_inlast
    
    def _parse_onlyreels(self) -> None:
        """ Parses onlyreels """
        if self.onlyreels:
            self.onlyreels: bool = True

    def _parse_numofreels(self) -> None:
        """ Loads numofreels """
        if self.numofreels:
            self.numofreels: int = to_int(self.numofreels, 'numofreels')
    
    def _parse_noreelcomments(self) -> None:
        """ Loads noreelcomments """
        if self.noreelcomments:
            self.noreelcomments: bool = True
    
    def _parse_likereelcomments(self) -> None:
        """ Loads likereelcomments """
        if self.likereelcomments:
            self.likereelcomments: int = to_int(self.likereelcomments, 'likereelcomments')
    
    def _parse_limits(self) -> None:
        """ Loads limits from json file """
        if self.limits:
            try:
                with open(self.limits) as fh:
                    limits = json.load(fh)
                    if any([not limits.get('daily', None), not limits.get('hourly', None)]):
                        raise InvalidLimitsFileError('Invalid Limits file received')
                    self.limits = limits
            except json.JSONDecodeError:
                raise InvalidLimitsFileError('Invalid Limits file received')
        else:
            raise LimitsFileMissingError('Limits file is missing. Use --limits file.json to specify a limits file.')

    def _parse_brprofile(self) -> None:
        """ Loads brprofile """
        if self.brprofile and not pathexists(self.brprofile):
            raise InvalidBrowserProfileError(f"Invalid browser profile - {self.brprofile}")

    def _parse_eltimeout(self) -> None:
        """ Loads eltimeout """
        if self.eltimeout:
            self.eltimeout: int = to_int(self.eltimeout, 'eltimeout')
        else:
            self.eltimeout: int = 30
    
    def _parse_delay(self) -> None:
        """ Parses delay """
        if self.delay:
            self.delay: Tuple[int] = parse_delay(self.delay)
        else:
            self.delay: Tuple[int] = (1,10)
    
    def _parse_browser(self) -> None:
        """ Parses browser """
        if self.browser:
            if self.browser.lower() not in ('chrome', 'firefox'):
                raise InvalidBrowserError("Invalid browser specified in 'browser' parameter")
            self.browser = self.browser.lower()
        else:
            self.browser = 'chrome'
    
    def _parse_headless(self) -> None:
        """ Parses headless """
        if self.headless:
            self.headless: bool = True
    

def remove_blanks(lst: List) -> List:
    """
    Removes empty elements from a list
    """
    return [el for el in lst if el != '']


def remove_carriage_ret(lst) -> List:
    """
    Remove carriage return - \r from a list
    """
    return list(map(lambda el: el.replace('\r',''), lst))


def to_int(val, field):
    """ Converts val to int """
    if isinstance(val, int):
        return val
    if isinstance(val, str) and val.isnumeric():
        return int(val)
    raise ValueError(f"'{field}' expects a numeric type")
   

def load_comments(fname: str) -> List:
    """
    Reads comments from a file and returns a list of comments
    """
    try:
        with open(fname,'rb') as fh:
            content = fh.read()
            lines = content.decode('utf-8').split('\n')
            comments = remove_carriage_ret(lines)
            comments = remove_blanks(comments)
            return comments
    except Exception as ex:
        logger.error(f'Error opening file: {fname}')
        return []


def load_tags(fname: str) -> List:
    """
    Returns list of tags from a file
    """
    tags = []
    try:
        with open(fname, 'r') as fh:
            tags = fh.read().split('\n')
            tags = [tag.strip() for tag in tags if tag != '']
    except Exception as ex:
        logger.error(f'Error opening file: {fname}')
    return tags


def parse_inlast(inlast: str) -> tuple:
        """
        Parses inlast value and returns (multiplier, tparam)
        tparams: 
            y -> year
            M -> month
            d -> day
            h -> hour
            m -> min
            s -> sec
        Ex: inlast -> 1h
            multiplier -> 1; tparam: h
        """
        if not inlast:
            return ()
        
        multiplier, tparam = (None,None)
        try:
            match = re.match(r'(\d+)(y|M|d|h|m|s)', inlast)
            if not match:
                return ()
            multiplier, tparam = match.groups()
            multiplier = int(multiplier)
        except:
            return ()
        return (multiplier, tparam)


def parse_delay(delay:str, default: tuple = (1,10)) -> tuple:
    """
    Parses delay value and returns start and end range
    """
    if not delay:
        return default

    match = re.match(r'(\d+),\s*(\d+)', delay)
    if match:
        st, en = map(int, match.groups())
        if st > en:
            logger.error(f'[parse_delay] Invalid delay range. Defaulting to {default}')
            return default
        if max(st,en) > 100 or min(st,en) < 1:
            logger.error(f'[parse_delay] Invalid delay range. Defaulting to {default}')
            return default
        if st == en:
            return (default[0],en)
        return (st, en)
    
    match = re.match(r'\d+$', delay)
    if match:
        st = int(match.group(0))
        return (st,) if st > 0 and st <= 100 else default
    
    raise ValueError(f"Invalid value received for 'delay' parameter: {delay}")


def parse_targets_multi(fname: str) -> List[str]:
    """
    Returns multiple targets from a file
    """
    if not pathexists(fname):
        return []
    try:
        targets = []
        with open(fname) as fh:
            targets = fh.read().split('\n')
            targets = [target.strip() for target in targets if target]
        return targets
    except Exception as ex:
        logger.error(f'Error opening file: {fname}')
    return []


def is_hashtag_present(targets: List) -> bool:
    """
    Checks if one of the targets is a hashtag
    """
    for target in targets:
        if target.startswith('#'):
            return True
    return False

        




