
# stats class - track total accounts, likes, comments, stories processed

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
