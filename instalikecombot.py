"""
    insta-likecom-bot v.2.2
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar

    LICENSE: MIT
"""


import time
from datetime import datetime
import sys
from random import randint
from instafunc import *
import argparse
from constants import getsettings
from applogger import AppLogger


COMMENTS = ["My jaw dropped", "This is amazing", "Awe-inspiring", "Sheeeeeeesh!","Out of this world",
"So beautiful ❤️", "So perfect ❤️", "Oh my lawd 😍", "I love this ❤️", "🔥🔥🔥", "👏👏",
"Beyond amazing 😍", "You’re the goat", "This is fire 🔥", "Keep grinding 💪", "Insane bro 🔥",
"The shocker! 😮", "Such a beauty 😍❤️", "Hell yeah 🔥", "Straight like that! 🔥", "Classy dude",
"Keep doing what you doing 🙌", "Freaking gorgeous 😍", "Keep going 💪", "You’re fabulous ❤️",
"This made my day 😍", "You’re literally unreal 😮", "I'm so obssessed", "Always popping off",
"Just like that 🔥", "Good vibes only ❤️", "This is mood ❤️", "The vibes are immaculate", "I adore you 🌺",
"You never fail to impress me😩", "These are hard 🔥", "Slaying as always 😍", "Blessing my feed rn 🙏",
"This is incredible ❤️", "Vibes on point 🔥", "You got it 🔥", "Dope!", "This is magical! ✨"]

VERSION = 'v.2.2'

def display_intro():

    intro = f"""
     ___ _  _ ___ _____ _      _    ___ _  _____ ___ ___  __  __     ___  ___ _____ 
    |_ _| \| / __|_   _/_\ ___| |  |_ _| |/ | __/ __/ _ \|  \/  |___| _ )/ _ |_   _|
     | || .` \__ \ | |/ _ |___| |__ | || ' <| _| (_| (_) | |\/| |___| _ | (_) || |  
    |___|_|\_|___/ |_/_/ \_\  |____|___|_|\_|___\___\___/|_|  |_|   |___/\___/ |_|  
    
    insta-likecom-bot {VERSION}
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    
    """
    print(intro)


def generate_random_comment(comments):
    """
    Returns a random comment from a list of comments
    """
    return comments[randint(0, len(comments)-1)]


# ====================================================
# Argument parsing
# ====================================================
description = "Automates likes and comments on an instagram account or tag"
usage = "instalikecombot.py [-h] [-u --username] [-p --password] [-t --target] [-le --loadenv] [-np NOOFPOSTS] [-ps TEXT] [-c FILE | -nc] [-d DELAY] [-hl --headless]"
examples="""
Examples:
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 20
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t '#haiku' -ps "Follow me @bob101" -c mycomments.txt
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk --delay 5 --numofposts 30 --headless
instalikecombot.py --loadenv --delay 5 --numofposts 10 --headless --nocomments
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    usage=usage,
    epilog=examples,
    prog='instalikecombot')


# optional arguments
parser.add_argument('-u','--username', metavar='', type=str, help='Instagram username')
parser.add_argument('-p','--password', metavar='', type=str, help='Instagram password')
parser.add_argument('-t', '--target',  metavar='', type=str, help='target (account or tag)')

parser.add_argument('-np', '--numofposts', type=int, metavar='', help='number of posts to like')
parser.add_argument('-ps', '--postscript', type=str, metavar='', help='additional text to add after every comment')
parser.add_argument('-ff', '--findfollowers', action='store_true', help="like/comment on posts from target's followers")
parser.add_argument('-fa', '--followersamount', type=int, metavar='', help='number of followers to process (default=all)', default=None)

parser.add_argument('-mt', '--matchtags', type=str, metavar='', help='read tags to match from a file')
match_group = parser.add_mutually_exclusive_group()
match_group.add_argument('-mn', '--matchtagnum', type=int, metavar='', help='minimum tag match count for post to be qualified')
match_group.add_argument('-ma', '--matchalltags', action='store_true', help='match all tags in matchtags')

comments_group = parser.add_mutually_exclusive_group()
comments_group.add_argument('-c', '--comments', type=str, metavar='', help='file containing comments (one comment per line)')
comments_group.add_argument('-oc', '--onecomment', type=str, metavar='', help='specify only one comment')
comments_group.add_argument('-nc', '--nocomments', action='store_true', help='turn off comments')

parser.add_argument('-et', '--eltimeout',  type=str, metavar='', help='max time to wait for elements to be loaded (default=30)', default=30)

parser.add_argument('-d', '--delay', type=int, metavar='', help='time to wait during post switch')
parser.add_argument('-br', '--browser',  type=str, metavar='', choices = ('chrome', 'firefox'), help='browser to use [chrome|firefox] (default=chrome)', default='chrome')
parser.add_argument('-hl', '--headless',  action='store_true', help='headless mode')
parser.add_argument('-le', '--loadenv',  action='store_true', help='load credentials from .env')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')

args = parser.parse_args()
# ====================================================

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


# ====================================================
# Setting up logger
# ====================================================
logger = AppLogger(__name__).getlogger()
#======================================================

DELAY = args.delay

insta:Insta = None

try:
    start = time.time()

    display_intro()

    logger.info("Script started")

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
        logger.info(f'[target: {target}] Checking if {target} is a private account')
        if insta.is_private():
            logger.info(f"[target: {target}] This account is private. You may need to follow {target} to like their posts.")
            continue
        logger.info(f'[target: {target}] Account not private')
        
        
        # open first post
        logger.info(f'[target: {target}] Opening first post')
        insta.click_first_post()

        post = 0

        # if user specified the number of posts to like
        if args.numofposts:
            no_of_posts_to_like = min(no_of_posts, args.numofposts)
        else:
            no_of_posts_to_like = no_of_posts

        logger.info(f"[target: {target}] Number of posts to like: {no_of_posts_to_like}")

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
                    time.sleep(DELAY or randint(1,10))                    
                    continue
            
            logger.info(f"[target: {target}] Liking post: {post + 1}")
            insta.like()

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
                    logger.info(f'[target: {target}] Commented: {random_comment}')

            logger.info(f"[target: {target}] Moving on to the next post")
            insta.next_post()
            # delay specified in --delay or random delay
            delay = DELAY or randint(1,10)
            logger.info(f"[target: {target}] Waiting for {delay} seconds")
            time.sleep(delay)
            post += 1

    logger.info("Script finished successfully")

except Exception as ex:
    logger.error(f"Script ended with error : {str(ex)}")

finally:
    if insta:
        insta.quit()
    timediff = time.time() - start
    logger.info(f"Total time taken: {round(timediff, 4)} seconds")
    sys.exit()
    


