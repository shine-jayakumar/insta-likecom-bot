""" 
    stats.py - Stats class to keep track of activity

    insta-likecom-bot v.3.0.3
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

class Stats:

    def __init__(self):
        self.accounts: int = 0
        self.stories: int = 0
        self.private_accounts: int = 0
        self.likes: int = 0 
        self.story_likes: int = 0
        self.comment_likes: int = 0
        self.comments: int = 0
        self.story_comments: int = 0
