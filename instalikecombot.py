"""
    insta-likecom-bot v.1.2
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar

    LICENSE: MIT
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
from datetime import datetime
import sys
from random import randint
from instafunc import *
import argparse
import os

# suppress webdriver manager logs
os.environ['WDM_LOG_LEVEL'] = '0'

COMMENTS = ["My jaw dropped", "This is amazing", "Awe-inspiring", "Sheeeeeeesh!","Out of this world",
"So beautiful ❤️", "So perfect ❤️", "Oh my lawd 😍", "I love this ❤️", "🔥🔥🔥", "👏👏",
"Beyond amazing 😍", "You’re the goat", "This is fire 🔥", "Keep grinding 💪", "Insane bro 🔥",
"The shocker! 😮", "Such a beauty 😍❤️", "Hell yeah 🔥", "Straight like that! 🔥", "Classy dude",
"Keep doing what you doing 🙌", "Freaking gorgeous 😍", "Keep going 💪", "You’re fabulous ❤️",
"This made my day 😍", "You’re literally unreal 😮", "I'm so obssessed", "Always popping off",
"Just like that 🔥", "Good vibes only ❤️", "This is mood ❤️", "The vibes are immaculate", "I adore you 🌺",
"You never fail to impress me😩", "These are hard 🔥", "Slaying as always 😍", "Blessing my feed rn 🙏",
"This is incredible ❤️", "Vibes on point 🔥", "You got it 🔥", "Dope!", "This is magical! ✨"]

VERSION = 'v.1.2'

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


# ====================================================
# Argument parsing
# ====================================================
description = "Automates likes and comments on an instagram account or tag"
usage = "instalikecombot.py [-h] [-np NOOFPOSTS] [-ps TEXT] [-c FILE | -nc] [-d DELAY | -cz] username password target"
examples="""
Examples:
instalikecombot.py bob101 b@bpassw0rd1 elonmusk
instalikecombot.py bob101 b@bpassw0rd1 elonmusk -np 20
instalikecombot.py bob101 b@bpassw0rd1 #haiku -ps "Follow me @bob101" -c mycomments.txt
instalikecombot.py bob101 b@bpassw0rd1 elonmusk --crazy -nc
instalikecombot.py bob101 b@bpassw0rd1 elonmusk --delay 5 --numofposts 30
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    usage=usage,
    epilog=examples,
    prog='instalikecombot')

# required arguments
parser.add_argument('username', type=str, help='Instagram username')
parser.add_argument('password', type=str, help='Instagram password')
parser.add_argument('target',   type=str, help='target (account or tag)')

# optional arguments
parser.add_argument('-np', '--numofposts', type=int, metavar='', help='number of posts to like')
parser.add_argument('-ps', '--postscript', type=str, metavar='', help='additional text to add after every comment')

comments_group = parser.add_mutually_exclusive_group()
comments_group.add_argument('-c', '--comments', type=str, metavar='', help='file containing comments (one comment per line)')
comments_group.add_argument('-nc', '--nocomments', action='store_true', help='turn off comments')

delay_group = parser.add_mutually_exclusive_group()
delay_group.add_argument('-d', '--delay', type=int, metavar='', help='time to wait during post switch')
delay_group.add_argument('-cz', '--crazy', action='store_true', help='minimal wait during post switch')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')

args = parser.parse_args()
# ====================================================

# ====================================================
# Setting up logger
# ====================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s")
file_handler = logging.FileHandler(f'instalikecombot.py_{datetime.now().strftime("%d_%m_%Y__%H_%M_%S")}.log', 'w', 'utf-8')
file_handler.setFormatter(formatter)

stdout_formatter = logging.Formatter("[*] => %(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(stdout_formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
#======================================================

DELAY = args.delay
driver = None

try:
    start = time.time()

    display_intro()

    logger.info("Script started")

    # load comments from file
    if args.comments:
        COMMENTS = load_comments(args.comments)
        logger.info(f"Loaded comments from {args.comments}")

    # if crazy mode is set
    if args.crazy:
        DELAY = 1
        logger.info("Crazy Mode set. Delay will be 1 second")

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    logger.info("Downloading webdriver for your version of chrome browser")
    # UNCOMMENT THIS TO SPECIFY LOCATION OF THE CHROMEDRIVER IN LOCAL MACHINE
    # driver = webdriver.Chrome("D:/chromedriver/98/chromedriver.exe", options=options)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 30)

    logger.info("Initializing instagram user")
    insta = Insta(driver, wait)
    insta.user(args.username, args.password)

    logger.info(f"Setting target to: {args.target}")

    # if tag
    if args.target.startswith('#'):
        insta.target(args.target[1:], tag=True)
    else:
        insta.target(args.target)

    logger.info(f"Attempting to log in with {insta.username}")

    if not insta.login():
        raise Exception("Failed to login. Incorrect username/password, or 2 factor verification is active.")

    logger.info("Login successful")
    logger.info("Skipping Save Login Info")
    insta.dont_save_login_info()

    logger.info(f"Opening target {args.target}")
    if not insta.open_target(3):
        raise Exception(f"Invalid tag or account : {args.target}")

    no_of_posts = insta.get_number_of_posts()
    logger.info(f"No. of posts found: {no_of_posts}")

    # exit if it's a private account
    if insta.is_private():
        raise Exception(f"This account is private. You may need to follow {args.target} to like their posts.")

    insta.click_first_post()

    post = 0

    # if user specified the number of posts to like
    if args.numofposts:
        no_of_posts_to_like = min(no_of_posts, args.numofposts)
    else:
        no_of_posts_to_like = no_of_posts

    logger.info(f"Number of posts to like: {no_of_posts_to_like}")
    while post < no_of_posts_to_like:
        logger.info(f"Liking post: {post + 1}")
        insta.like()

        # don't comment if --nocomments is set
        if not args.nocomments:
            random_comment = COMMENTS[randint(0, len(COMMENTS)-1)]
            # add ps to the comment
            if args.postscript:
                random_comment += " " + args.postscript
            logger.info(f"Commenting on the post")
            insta.comment(random_comment, 5, 5)

        logger.info("Moving on to the next post")
        insta.next_post()
        # delay specified in --delay or random delay
        delay = DELAY or randint(1,10)
        logger.info(f"Waiting for {delay} seconds")
        time.sleep(delay)
        post += 1

    logger.info("Script finished successfully")

except Exception as ex:
    logger.error(f"Script ended with error : {ex}")

finally:
    if driver:
        driver.quit()
    timediff = time.time() - start
    logger.info(f"Total time taken: {round(timediff, 4)} seconds")
    sys.exit()
    


