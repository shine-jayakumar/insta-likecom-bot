""" 
    instaworkflows.py - Instagram workflows - Posts, Stories, Reels
    insta-likecom-bot v.3.0.5
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

from modules.exceptions import InvalidAccountError
from modules.helpers import get_delay, get_random_index, generate_random_comment
import time
from typing import List, Callable
from modules.insta import TParam


class InstaWorkFlow:
    
    def __init__(self, insta: 'Insta', profile: 'Profile'):
        self.insta = insta
        self.profile = profile


class Followers(InstaWorkFlow):
    
    def __init__(self, insta: 'Insta', profile: 'Profile', logger) -> None:
        super().__init__(insta, profile)
        self.logger = logger

    def get_targets(self, stats: 'Stats') -> list[str]:
        
        if not self.profile.findfollowers:
            return self.profile.target
        
        target_list = []

        for target in self.profile.target:
            self.logger.info(f"Setting target to: {target}")
            self.insta.target(target)

            self.logger.info(f"Opening target {target}")
            if not self.insta.open_target():
                self.logger.error(f'Invalid tag or account: {target}')
                raise InvalidAccountError(f"Invalid tag or account : {target}")
                
            self.logger.info(f'Finding followers of {target}')
            followers = self.insta.get_followers(amount = self.profile.followersamount)
            self.logger.info(followers)
            self.logger.info(f'Found {len(followers)} followers for {target}')
            target_list.extend(followers)

        stats.accounts = len(target_list)
        return target_list
    

class Story(InstaWorkFlow):
    
    def __init__(self, insta: 'Insta', profile: 'Profile', is_private: bool, logger):
        super().__init__(insta, profile)
        self.is_private = is_private
        self.logger = logger
    
    def interact(self, target, stats: 'Stats') -> None | bool:

        if not self.profile.viewstory:
            self.logger.info(f"[{target}] '--viewstory' argument not set. Skipping stories.")
            return 
        
        if self.is_private:
            self.logger.info(f"[{target}] Private account. Skipping stories.")
            return 
        
        if not self.insta.is_story_present():
            self.logger.info(f'[target: {target}] No stories found')
            return
        
        self.insta.open_story()
        self.insta.pause_story()
        total_stories = self.insta.get_total_stories()
        
        like_stories_at = get_random_index(total_items=total_stories, nreq=self.profile.likestory)
        comment_stories_at = get_random_index(total_items=total_stories, nreq=self.profile.commentstory)
        for story_idx in range(total_stories):
            stats.stories += 1
            if self.profile.likestory and story_idx in like_stories_at:
                if self.insta.like_story():
                    stats.story_likes += 1
                    self.logger.info(f'[{target}] Liked story # {story_idx+1}')
                    time.sleep(get_delay(delay=(1,3)))

            if self.profile.commentstory and story_idx in comment_stories_at:
                comment_text = generate_random_comment(self.profile.comments)
                if self.insta.comment_on_story(comment_text):
                    stats.story_comments += 1
                    self.logger.info(f'[{target}] Commented on story # {story_idx+1}: {comment_text}')
                    time.sleep(get_delay(delay=(1,3)))
            
            self.insta.next_story()
            time.sleep(0.5)
            self.insta.pause_story()
            time.sleep(1)
            stats.save()
        return True


class Post(InstaWorkFlow):
    
    def __init__(self, insta: 'Insta', profile: 'Profile', logger):
        super().__init__(insta, profile)
        self.logger = logger

    def _is_post_eligible(self, filters: List[Callable]):
        return all([filter() for filter in filters])
    
    def _filter_matchtags(self) -> bool:
        """
        Checks post eligibility based on tags
        """
        if not self.profile.matchtags:
            return True
        
        tags = self.insta.get_post_tags()
        self.logger.info(f'Post tags: {tags}')
        if self.insta.get_tag_match_count(
            posttags=tags, matchtags=self.profile.matchtags, 
            min_match=self.profile.matchtagnum):
            self.logger.info(f'[Filter MatchTags] Post is eligible')
            return True
        
        self.logger.info(f'[Filter MatchTags] Post not eligible')
        return False
    
    def _filter_ignoretags(self) -> bool:
        """
        Checks post eligibility based on tags to ignore
        """
        if not self.profile.ignoretags:
            return True
        
        tags = self.insta.get_post_tags()
        if set(tags).intersection(self.profile.ignoretags):
            self.logger.info(f'[Filter IgnoreTags] Post not eligible')
            return False
        return True
    
    def _filter_inlast(self) -> bool:
        """
        Checks post eligbility based on time filter
        """
        if not self.profile.inlast:
            return True
        
        postdate, ts = self.insta.get_post_date()

        if not self.insta.post_within_last(
            ts=ts, multiplier=self.profile.inlast_multiplier, 
            tparam=self.profile.inlast_tparam):
                self.logger.info(f'Post [{postdate}] is older than {self.profile.inlast_multiplier} {TParam[self.profile.inlast_tparam].value}{"s" if self.profile.inlast_multiplier>1 else ""}. Post not eligible')
                return False
        return True
    
    def _like_comments(self, target, stats) -> bool:
        """ 
        Likes comments on the post
        """
        if not self.profile.likecomments:
            return
        
        successful_comments = self.insta.like_comments(max_comments=self.profile.likecomments)
        if not successful_comments:
            self.logger.info('No comments found for this post')
            return False
        
        for username, comment in successful_comments:
            self.logger.info(f'[target: {target}] Liked [({username}) - {comment}]')
            stats.comment_likes += 1
        return True

    def _comment(self, target, stats) -> bool:
        """
        Comments on post
        """
        if self.profile.nocomments:
            return
        
        # comments disabled or not                  
        if self.insta.is_comment_disabled():
            self.logger.info(f'[target: {target}] Comment disabled for this post')
            return
        
        if self.profile.skipcommented and self.insta.is_commented():
            self.logger.info(f'[target: {target}] Already commented on this post')
            return
        
        # generating comment text
        comment_text = ''
        if self.profile.onecomment:
            comment_text = self.profile.onecomment
        else:
            comment_text = generate_random_comment(self.profile.comments)
        
        # adding postscript
        if self.profile.postscript:
            comment_text += ' ' + self.profile.postscript
        
        # check if post has to be ignored if already commented and skipcommented flag is set
        if self.insta.comment(comment_text, timeout = 5, fs_comment = 'Perfect!'):
            stats.comments += 1
            self.logger.info(f'[target: {target}] Commented: {comment_text}')

        return True
        
    def interact(self, target: str, is_private: bool, stats: 'Stats') -> None | bool:
        """
        Interact with posts
        """

        if self.profile.onlystory or self.profile.onlyreels:
            return
        
        if is_private:
            self.logger.info(f"[target: {target}] This account is private. You may need to follow {target} to like their posts.")
            return 
        
        total_posts = self.insta.get_number_of_posts()
        if not total_posts:
            self.logger.info(f"[target: {target}] No. of posts found: {total_posts}")
            return
        
        posts_to_interact = total_posts
        if self.profile.numofposts:
            posts_to_interact = min(total_posts, self.profile.numofposts)
        self.logger.info(f"[target: {target}] Posts to interact: {posts_to_interact}")
        
        # first post of Top Posts
        self.logger.info(f'[target: {target} (Top Posts)] Opening first post')
        self.insta.click_first_post()

        if posts_to_interact and not self._filter_inlast():
            self.logger.info(f"[target: {target}] Latest post older than set time limit.")
            return True

        post = 0
        while post < posts_to_interact:
            # check post eligibility
            post_eligible = self._is_post_eligible(filters=[
                self._filter_matchtags,
                self._filter_ignoretags,
                self._filter_inlast
            ])
            if not post_eligible:
                time.sleep(get_delay(self.profile.delay))
                self.logger.info(f"[target: {target}] Moving on to the next post")
                self.insta.next_post()
                continue
            
            if self.insta.like():
                stats.likes += 1

            self._like_comments(target, stats)
            self._comment(target, stats)

            self.logger.info(f"[target: {target}] Moving on to the next post")
            self.insta.next_post()

            delay = get_delay(self.profile.delay)
            self.logger.info(f"[target: {target}] Waiting for {delay} seconds")
            time.sleep(delay)
            post += 1
            stats.save()
        return True


class Reel(InstaWorkFlow):
    def __init__(self, insta: 'Insta', profile: 'Profile', logger):
        super().__init__(insta, profile)
        self.logger = logger
    
    def _comment(self, target: str, stats: 'Stats') -> bool:
        """
        Comment on a reel
        """
        if self.profile.nocomments:
            return
        
        # comments disabled or not                  
        if self.insta.is_comment_disabled():
            self.logger.info(f'[target: {target}] Comment disabled for this reel')
            return
        
        if self.profile.skipcommented and self.insta.is_commented():
            self.logger.info(f'[target: {target}] Already commented on this reel')
            return
        
        # generating comment text
        comment_text = ''
        if self.profile.onecomment:
            comment_text = self.profile.onecomment
        else:
            comment_text = generate_random_comment(self.profile.comments)
        
        # adding postscript
        if self.profile.postscript:
            comment_text += ' ' + self.profile.postscript
        
        # check if post has to be ignored if already commented and skipcommented flag is set
        if self.insta.comment(comment_text, timeout = 5, fs_comment = 'Perfect!'):
            stats.comments += 1
            self.logger.info(f'[target: {target}] Commented: {comment_text}')

        return True
    
    def _like_comments(self, target, stats) -> bool:
        """ 
        Likes comments on a reel
        """
        if not self.profile.likereelcomments:
            return
        
        successful_comments = self.insta.like_comments(max_comments=self.profile.likereelcomments)
        if not successful_comments:
            self.logger.info('No comments found for this reel')
            return False
        
        for username, comment in successful_comments:
            self.logger.info(f'[target: {target}] Liked [({username}) - {comment}]')
            stats.comment_likes += 1
        return True
    
    def interact(self, target: str, is_private: bool, stats: 'Stats') -> None | bool:
        """
        Interact with reels
        """
        if not self.profile.numofreels:
            return

        if self.profile.onlystory:
            return
        
        if is_private:
            return
        
        if not self.insta.is_reels_present():
            self.logger.info(f'[target: {target}] No reels present')
            return

        if not self.insta.open_reels():
            self.logger.error(f'[target: {target}] Failed to open reels page')
            return False
        
        self.insta.click_first_reel()

        reel = 0
        while reel < self.profile.numofreels:

            self.insta.like_reel()
            stats.reel_likes += 1

            self._comment(target, stats)
            self._like_comments(target, stats)

            self.logger.info(f"[target: {target}] Moving on to the next reel")
            self.insta.next_reel()

            delay = get_delay(self.profile.delay)
            self.logger.info(f"[target: {target}] Waiting for {delay} seconds")
            time.sleep(delay)
            reel += 1
            stats.save()
        return True


if __name__ == '__main__':
    pass
            


