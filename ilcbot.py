"""
    insta-likecom-bot v.3.0.3
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""


import time
import sys
from modules.instafunc import *
from modules.stats import Stats
from modules.applogger import AppLogger
from modules.argparsing import parser
from modules.profile import Profile
from modules.exceptions import *
from modules.constants import INSTA_URL



args = parser.parse_args()

logger = AppLogger('ilcbot').getlogger()

try:
    profile = Profile(args=args)
except Exception as ex:
    logger.error('Script ended with error')
    logger.error(f'{ex.__class__.__name__}: {str(ex)}')
    sys.exit(1)


insta:Insta = None
stats = Stats()

try:
    start = time.time()

    display_intro()

    logger.info("Script started")
    logger.info(f"Downloading webdriver for your version of {profile.browser.capitalize()}")

    logger.info("Loading Instagram")
    insta = Insta(
        username=profile.username,
        password=profile.password,
        timeout=profile.eltimeout,
        browser=profile.browser,
        headless=profile.headless,
        profile=profile.brprofile
    )
    if profile.headless:
        logger.info('Running in headless mode')
        
    logger.info(f'Delay: {profile.delay[0]}{"-" + str(profile.delay[1]) if len(profile.delay) > 1 else ""} secs')

    if profile.matchtags:
        logger.info(f'Match tags: {profile.matchtags}')
        if profile.matchtagnum:
            logger.info(f'Match at least: {profile.matchtagnum}')
    
    if profile.ignoretags:
        logger.info(f'Ignore tags: {profile.ignoretags}')
    
    if profile.likecomments:
        logger.info(f'Max. comments to like: {profile.likecomments}')

    if profile.mostrecent:
        logger.info('Targetting most recent posts')

    if profile.inlast:
        logger.info(f'Filtering posts posted within last {profile.inlast}')

    # if browser profile was specified
    if profile.brprofile:
        logger.info(f'Using profile: {profile.brprofile}')
        logger.info('Launching Instagram')
        insta.launch_insta()

        logger.info('Checking if user is already logged in')
        # check if already logged in
        if not insta.validate_login():
            logger.info('User not logged in. Attempting to login')
            if not insta.login(validate=False):
                raise LoginFailedError('Failed to login to Instagram')
            
            if insta.is_2factor_present():
                logger.info('Script paused for 10 seconds (waiting for code)')
                time.sleep(10)

            logger.info('Validating login')
            if not insta.validate_login():
                raise LoginFailedError("Failed to login. Incorrect username/password, or 2 factor verification is active.")
            logger.info('Logged in successfully')

            logger.info('Attempting to save login information')
            # attempt to save login info
            if not insta.save_login_info():
                raise Exception('Could not find Save Login Info dialog box')
            logger.info('Login information saved for the profile')
            time.sleep(2)

    # attempt to login in only if profile wasn't loaded
    # in which case, script will save the Login Info
    else:
        logger.info(f"Attempting to log in with {profile.username}")
        if not insta.login():
            raise LoginFailedError("Failed to login. Incorrect username/password, or 2 factor verification is active.")
        logger.info("Login successful")

    # EXTRACTING FOLLOWERS
    target_list = []
    # extracting followers from multiple targets
    if profile.findfollowers:
        for target in profile.target:
            logger.info(f"Setting target to: {target}")
            insta.target(target)

            logger.info(f"Opening target {target}")
            if not insta.open_target():
                logger.error(f'Invalid tag or account: {target}')
                raise InvalidAccountError(f"Invalid tag or account : {target}")
            
            logger.info(f'Finding followers of {target}')
            followers = insta.get_followers(amount = profile.followersamount)
            logger.info(followers)
            logger.info(f'Found {len(followers)} followers')
            target_list.extend(followers)
    else:
        target_list = profile.target

    stats.accounts = len(target_list)

    for target in target_list:
        
        # setting target
        logger.info(f'Setting target to: {target}')
        insta.target(target)

        # opening target
        logger.info(f"[target: {target}] Opening target")
        if not insta.open_target():
            logger.error(f'[target: {target}] Invalid tag or account')
            continue

        # check if account is private
        private_account = insta.is_private()
        if private_account:
            stats.private_accounts += 1
            logger.info(f'[target: {target}] Private account')

        # view, like and comment on stories
        if profile.viewstory and not private_account:
            if insta.is_story_present():
                insta.open_story()
                insta.pause_story()
                total_stories = insta.get_total_stories()
                stats.stories += total_stories

                like_stories_at = get_random_index(total_items=total_stories, nreq=profile.likestory)
                comment_stories_at = get_random_index(total_items=total_stories, nreq=profile.commentstory)
                for story_idx in range(total_stories):
                    if profile.likestory and story_idx in like_stories_at:
                        insta.like_story()
                        stats.story_likes += 1
                        time.sleep(get_delay(delay=(2,10)))

                    if profile.commentstory and story_idx in comment_stories_at:
                        insta.comment_on_story(generate_random_comment(profile.comments))
                        stats.story_comments += 1
                        time.sleep(get_delay(delay=(2,10)))
                    insta.next_story()
            else:
                logger.info(f'[target: {target}] No stories found')
            time.sleep(2)

        # only stories to be processed
        if profile.onlystory and profile.likestory:
            continue

        # getting number of posts
        no_of_posts = None
        max_tries = 3
        tries = 0
        while no_of_posts == None and tries < max_tries:
            no_of_posts = insta.get_number_of_posts()
            if no_of_posts != None:
                logger.info(f"[target: {target}] No. of posts found: {no_of_posts}")
            else:
                logger.error(f'[target: {target}, retry={tries+1}] Unable to find posts. Reloading the target')
                insta.open_target()
            tries += 1

        # if not posts found
        if no_of_posts == None or no_of_posts == 0:
            logger.info(f'[target: {target}] No posts found for the target')
            continue

        # it's a private account
        if private_account:
            logger.info(f"[target: {target}] This account is private. You may need to follow {target} to like their posts.")
            continue        
        
        # open first post
        if profile.mostrecent:
            # if not able to open find most recent
            logger.info(f'[target: {target} (Most Recent)] Opening first post')
            if not insta.click_first_post_most_recent(): 
                logger.info('Unable to find most recent posts. Continuing with top posts.')
                # first post of Most Recent
                insta.click_first_post()
        else:
            # first post of Top Posts
            logger.info(f'[target: {target} (Top Posts)] Opening first post')
            insta.click_first_post()

        
        # if user specified the number of posts to like
        if profile.numofposts:
            no_of_posts_to_like = min(no_of_posts, profile.numofposts)
        else:
            no_of_posts_to_like = no_of_posts

        logger.info(f"[target: {target}] Number of posts to like: {no_of_posts_to_like}")
        
        post = 0
        reloadrepeat_cnt = 1
        # loop to like and comment
        while post < no_of_posts_to_like:

            if profile.matchtags or profile.ignoretags:
                # get tags from post
                posttags = insta.get_post_tags()
                logger.info(f'Post Tags: {posttags}')

                # minimum tag match
                if profile.matchtags and not insta.get_tag_match_count(posttags=posttags, matchtags=profile.matchtags, min_match=profile.matchtagnum): 
                    logger.info('Irrelavent post - no matching tags found')
                    logger.info(f"[target: {target}] Moving on to the next post")
                    insta.next_post()
                    # time.sleep(DELAY or randint(1,10))
                    time.sleep(get_delay(profile.delay))
                    continue
                
                # ignore tags
                if profile.ignoretags and set(posttags).intersection(profile.ignoretags):
                    logger.info('Irrelavent post - Tags to ignore found')
                    logger.info(f"[target: {target}] Moving on to the next post")
                    insta.next_post()
                    # time.sleep(DELAY or randint(1,10))
                    time.sleep(get_delay(profile.delay))
                    continue

            if profile.inlast:
                # get post date
                postdate, ts = insta.get_post_date()
                
                if not insta.post_within_last(ts=ts, multiplier=profile.inlast_multiplier, tparam=profile.inlast_tparam):
                    logger.info(
                        f'Post [{postdate}] is older than {profile.inlast_multiplier} {TParam[profile.inlast_tparam].value}{"s" if profile.inlast_multiplier>1 else ""}. Skipping'
                    )
                    insta.next_post()
                    # time.sleep(DELAY or randint(1,10))
                    time.sleep(get_delay(profile.delay))
                    continue

            logger.info(f"[target: {target}] Liking post: {post + 1}")
            insta.like()
            stats.likes += 1
            
            # Added as per issue # 35
            # liking user comments
            if profile.likecomments:
                successful_comments = insta.like_comments(max_comments=profile.likecomments)
                if successful_comments:
                    stats.comment_likes += 1
                    for username, comment in successful_comments:
                        logger.info(f'[target: {target}] Liked [({username}) - {comment}]')
                else:
                    logger.info('No comments found for this post')

            # comments disabled or not                  
            comment_disabled = True
            comment_disabled = insta.is_comment_disabled()
            logger.info(f'[target: {target}] Comment disabled? {"Yes" if comment_disabled else "No"}')

            # don't comment if --nocomments is set
            # and if comments are enabled
            if not profile.nocomments and not comment_disabled:
                if profile.onecomment:
                    random_comment = profile.onecomment
                else:
                    random_comment = generate_random_comment(profile.comments)
                    
                # add ps to the comment
                if profile.postscript:
                    random_comment += " " + profile.postscript

                # check if post has to be ignored if already commented and skipcommented flag is set
                if any([not profile.skipcommented, all([profile.skipcommented, not insta.is_commented()])]):
                    logger.info(f"[target: {target}] Commenting on the post")
                    if insta.comment(random_comment, timeout = 5, fs_comment = 'Perfect!'):
                        stats.comments += 1
                        logger.info(f'[target: {target}] Commented: {random_comment}')
                else:
                    logger.info(f"[target: {target}] Skipping post. Already commented.")
            
            logger.info(f"[target: {target}] Moving on to the next post")
            insta.next_post()
            # delay specified in --delay or random delay
            # delay = DELAY or randint(1,10)
            delay = get_delay(profile.delay)
            logger.info(f"[target: {target}] Waiting for {delay} seconds")
            time.sleep(delay)
            post += 1

            # already viewed max no. of posts and reloadrepeat is specified
            if profile.reloadrepeat and post >= no_of_posts_to_like and \
                reloadrepeat_cnt <= profile.reloadrepeat:
                logger.info(f'[target: {target}] Reloading target [reload count:{reloadrepeat_cnt}]')
                post = 0
                reloadrepeat_cnt += 1
                # reload target
                insta.open_target()
                logger.info(f'[target: {target}] Waiting...')
                time.sleep(5)
                if profile.mostrecent:
                    # if not able to open find most recent
                    logger.info(f'[target: {target} (Most Recent)] Opening first post')
                    if not insta.click_first_post_most_recent(): 
                        logger.info('Unable to find most recent posts. Continuing with top posts.')
                        # first post of Most Recent
                        insta.click_first_post()


    logger.info("Script finished successfully")
    logger.info(f'Total accounts: {stats.accounts}')
    logger.info(f'Total post likes: {stats.likes}')
    logger.info(f'Total post comments: {stats.comments}')
    logger.info(f'Total post comment likes: {stats.comment_likes}')
    logger.info(f'Total stories: {stats.stories}')
    logger.info(f'Total story likes: {stats.story_likes}')
    logger.info(f'Total story comments: {stats.story_comments}')

except Exception as ex:
    logger.error(f"Script ended with error")
    logger.error(f'Error: [{ex.__class__.__name__}] - {str(ex)}',exc_info=1)

finally:
    if insta:
        insta.quit()
    timediff = time.time() - start
    logger.info(f"Total time taken: {round(timediff, 4)} seconds")
    sys.exit()
    


