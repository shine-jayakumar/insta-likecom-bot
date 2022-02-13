"""
    insta-likecom-bot v.1
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
import param_funcs as pf
import os

# suppress webdriver manager logs
os.environ['WDM_LOG_LEVEL'] = '0'

DEFAULT_PARAMS = {
    "INSTA_USER": None,
    "INSTA_PASS": None,
    "TARGET": None,
    "COMMENTS_FILE": None,
    "NOCOMMENTS": None,
    "POSTSTOLIKE": None,
    "CRAZYMODE": None,
    "DELAY": None,
    "PS":None
}

COMMENTS = ["My jaw dropped", "This is amazing", "Awe-inspiring", "Sheeeeeeesh!","Out of this world",
"So beautiful ❤️", "So perfect ❤️", "Oh my lawd 😍", "I love this ❤️", "🔥🔥🔥", "👏👏",
"Beyond amazing 😍", "You’re the goat", "This is fire 🔥", "Keep grinding 💪", "Insane bro 🔥",
"The shocker! 😮", "Such a beauty 😍❤️", "Hell yeah 🔥", "Straight like that! 🔥", "Classy dude",
"Keep doing what you doing 🙌", "Freaking gorgeous 😍", "Keep going 💪", "You’re fabulous ❤️",
"This made my day 😍", "You’re literally unreal 😮", "I'm so obssessed", "Always popping off",
"Just like that 🔥", "Good vibes only ❤️", "This is mood ❤️", "The vibes are immaculate", "I adore you 🌺",
"You never fail to impress me😩", "These are hard 🔥", "Slaying as always 😍", "Blessing my feed rn 🙏",
"This is incredible ❤️", "Vibes on point 🔥", "You got it 🔥", "Dope!", "This is magical! ✨"]


def display_intro():

    intro = """
     ___ _  _ ___ _____ _      _    ___ _  _____ ___ ___  __  __     ___  ___ _____ 
    |_ _| \| / __|_   _/_\ ___| |  |_ _| |/ | __/ __/ _ \|  \/  |___| _ )/ _ |_   _|
     | || .` \__ \ | |/ _ |___| |__ | || ' <| _| (_| (_) | |\/| |___| _ | (_) || |  
    |___|_|\_|___/ |_/_/ \_\  |____|___|_|\_|___\___\___/|_|  |_|   |___/\___/ |_|  
    
    insta-likecom-bot v.1.2
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    
    """
    print(intro)


# Setting up logger
# =====================================================
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
#=======================================================

# checking command-line arguments
if len(sys.argv) < 2 or len(sys.argv) % 2 == 0 or not pf.check_params_present(['-u', '-p', '-t'], sys.argv):
    pf.display_help()
    sys.exit()

driver = None

try:
    start = time.time()

    display_intro()

    logger.info("Script started")
    logger.info("Loading arguments")
    #loading command line arguments
    pf.load_params(sys.argv, DEFAULT_PARAMS)

    if DEFAULT_PARAMS['COMMENTS_FILE']:
        COMMENTS = load_comments(DEFAULT_PARAMS['COMMENTS_FILE'])
        logger.info(f"Loaded comments from {DEFAULT_PARAMS['COMMENTS_FILE']}")

    if DEFAULT_PARAMS['CRAZYMODE']:
        DEFAULT_PARAMS['DELAY'] = 0.50
        logger.info("Crazy Mode set. Delay will be 0.5 seconds")

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    logger.info("Downloading webdriver for your version of chrome browser")
    # UNCOMMENT THIS TO SPECIFY LOCATION OF THE CHROMEDRIVER IN LOCAL MACHINE
    # driver = webdriver.Chrome("D:/chromedriver/98/chromedriver.exe", options=options)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 20)

    logger.info("Initializing instagram user")
    insta = Insta(driver, wait)
    insta.user(DEFAULT_PARAMS["INSTA_USER"], DEFAULT_PARAMS["INSTA_PASS"])

    logger.info(f"Setting target to: {DEFAULT_PARAMS['TARGET']}")
    # if tag
    if DEFAULT_PARAMS['TARGET'].startswith('#'):
        insta.target(DEFAULT_PARAMS['TARGET'][1:], tag=True)
    else:
        insta.target(DEFAULT_PARAMS['TARGET'])

    logger.info(f"Attempting to log in with {insta.username}")
    if not insta.login():
        raise Exception("Failed to login. Incorrect username/password, or 2 factor verification is active.")

    logger.info("Login successful")
    insta.dont_save_login_info()

    logger.info(f"Opening target {DEFAULT_PARAMS['TARGET']}")
    if not insta.open_target(3):
        logger.info("Invalid tag or account")
        raise Exception(f"Invalid tag or account : {DEFAULT_PARAMS['TARGET']}")

    no_of_posts = insta.get_number_of_posts()
    logger.info(f"No. of posts found: {no_of_posts}")

    insta.click_first_post()

    post = 0

    # if user specified the number of posts to like
    if DEFAULT_PARAMS['POSTSTOLIKE']:
        no_of_posts_to_like = min(no_of_posts, DEFAULT_PARAMS['POSTSTOLIKE'])
    else:
        no_of_posts_to_like = no_of_posts

    logger.info(f"Number of posts to like: {no_of_posts_to_like}")
    while post < no_of_posts_to_like:
        logger.info(f"Liking post: {post + 1}")
        insta.like()

        # don't comment if -nocom is set
        if not DEFAULT_PARAMS['NOCOMMENTS']:
            random_comment = COMMENTS[randint(0, len(COMMENTS)-1)]
            # add ps to the comment
            if DEFAULT_PARAMS['PS']:
                random_comment += " " + DEFAULT_PARAMS['PS']
            logger.info(f"Commenting on the post")
            insta.comment(random_comment, 5, 5)

        logger.info("Moving on to the next post")
        insta.next_post()
        # if there's a delay specified by user, otherwise random delay
        delay = DEFAULT_PARAMS['DELAY'] or randint(1,10)
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
    


