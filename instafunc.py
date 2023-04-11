""" 
    instafunc.py - function module for insta-likecom-bot

    insta-likecom-bot v.2.4
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar

    LICENSE: MIT
"""


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver import ActionChains

# Added for FireFox support
from webdriver_manager.firefox import GeckoDriverManager


import os
import re
import time
from datetime import datetime
from sys import platform

from applogger import AppLogger
from typing import List, Tuple
from functools import wraps



logger = AppLogger(__name__).getlogger()

# suppress webdriver manager logs
os.environ['WDM_LOG_LEVEL'] = '0'


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
            attempt +=  1
        return status
    return wrapper


class Insta:
    def __init__(self, username, password, timeout=30, browser='chrome', headless=False) -> None:
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
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager(path=os.path.join(self.driver_baseloc, 'firefox')).install(),
                options=options)
        # Chrome
        else:
            # Chrome Options
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--disable-notifications")
            options.add_argument("--start-maximized")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--log-level=3")
            
            if platform == 'linux' or platform == 'linux2':
                options.add_argument('--disable-dev-shm-usage')

            # current working directory/driver/chrome
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager(path=os.path.join(self.driver_baseloc, 'chrome')).install(),
                options=options)

        self.wait = WebDriverWait(self.driver, timeout)
        self.ac = ActionChains(self.driver)

        self.baseurl = "https://www.instagram.com"
        self.targeturl = self.baseurl
        self.username = username
        self.password = password
        self.tag = None
        self.account = None

    def target(self, accountname: str, tag: bool=False) -> None:
        """
        Loads the target - account or hastag
        """
        # account
        if not tag:
            self.account = accountname
            self.targeturl = f"{self.baseurl}/{accountname}"
        # tag
        else:
            self.tag = accountname
            self.targeturl = f"{self.baseurl}/explore/tags/{accountname}"

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
        user_profile_xpaths = [
            '//img[contains(@alt, " profile picture")]',
            '//div[@class="_acut"]/div/span/img',
            '//img[@data-testid="user-avatar"]'
        ]
        for xpath in user_profile_xpaths:
            try:
                logger.info(f'Validating login with xpath: {xpath}')
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                return True
            except:
                logger.error(f"Could not find user's profile with xpath: {xpath}")

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
                return 'skip_retry'
        except:
            return False
        return True

    def login(self) -> bool:
        """
        Initiates login with username and password
        """
        try:
            self.driver.get(self.baseurl)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(self.password)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
            if not self.validate_login():
                return False
        except:
            return False
        return True

    @retry
    def like(self) -> bool:
        """
        Likes a post if not liked already
        """
        like_button:WebElement = None
        try:
            # like_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="fr66n"]/button')))
            like_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_aamw"]/button')))
            like_button_span = like_button.find_element(By.XPATH, 'div/span')
            button_status = like_button_span.find_element(By.TAG_NAME, 'svg').get_attribute('aria-label')
            # like only if not already liked
            if button_status == 'Like':
                like_button.click()

        except ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', like_button)         
        except:
            return False
        return True
    
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
    def comment(self, text, timeout, max_retry, fs_comment = 'Perfect!') -> bool:
        """
        Comments on a post

        Args:
        timeout     wait until comment is posted
        max_retry   no. of times to try re-capturing comment textarea
        fs_comment  failsafe comment in case bmp_emoji_safe_text returns an empty string
        """

        cmt_text = text
        cmt: WebElement = None

        # remove non-bmp characters (for chrome)
        if self.browser == 'chrome':
            cmt_text = bmp_emoji_safe_text(text) or fs_comment

        # comment_success = False
        # retry_count = 0
        # while retry_count < max_retry and not comment_success:
        try:
            
            # cmt = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form[@class="_aidk"]/textarea')))
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
            # num_of_posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="g47SY "]'))).text
            # classname changed
            # num_of_posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[normalize-space(text())="posts"]/span'))).text
            # changed to class name as finding div with text 'posts' fails for different language
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
            logger.error(f'{ex.__class__.__name__} {str(ex)}')
            return False

    def dont_save_login_info(self) -> bool:
        """
        Clicks 'Not Now' button when prompted with 'Save Your Login Info?'
        """
        not_now_button_xpaths = [
            '//button[text()="Not now"]',
            '//div[@class="cmbtv"]/button',
            '//div[@class="_ac8f"]/button'
        ]
        for xpath in not_now_button_xpaths:
            try:
                logger.info(f'Finding Not Now button with xpath: {xpath}')
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                return True
            except:
                logger.error(f'Could not find Not Now button with xpath: {xpath}')
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
                return True        
            except:
                logger.info(f'Failed to find text: {text}')

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
    
    def like_comments(self, max_comments: int = 5) -> List[Tuple]:
        """
        Likes post comments
        """
        def comment_not_liked(com_el):
            """ Check if like button is not already clicked """
            try:
                # like button svg
                return com_el.find_element(By.CSS_SELECTOR, '._aamf svg')\
                    .get_attribute('aria-label').lower() == 'like'
            except Exception as ex:
                logger.error(str(ex))
                return False
            
        wait = WebDriverWait(self.driver, 5)
        try:
            comment_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='_a9ym']")))
        except Exception:
            return []
        
        if not comment_elements:
            return []
        
        successful_comments = []
        try:
            total_comments_liked = 0
            for com_el in comment_elements:
                if comment_not_liked(com_el):
                    # like button
                    com_el.find_element(By.CSS_SELECTOR, '._aamf').click()
                    successful_comments.append(self.get_user_and_comment_from_element(com_el))    
                    total_comments_liked += 1
                    time.sleep(0.5)
                else:
                    user,comment = self.get_user_and_comment_from_element(com_el)
                    logger.info(f'Already Liked: [({user}) - {comment}]')
                if total_comments_liked == max_comments: break

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

    def post_within_last(self, ts: float, multiplier: int, tparam: str = 'd') -> bool:
        """
        Checks if the post is within last n days
        """
        if not ts:
            return False
        if tparam.lower() == 'd':
            current_ts = datetime.now().timestamp()
            return current_ts - ts <= multiplier*60*60*24
        return False


def remove_blanks(lst: List) -> List:
    """
    Removes empty elements from a list
    """
    return [el for el in lst if el != '']


def remove_carriage_ret(lst) -> List:
    """
    Remove carriage return - \r from a list
    """
    return list(map(lambda el: el.replace('\r',''), lst))


def load_comments(fname: str) -> List:
    """
    Reads comments from a file and returns a list of comments
    """
    with open(fname,'rb') as fh:
        content = fh.read()
        lines = content.decode('utf-8').split('\n')
        comments = remove_carriage_ret(lines)
        comments = remove_blanks(comments)
        return comments


def load_matchtags(fname: str) -> List:
    """
    Returns list of tags from a file
    """
    tags = []
    try:
        with open(fname, 'r') as fh:
            tags = fh.read().split('\n')
            tags = [tag.strip() for tag in tags if tag != '']
    except Exception as ex:
        logger.error(f'{ex.__class__.__name__} {str(ex)}')
    return tags


def bmp_emoji_safe_text(text) -> str:
    """
    Returns bmp emoji safe text
    ChromeDriver only supports bmp emojis - unicode < FFFF
    """
    transformed = [ch for ch in text if ch <= '\uFFFF']
    return ''.join(transformed)


def scroll_into_view(driver, element) -> None:
    """
    Scrolls an element into view
    """
    driver.execute_script('arguments[0].scrollIntoView()', element)