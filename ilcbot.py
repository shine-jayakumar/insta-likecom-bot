"""
    insta-likecom-bot v.3.0.4
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""


import time
import sys
from modules.insta import Insta
from modules.stats import Stats
from modules.applogger import AppLogger
from modules.argparsing import parser
from modules.profile import Profile
from modules.instaworkflows import Followers, Story, Post, Reel
from modules.exceptions import *
from modules.helpers import display_intro


args = parser.parse_args()

logger = AppLogger('ilcbot').getlogger()

try:
    profile = Profile(args=args)
except Exception as ex:
    logger.error('Script ended with error')
    logger.error(f'{ex.__class__.__name__}: {str(ex)}')
    sys.exit(1)


insta:Insta = None
stats = Stats(profile.limits)

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

    # Extracting followers
    target_list = Followers(insta, profile, logger).get_targets(stats)

    for target in target_list:
        
        # setting target
        logger.info(f'Setting target to: {target}')
        insta.target(target)

        # opening target
        logger.info(f"[target: {target}] Opening target")
        if not insta.open_target():
            logger.error(f'[target: {target}] Invalid tag or account')
            continue
        
        stats.accounts += 1
        # check if account is private
        private_account = insta.is_private()
        if private_account:
            stats.private_accounts += 1
            logger.info(f'[target: {target}] Private account')
        
        Story(insta, profile, is_private=private_account, logger=logger).interact(target, stats)
        Post(insta, profile, logger).interact(target, private_account, stats)
        Reel(insta, profile, logger).interact(target, private_account, stats)
        stats.save() 

    logger.info("Script finished successfully")
    stats.log()
    print(stats)

except Exception as ex:
    logger.error(f"Script ended with error")
    logger.error(f'Error: [{ex.__class__.__name__}] - {str(ex)}',exc_info=1)

finally:
    if insta:
        insta.quit()
    timediff = time.time() - start
    logger.info(f"Total time taken: {round(timediff, 4)} seconds")
    sys.exit()
    


