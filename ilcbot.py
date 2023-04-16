"""
    insta-likecom-bot v.2.8
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
from modules.constants import getsettings, COMMENTS
from modules.applogger import AppLogger
from modules.argparsing import parser


args = parser.parse_args()
logger = AppLogger(__name__).getlogger()


IUSER = None
IPASS = None
TARGET = None

# load username, password, target from env
if args.loadenv:
    settings = getsettings()
    IUSER = settings['username']
    IPASS = settings['password']
    TARGET = settings['target']

    if not IUSER or not IPASS or not TARGET:
        print('Error: username, password, and target are required.')
        sys.exit(1)
# load username, password, target from arguments
else:
    if not args.username or not args.password or not args.target:
        print('Error: username, password, and target are required.')
        sys.exit(1)
    IUSER = args.username
    IPASS = args.password
    TARGET = args.target


DELAY = parse_delay(args.delay)

insta:Insta = None

stats = Stats()

try:
    start = time.time()

    display_intro()

    logger.info("Script started")
    logger.info(f'Delay: {DELAY[0]}{"-" + str(DELAY[1]) if len(DELAY) > 1 else ""} secs')
    
    # load comments from file
    if args.comments:
        COMMENTS = load_comments(args.comments)
        logger.info(f"Loaded comments from {args.comments}")

    # only one comment
    elif args.onecomment:
        COMMENTS = args.onecomment
        logger.info(f'Loading only one comment: {COMMENTS}')

    MATCHTAGS = load_matchtags(args.matchtags) if args.matchtags else []
    MATCH_TAG_CNT = 3
    if MATCHTAGS:
        if args.matchtagnum:
            MATCH_TAG_CNT = args.matchtagnum
            if MATCH_TAG_CNT > len(MATCHTAGS):
                raise Exception('Number of tags to match cannot be greater than total number of tags in matchtags')
        elif args.matchalltags:
            MATCH_TAG_CNT = len(MATCHTAGS)

        logger.info(f'MATCHTAGS: {MATCHTAGS}')
        logger.info(f'Match at least: {MATCH_TAG_CNT} tag(s)')
    

    LIKE_NCOMMENTS = args.likecomments if args.likecomments else 0
    if LIKE_NCOMMENTS:
        logger.info(f'Max. comments to like: {LIKE_NCOMMENTS}')


    if args.mostrecent:
        logger.info('Targetting most recent posts')
    
    INLAST_MULTIPLIER, INLAST_TPARAM = (None, None)
    if args.inlast:
        INLAST_MULTIPLIER, INLAST_TPARAM = parse_inlast(args.inlast)
        if not all([INLAST_MULTIPLIER, INLAST_TPARAM]):
            raise Exception('Invalid inlast value')
        logger.info(f'Filtering posts posted within last {args.inlast}')

    browser = args.browser
    logger.info(f"Downloading webdriver for your version of {browser.capitalize()}")

    logger.info("Initializing instagram user")
    insta = Insta(
        username=IUSER,
        password=IPASS,
        timeout=args.eltimeout,
        browser=browser,
        headless=args.headless
        )

    logger.info(f"Setting target to: {TARGET}")

    # if tag
    if TARGET.startswith('#'):
        insta.target(TARGET[1:], tag=True)
    else:
        insta.target(TARGET)

    # findfollowers with tag name
    if args.findfollowers and TARGET.startswith('#'):
        logger.error("Cannot use 'findfollowers' option with tags")
        raise Exception("Cannot use 'findfollowers' option with tags")

        
    logger.info(f"Attempting to log in with {IUSER}")

    if not insta.login():
        raise Exception("Failed to login. Incorrect username/password, or 2 factor verification is active.")

    logger.info("Login successful")
    # logger.info("Skipping Save Login Info")
    # logger.info(f'Do not save login info: {insta.dont_save_login_info()}')

    logger.info(f"Opening target {TARGET}")
    if not insta.open_target():
        logger.error(f'Invalid tag or account: {TARGET}')
        raise Exception(f"Invalid tag or account : {TARGET}")
    
    if args.findfollowers:
        logger.info(f'Finding followers of {args.target}')
        followers = insta.get_followers(args.followersamount)
        logger.info(followers)
        logger.info(f'Found {len(followers)} followers')
        target_list = followers
    else:
        target_list = [TARGET]
    
    stats.accounts = len(target_list)

    for target in target_list:
        
        # if findfollowers option is set
        # there would be multiple targets that
        # need to be set and opened
        if args.findfollowers:
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
        if args.viewstory and not private_account:
            if insta.is_story_present():
                insta.open_story()
                insta.pause_story()
                total_stories = insta.get_total_stories()
                stats.stories += total_stories

                like_stories_at = get_random_index(total_items=total_stories, arg=args.likestory)
                comment_stories_at = get_random_index(total_items=total_stories, arg=args.commentstory)
                for story_idx in range(total_stories):
                    if args.likestory and story_idx in like_stories_at:
                        insta.like_story()
                        stats.story_likes += 1
                        time.sleep(get_delay(delay=(2,10)))

                    if args.commentstory and story_idx in comment_stories_at:
                        insta.comment_on_story(generate_random_comment(COMMENTS))
                        stats.story_comments += 1
                        time.sleep(get_delay(delay=(2,10)))
                    insta.next_story()
            else:
                logger.info(f'[target: {target}] No stories found')
            time.sleep(2)

        # only stories to be processed
        if args.onlystory and args.likestory:
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
        if args.mostrecent:
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
        if args.numofposts:
            no_of_posts_to_like = min(no_of_posts, args.numofposts)
        else:
            no_of_posts_to_like = no_of_posts

        logger.info(f"[target: {target}] Number of posts to like: {no_of_posts_to_like}")
        
        post = 0
        reloadrepeat_cnt = 1
        # loop to like and comment
        while post < no_of_posts_to_like:

            if MATCHTAGS:
                # get tags from post
                posttags = insta.get_post_tags()
                logger.info(f'Tags: {posttags}')

                # minimum tag match
                if not insta.get_tag_match_count(posttags=posttags, matchtags=MATCHTAGS, min_match=MATCH_TAG_CNT):
                    logger.info('Irrelavent post')
                    logger.info(f"[target: {target}] Moving on to the next post")
                    insta.next_post()
                    # time.sleep(DELAY or randint(1,10))
                    time.sleep(get_delay(DELAY))
                    continue
            
            if args.inlast:
                # get post date
                postdate, ts = insta.get_post_date()
                
                if not insta.post_within_last(ts=ts, multiplier=INLAST_MULTIPLIER, tparam=INLAST_TPARAM):
                    logger.info(f'Post [{postdate}] is older than {INLAST_MULTIPLIER} {TParam[INLAST_TPARAM].value}{"s" if INLAST_MULTIPLIER>1 else ""}. Skipping')
                    insta.next_post()
                    # time.sleep(DELAY or randint(1,10))
                    time.sleep(get_delay(DELAY))
                    continue

            logger.info(f"[target: {target}] Liking post: {post + 1}")
            insta.like()
            stats.likes += 1
            
            # Added as per issue # 35
            # liking user comments
            if LIKE_NCOMMENTS:
                successful_comments = insta.like_comments(max_comments=LIKE_NCOMMENTS)
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
            if not args.nocomments and not comment_disabled:
                if args.onecomment:
                    random_comment = COMMENTS
                else:
                    random_comment = generate_random_comment(COMMENTS)
                    
                # add ps to the comment
                if args.postscript:
                    random_comment += " " + args.postscript

                logger.info(f"[target: {target}] Commenting on the post")
                if insta.comment(random_comment, 5, 5, fs_comment='Perfect!'):
                    stats.comments += 1
                    logger.info(f'[target: {target}] Commented: {random_comment}')
            
            logger.info(f"[target: {target}] Moving on to the next post")
            insta.next_post()
            # delay specified in --delay or random delay
            # delay = DELAY or randint(1,10)
            delay = get_delay(DELAY)
            logger.info(f"[target: {target}] Waiting for {delay} seconds")
            time.sleep(delay)
            post += 1

            # already viewed max no. of posts and reloadrepeat is specified
            if args.reloadrepeat and post >= no_of_posts_to_like and \
                reloadrepeat_cnt <= args.reloadrepeat:
                logger.info(f'[target: {target}] Reloading target [reload count:{reloadrepeat_cnt}]')
                post = 0
                reloadrepeat_cnt += 1
                # reload target
                insta.open_target()
                logger.info(f'[target: {target}] Waiting...')
                time.sleep(5)
                if args.mostrecent:
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
    logger.error(f'Error: [{ex.__class__.__name__}] - {str(ex)}')

finally:
    if insta:
        insta.quit()
    timediff = time.time() - start
    logger.info(f"Total time taken: {round(timediff, 4)} seconds")
    sys.exit()
    


