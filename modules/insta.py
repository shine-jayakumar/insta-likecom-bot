""" 
    insta.py - Insta class and helper methods

    insta-likecom-bot v.3.0.4
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
# Added for FireFox support
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver import ActionChains


import os
import re
import time
from datetime import datetime
from sys import platform
import sys

from modules.applogger import AppLogger
from typing import List, Tuple
from functools import wraps
from enum import Enum
from modules.constants import INSTA_URL
from modules.helpers import *


logger = AppLogger(__name__).getlogger()

# suppress webdriver manager logs
os.environ['WDM_LOG_LEVEL'] = '0'


class Seconds(Enum):
    Year: int = 31536000
    Month: int = 2592000
    Day: int = 86400
    Hour: int = 3600
    Min: int = 60
    Sec: int = 1


class TParam(Enum):
    y: str = 'year'
    M: str = 'month'
    d: str = 'day'
    h: str = 'hour'
    m: str = 'min'
    s: str = 'sec'



def retry(func):
    """
    Adds retry functionality to functions
    """
    # wrapper function
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_tries = 5
        attempt = 1
        status = False
        while not status and attempt < max_tries:
            logger.info(f'[{func.__name__}]: Attempt - {attempt}')
            status = func(*args, **kwargs)
            if status == 'skip_retry':
                status = False
                break         
            if status == None:
                break           
            attempt +=  1
        return status
    return wrapper


class Insta:
    def __init__(self, username, password, timeout=30, browser='chrome', headless=False, profile:str = None) -> None:

        # current working directory/driver
        self.browser = 'chrome'
        self.driver_baseloc = os.path.join(os.getcwd(), 'driver')
        self.comment_disabled = False

        # Firefox
        if browser.lower() == 'firefox':
            self.browser = 'firefox'
            # Firefox Options
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.set_preference("dom.webnotifications.enabled", False)
            options.log.level = 'fatal'

            # current working directory/driver/firefox
            # self.driver = webdriver.Firefox(
            #     executable_path=GeckoDriverManager(path=os.path.join(self.driver_baseloc, 'firefox')).install(),
            #     options=options)
            self.driver = None
            try:
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            except Exception as webdriver_ex:
                logger.error(f'[Driver Download Manager Error]: {str(webdriver_ex)}')
                sys.exit(1)

        # Chrome
        else:
            # Chrome Options
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            if profile:
                options.add_argument(f'user-data-dir={profile}')
            options.add_argument("--disable-notifications")
            options.add_argument("--start-maximized")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--log-level=3")
            
            if platform == 'linux' or platform == 'linux2':
                options.add_argument('--disable-dev-shm-usage')

            # current working directory/driver/chrome
            self.driver = None
            try:
                # self.driver = webdriver.Chrome(
                #     executable_path=ChromeDriverManager(path=os.path.join(self.driver_baseloc, 'chrome')).install(),
                #     options=options)
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

            except Exception as webdriver_ex:
                logger.error(f'[Driver Download Manager Error]: {str(webdriver_ex)}')
                sys.exit(1)
                
        self.wait = WebDriverWait(self.driver, timeout)
        self.ac = ActionChains(self.driver)

        self.baseurl = INSTA_URL
        self.targeturl = self.baseurl
        self.username = username
        self.password = password
        self.tag = None
        self.account = None

    def target(self, accountname: str, tag: bool=False) -> None:
        """
        Loads the target - account or hastag
        """
        if accountname.startswith('#'):
            self.tag = accountname[1:]
            self.targeturl = f"{self.baseurl}/explore/tags/{accountname[1:]}"
        else:
            self.account = accountname
            self.targeturl = f"{self.baseurl}/{accountname}"

    def validate_target(self) -> bool:
        """
        Validates the target account or hashtag
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[text()="{self.account or self.tag}"]')))
            return True
        except:
            return False

    def validate_login(self) -> bool:
        """
        Validates login
        """
        wait = WebDriverWait(self.driver, 5)
        user_profile_xpaths = [
            '//img[contains(@alt, " profile picture")]',
            '//div[@class="_acut"]/div/span/img',
            '//img[@data-testid="user-avatar"]'
        ]
        for atmpt_cnt, xpath in enumerate(user_profile_xpaths, start=1):
            try:
                logger.info(f'[Attempt# {atmpt_cnt}] Validating login')
                wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                return True
            except:
                logger.error(f'Failed to validate login')

        return False

    def is_page_loaded(self) -> bool:
        """
        Checks if page is loaded successfully
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            return True
        except:
            return False

    @retry
    def open_target(self) -> bool:
        """
        Opens the target account or hashtag
        """
        try:
            self.driver.get(self.targeturl)
            # if unable to load the page
            if not self.is_page_loaded():
                logger.info("[open_target] Unable to load the page. Retrying...")
                time.sleep(1)
                return False

            # if not a valid account or tag
            elif not self.validate_target():
                logger.error('Failed to validate target')
                return False
        except:
            return False
        return True
    
    @retry
    def launch_insta(self) -> bool:
        """
        Opens instagram
        """
        try:
            self.driver.get(self.baseurl)
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
            return False
        return True
    
    def login(self, validate=True) -> bool:
        """
        Initiates login with username and password
        """
        try:
            self.driver.get(self.baseurl)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(self.password)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()

            if self.is_2factor_present():
                logger.info('2 factor authentication active. Enter your authentication code to continue')
                time.sleep(10)

            if validate:
                if not self.validate_login():
                    return False
        except:
            return False
        return True

    @retry
    def like(self) -> bool | None:
        """
        Likes a post if not liked already
        """
        like_button:WebElement = None
        wait = WebDriverWait(self.driver, timeout=2)
        try:
            like_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_aamw"]')))
            like_button_span = like_button.find_element(By.XPATH, 'div/div/span')
            button_status = like_button_span.find_element(By.TAG_NAME, 'svg').get_attribute('aria-label')
            # like only if not already liked
            if button_status == 'Like':
                like_button.click()
                return True

        except ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', like_button)         
        except Exception as ex:
            print(str(ex))
            return False
        return None
    
    def wait_until_comment_cleared(self, element, timeout) -> None:
        """
        Waits until the comment textarea is cleared, or until timeout
        """
        start = time.time()
        end = 0
        # wait until posted or until timeout
        while element.text != '' and (end - start) < timeout:
            end = time.time()
    
    def is_comment_disabled(self) -> bool:
        """
        Checks if comment is disabled or not
        """
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[normalize-space(text())="Comments on this post have been limited."]')))
            wait = WebDriverWait(self.driver, timeout=1)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_ae63"]')))
            self.comment_disabled = True
            return True
        except:
            return False

    @retry
    def comment(self, text, timeout, fs_comment = 'Perfect!') -> bool:
        """
        Comments on a post

        Args:
        timeout     wait until comment is posted
        fs_comment  failsafe comment in case bmp_emoji_safe_text returns an empty string
        """

        cmt_text = text
        cmt: WebElement = None

        # remove non-bmp characters (for chrome)
        if self.browser == 'chrome':
            cmt_text = bmp_emoji_safe_text(text) or fs_comment

        try:
            # cmt = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form[@class="_aao9"]/textarea')))
            cmt = self.wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Add a comment…"]')))
            cmt.click()
            cmt.send_keys(cmt_text)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and contains(@class,"_acan")]'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and contains(text(), "Post")]'))).click()
            self.wait_until_comment_cleared(cmt, timeout)

        except ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', cmt)
            self.wait_until_comment_cleared(cmt, timeout)

        except:
            return False

        return True
    
    def get_number_of_posts(self) -> int:
        """
        Returns number of post for an account or tag
        """
        try:
            num_of_posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_ac2a"]'))).text
            num_of_posts = num_of_posts.replace(',','')
            return int(num_of_posts)
        except:
            return None

    def click_first_post(self) -> bool:
        """
        Clicks on the first post found for an account
        """
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="v1Nh3 kIKUG _bz0w"]'))).click()
            # classname changed
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"_aagw")]'))).click()
            return True
        except:
            return False

    def click_first_post_most_recent(self) -> bool:
        """
        Clicks on the first post under most recent
        """
        try:
            # most recent div
            most_recent_div_el = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//h2[contains(text(),"Most recent")]//following-sibling::div')))
            # first post
            most_recent_div_el.find_element(By.CSS_SELECTOR, '._aagw').click()
            return True
        except Exception as ex:
            logger.error(f'[most_recent] Error: {ex.__class__.__name__}')
            return False

    def dont_save_login_info(self) -> bool:
        """
        Clicks 'Not Now' button when prompted with 'Save Your Login Info?'
        """
        wait = WebDriverWait(self.driver, timeout=2)
        not_now_button_xpaths = [
            '//button[text()="Not now"]',
            '//div[@class="cmbtv"]/button',
            '//div[@class="_ac8f"]/button',
            '//div[text()="Not now"]'
        ]
        for xpath in not_now_button_xpaths:
            try:
                logger.info(f'Finding Not Now button with xpath: {xpath}')
                wait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                return True
            except:
                logger.error(f'Could not find Not Now button with xpath: {xpath}')
        return False
    
    def save_login_info(self) -> bool:
        """
        Saves login information
        """
        wait = WebDriverWait(self.driver, 2)
        xpaths = [
            '//button[contains(text(),"Save Info")]',
            '//button[contains(text(),"Save info")]'
        ]
        for xpath in xpaths:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                return True
            except:
                logger.error(f'Save Login Info dialog box not found')
        return False

    def next_post(self) -> bool: 
        """
        Moves to the next post
        """
        try:
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)
            return True
        except:
            return False

    def is_private(self) -> bool:
        """
        Checks if an account is private
        """
        private_text_indicator = [
            'This account is private',
            'This Account is private',
            'This Account is Private'            
        ]
        for text in private_text_indicator:
            try:
                self.driver.find_element(By.XPATH, f'//*[text()="{text}"]')
                logger.info(f'[is_private] text=>({text}) found.')
                return True        
            except:
                logger.info(f'[is_private]: text=>({text}) not found')
        return False
    
    def is_2factor_present(self) -> bool:
        """
        Checks if 2 factor verification screen is present
        """
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="verificationCodeDescription"]')))
            return True
        except Exception as ex:
            logger.error('Could not locate 2 factor authentication screen')
        return False

    def quit(self) -> None:
        """
        Quit driver
        """
        try:
            self.driver.quit()
        except Exception as ex:
            logger.error(f'Failed to close browser: {str(ex)}')
    
    def extract_username(self, text: str) -> str:
        """
        Extracts username from text
        """
        if not text:
            return None

        username = text.split('https://www.instagram.com')[1]
        username = username.split('/')[1]
        return username

    def get_followers(self, amount: int = None) -> List:
        """
        Gets followers from the target's page
        """
        if amount:
            logger.info(f'Restricting followers search to: {amount}')
            
        logger.info('Opening followers list')
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/followers")]'))).click()
        followers_div = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_aano"]/div/div')))

        # holds extracted usernames
        usernames = []

        div_read_start = 0
        div_read_end = 0

        num_previous_div = 0
        num_updated_div = 1

        time.sleep(3)

        running = True

        while(num_updated_div > num_previous_div and running):    

            logger.info('Getting updated list of username divs')
            username_links = None

            max_tries = 5
            tries = 0
            did_not_find_more_divs = True

            while tries < max_tries and did_not_find_more_divs:
                try:
                    # user_divs = followers_div.find_elements(By.TAG_NAME, 'div')
                    username_links = followers_div.find_elements(By.TAG_NAME, 'a')
                    num_previous_div = num_updated_div
                    num_updated_div = len(username_links)
                    if num_updated_div > num_previous_div:
                        did_not_find_more_divs = False
                    else:
                        logger.info('Scrolling')
                        scroll_into_view(self.driver, username_links[-1])
                        time.sleep(2)
                        tries += 1

                except StaleElementReferenceException:
                    logger.error(f'StaleElementReferenceException exception occured while capturing username links')
                    logger.info("Capturing div containing followers' list")
                    followers_div = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_aano"]/div/div')))
                    time.sleep(2)
    
            
            div_read_start = div_read_end
            div_read_end = len(username_links)
            
            logger.info(f'Processing userdiv range: {div_read_start} - {div_read_end}')
            for i in range(div_read_start, div_read_end):
                # get all text from the div
                # alltext = user_divs[i].text
                username_link = username_links[i].get_attribute('href')
                username = self.extract_username(username_link)

                # add found username to the list
                if username and username not in usernames:
                    usernames.append(username)

                # check if we have reached the desired amount
                if amount is not None and len(usernames) >= amount:
                    running = False
                    break
                    
            logger.info(f'Total username count: {len(usernames)}')
            logger.info('Scrolling')
            scroll_into_view(self.driver, username_links[-1])
            time.sleep(3)
        
        return usernames
    
    def get_post_tags(self) -> List:
        """
        Gets tags present in current post
        """
        tags = []
        try:
            tags_links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/explore/tags")]')
            tags = [taglink.text for taglink in tags_links]
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
        return tags
    
    def get_tag_match_count(self, posttags: List, matchtags: List, min_match: int = 3) -> bool:
        """
        Checks if a minimum number of tags in matchtags match in
        tags from post
        """
        if not all([posttags, matchtags]):
            return False
        return sum([tag in posttags for tag in matchtags]) >= min_match

    def get_comment_usernames_from_post(self) -> List[str]:
        """
        Returns usernames for comments on a post
        """
        wait = WebDriverWait(self.driver, 2)
        usernames = []
        try:
            comment_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='_a9ym']")))
            for comment_el in comment_elements:
                usernames.append(comment_el.find_element(By.CSS_SELECTOR, '._a9zc').text)
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
        return list(set(usernames))

    def get_user_and_comment_from_element(self, comment_el) -> Tuple:
        """
        Returns username and their comment from a comment element
        """
        if not comment_el:
            return ('','')
    
        username = ''
        comment = ''
        try:
            username = comment_el.find_element(By.CSS_SELECTOR, '._a9zc').text
            comment = comment_el.find_element(By.CSS_SELECTOR, '._a9zs').text
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
        return (username, comment)

    def is_commented(self) -> bool:
        """
        Checks if a post already has a comment from the user
        """
        usernames = self.get_comment_usernames_from_post()        
        if not usernames:
            return False
        if self.username not in usernames:
            return False
        return True
    
    def like_comments(self, max_comments: int = 5) -> List[Tuple]:
        """
        Likes post comments
        """
        def comment_not_liked(com_el):
            """ Check if like button is not already clicked """
            try:
                # like button svg
                 return com_el.find_element(By.CSS_SELECTOR, '._a9zu svg')\
                    .get_attribute('aria-label').lower() == 'like'
            except Exception as ex:
                logger.error(str(ex))
                return False
            
        wait = WebDriverWait(self.driver, 5)
        try:
            comment_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='_a9ym']")))
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
            return []
        
        if not comment_elements:
            return []
        
        successful_comments = []
        try:
            total_comments_liked = 0
            for com_el in comment_elements:
                if comment_not_liked(com_el):
                    # like button
                    com_el.find_element(By.CSS_SELECTOR, '._a9zu').click()
                    successful_comments.append(self.get_user_and_comment_from_element(com_el))    
                    total_comments_liked += 1
                    time.sleep(0.5)
                else:
                    user,comment = self.get_user_and_comment_from_element(com_el)
                    logger.info(f'Already Liked: [({user}) - {comment}]')
                if total_comments_liked == max_comments: 
                    break

        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
        return successful_comments

    def get_post_date(self) -> Tuple[str,float]:
        """
        Returns post date (%Y-%m-%d %H:%M:%S, timestamp)
        """
        try:
            dt = self.driver.find_element(By.XPATH, '//time[@class="_aaqe"]').get_attribute('datetime')
            if not dt:
                logger.error('Date not found (xpath: //time[@class="_aaqe"])')
                return ('','')
            # %Y-%m-%d %H:%M:%S
            fmt_dt = re.sub(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}).+', r'\1 \2', dt)
            ts = datetime.strptime(fmt_dt, '%Y-%m-%d %H:%M:%S').timestamp()
            return (fmt_dt, ts)
        except Exception as ex:
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
        return ('','')

    def post_within_last(self, ts: float, multiplier: int, tparam: str) -> bool:
        """
        Checks if the post is within last n days
        """
        if not ts:
            return False
        current_ts = datetime.utcnow().timestamp()
 
        if tparam == 'y': return current_ts - ts <= multiplier * Seconds.Year.value
        if tparam == 'M': return current_ts - ts <= multiplier * Seconds.Month.value
        if tparam == 'd': return current_ts - ts <= multiplier * Seconds.Day.value
        if tparam == 'h': return current_ts - ts <= multiplier * Seconds.Hour.value
        if tparam == 'm': return current_ts - ts <= multiplier * Seconds.Min.value
        if tparam == 's': return current_ts - ts <= multiplier * Seconds.Sec.value

        return False

    def is_story_present(self):
        """
        Checks if story is present
        """
        wait = WebDriverWait(self.driver, 5)
        try:
            is_disabled = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_aarf")]'))).get_attribute('aria-disabled')
            return is_disabled == 'false'
        except Exception as ex:
            logger.error(f'[is_story_present] Could not locate story')
        return False

    def open_story(self) -> bool:
        """
        Opens story for a user
        """
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, f'//img[contains(@alt, "{self.account}")]'))).click()
            return True
        except Exception as ex:
            logger.error(f'[open_story] Error: {ex.__class__.__name__}')
        return False
    
    def pause_story(self) -> bool:
        """
        Pauses a story
        """
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac0m'))).find_element(By.CSS_SELECTOR, 'svg[aria-label="Pause"]').click()
            return True
        except Exception as ex:
            logger.error(f'[pause_story] Error: {ex.__class__.__name__}')
        return False
    
    def like_story(self) -> bool | None:
        """
        Pauses a story
        """
        wait = WebDriverWait(self.driver, 2)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._abx4'))).find_element(By.CSS_SELECTOR, 'svg[aria-label="Like"]').click()
            return True
        except Exception as ex:
            if self.driver.find_element(By.CSS_SELECTOR, '._abx4').find_element(By.CSS_SELECTOR, 'svg[aria-label="Unlike"]'):
                logger.info('[like_story]: Already liked')
                return None
            logger.error(f'[like_story] Error: {ex.__class__.__name__}')
        return False

    def next_story(self):
        """
        Moves to next story
        """
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Next")]'))).click()
            return True
        except Exception as ex:
            logger.error(f'[next_story] Error: {ex.__class__.__name__}')
        return False
    
    def get_total_stories(self) -> int:
        """
        Get total stories
        """
        wait = WebDriverWait(self.driver, 10)
        try:
            return len(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac3r')))
                       .find_elements(By.CSS_SELECTOR, '._ac3n'))
        except Exception as ex:
            logger.error(f'[get_total_stories] Error: {ex.__class__.__name__}')
        return 0
    
    def comment_on_story(self, text) -> bool:
        """
        Comments on a story
        """
        wait = WebDriverWait(self.driver, 10)
        try:

            cmt = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac12'))).find_element(By.CSS_SELECTOR, '._abx2')
            cmt.click()
            time.sleep(0.5)
            cmt.send_keys(text)
            cmt.send_keys(Keys.ENTER)
            return True
        except Exception as ex:
            logger.error(f'[comment_on_story] Error: {ex.__class__.__name__}')
        return False
    
    def is_reels_present(self):
        """
        Checks if reels is present for an account
        """
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, f'//a[contains(@href,"{self.account}/reels")]')))
            return True
        except Exception as ex:
            logger.error(f'[is_reels_present] Could not find reels')
        return False

    def open_reels(self):
        """
        Opens reels page
        """
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, f'//a[contains(@href,"{self.account}/reels")]'))).click()
            return True
        except:
            logger.error(f'[open_reels] Failed to open reels page')
        return False
    
    def click_first_reel(self):
        """
        Clicks on the first reel found on the account
        """
        try:
            reels = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_aajw"]')))
            reels[0].click()
            return True
        except:
            logger.error(f'[click_first_reels] Failed to open first reel')
        return False

    def next_reel(self):
        """
        Moves to the next reel
        """
        try:
            self.next_post()
            return True
        except:
            logger.error('[next_reel] Failed to move to the next reel')
        return False
    
    def like_reel(self):
        """
        Likes a reel
        """
        try:
            self.like()
            return True
        except:
            logger.error(f'[like_reel] Failed to like reel')
        return False

    def comment_on_reel(self, text: str, timeout: int):
        """
        Comments on a reel
        """
        try:
            self.comment(text=text, timeout=timeout)
            return True
        except Exception as ex:
            logger.error('[comment_on_reel] Failed to comment on the reel')
        return False

    def like_reel_comments(self, max_comments: int = 5):
        """
        Likes comments on a reel
        """
        try:
            self.like_comments(max_comments=max_comments)
            return True
        except Exception as ex:
            logger.error('[like_reel_comments] Failed to comment on the reel')
        return False
        

