
"""
    locators.py - contains classes to access DOM locators for Instagram elements

    insta-likecom-bot v.3.0.5
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

from dataclasses import dataclass
import json
import os
import requests
from modules.constants import LOCATORS_URL, LOCATORS_DIR
from modules.applogger import AppLogger


logger = AppLogger('locators').getlogger()


LOCATORS = json.load(open(os.path.join(LOCATORS_DIR, 'locators.json')))

try:
    locators_remote = requests.get(LOCATORS_URL).json()
    if all([
        locators_remote,
        locators_remote.get('version', ''),
        int(LOCATORS['version'].replace('.','')) < int(locators_remote['version'].replace('.',''))
        ]):
        LOCATORS = locators_remote    
except Exception as ex:
    logger.error(f'[Fetch Locators] {ex.__class__.__name__} - {str(ex)}')


@dataclass
class AccountLocators:
    is_private: tuple[str] = tuple(LOCATORS['locators']['account']['is_private'])
    
@dataclass
class SaveLoginLocators:
    notnow: tuple[str] = tuple(LOCATORS['locators']['login']['save_login']['notnow'])
    save: tuple[str] = tuple(LOCATORS['locators']['login']['save_login']['save'])


@dataclass
class LoginLocators:
    username: str = LOCATORS['locators']['login']['username']
    password: str = LOCATORS['locators']['login']['password']
    submit: str = LOCATORS['locators']['login']['submit']
    validaton: tuple[str] = tuple(LOCATORS['locators']['login']['validation'])
    twofactor: str = LOCATORS['locators']['login']['twofactor']
    save_login: SaveLoginLocators = SaveLoginLocators()


@dataclass
class PostCommentLocators:
    comment_list: str = LOCATORS['locators']['post']['post_properties']['comment']['comments_list']
    username: str = LOCATORS['locators']['post']['post_properties']['comment']['username']
    comment: str = LOCATORS['locators']['post']['post_properties']['comment']['comment']
    like: str = LOCATORS['locators']['post']['post_properties']['comment']['like']
    is_liked: str = LOCATORS['locators']['post']['post_properties']['comment']['is_liked']


@dataclass
class PostPropertiesLocators:
    tags: str = LOCATORS['locators']['post']['post_properties']['tags']
    comment: PostCommentLocators = PostCommentLocators()
    date: str = LOCATORS['locators']['post']['post_properties']['date']


@dataclass
class PostLocators:
    like: str = LOCATORS['locators']['post']['like']
    comment: str = LOCATORS['locators']['post']['comment']
    comment_post: str = LOCATORS['locators']['post']['comment_post']
    comment_disabled: str = LOCATORS['locators']['post']['comment_disabled']
    num_of_posts: str = LOCATORS['locators']['post']['num_of_posts']
    first_post: str = LOCATORS['locators']['post']['first_post']
    properties: PostPropertiesLocators = PostPropertiesLocators()


@dataclass
class StoryPauseLocators:
    container: str = LOCATORS['locators']['story']['pause']['container']
    pause_button: str = LOCATORS['locators']['story']['pause']['pause_button']


@dataclass
class StoryLikeLocators:
    container: str = LOCATORS['locators']['story']['like']['container']
    like_button: str = LOCATORS['locators']['story']['like']['like_button']
    unlike_button: str = LOCATORS['locators']['story']['like']['unlike_button']


@dataclass
class StoryCommentLocators:
    container: str = LOCATORS['locators']['story']['comment']['container']
    comment_box: str = LOCATORS['locators']['story']['comment']['comment_box']


@dataclass
class StoryCountLocators:
    container: str = LOCATORS['locators']['story']['count']['container']
    story: str = LOCATORS['locators']['story']['count']['story']


@dataclass
class StoryLocators:
    is_present: str = LOCATORS['locators']['story']['is_present']
    pause: StoryPauseLocators = StoryPauseLocators()
    like: StoryLikeLocators = StoryLikeLocators()
    comment: StoryCommentLocators = StoryCommentLocators()
    next: str = LOCATORS['locators']['story']['next']
    count: StoryCountLocators = StoryCountLocators()


@dataclass
class ReelsLocators:
    first_reel: str  = LOCATORS['locators']['reels']['first_reel']


@dataclass
class FollowersLocators:
    link: str = LOCATORS['locators']['followers']['link']
    container: str = LOCATORS['locators']['followers']['container']

if __name__ == '__main__':
    pass