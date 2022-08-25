""" 
    instafunc.py - function module for insta-likecom-bot

    insta-likecom-bot v.1.4
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

# Added for FireFox support
from webdriver_manager.firefox import GeckoDriverManager

import os
import time


# suppress webdriver manager logs
os.environ['WDM_LOG_LEVEL'] = '0'


def retry(func):
    """
    Adds retry functionality to functions
    """
    # wrapper function
    def wrapper(*args, **kwargs):
        max_tries = 5
        attempt = 1
        status = False
        while not status and attempt < max_tries:
            print(f'[{func.__name__}]: Attempt - {attempt}')
            status = func(*args, **kwargs)
            if status == 'skip_retry':
                status = False
                break                    
            attempt +=  1
        return status
    return wrapper


class Insta:
    def __init__(self, username, password, timeout=30, browser='chrome', headless=False):
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
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--log-level=3")

            # current working directory/driver/chrome
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager(path=os.path.join(self.driver_baseloc, 'chrome')).install(),
                options=options)

        self.wait = WebDriverWait(self.driver, timeout)
        self.baseurl = "https://www.instagram.com"
        self.targeturl = self.baseurl
        self.username = username
        self.password = password
        self.tag = None
        self.account = None

    def target(self, accountname, tag=False):
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

    def validate_target(self):
        """
        Validates the target account or hashtag
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[text()="{self.account or self.tag}"]')))
            return True
        except:
            return False

    def validate_login(self):
        """
        Validates login
        """
        try:
            # look for user avatar
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//img[@data-testid="user-avatar"]')))
            return True
        except:
            return False

    def is_page_loaded(self):
        """
        Checks if page is loaded successfully
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            return True
        except:
            return False

    @retry
    def open_target(self):
        """
        Opens the target account or hashtag
        """
        try:
            self.driver.get(self.targeturl)
            # if unable to load the page
            if not self.is_page_loaded():
                print("** Open Target **: Unable to load the page. Retrying...")
                time.sleep(1)
                return False

            # if not a valid account or tag
            elif not self.validate_target():
                return 'skip_retry'
        except:
            return False
        return True

    def login(self):
        """
        Initiates login with username and password
        """
        try:
            self.driver.get(self.baseurl)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Log In"]'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(self.password)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
            if not self.validate_login():
                return False
        except:
            return False
        return True

    @retry
    def like(self):
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
    
    def wait_until_comment_cleared(self, element, timeout):
        """
        Waits until the comment textarea is cleared, or until timeout
        """
        start = time.time()
        end = 0
        # wait until posted or until timeout
        while element.text != '' and (end - start) < timeout:
            end = time.time()
    
    def is_comment_disabled(self):
        """
        Checks if comment is disabled or not
        """
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[normalize-space(text())="Comments on this post have been limited."]')))
            wait = WebDriverWait(self.driver, timeout=1)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_aasr"]/div')))
            self.comment_disabled = True
            return True
        except:
            return False

    @retry
    def comment(self, text, timeout, max_retry, fs_comment = 'Perfect!'):
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
            cmt = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form[@class="_aao9"]/textarea')))
            # cmt = self.wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Add a comment…"]')))
            cmt.click()
            cmt.send_keys(cmt_text)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="post-comment-input-button"]'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and contains(@class,"_acan")]'))).click()
            self.wait_until_comment_cleared(cmt, timeout)

        except ElementClickInterceptedException:
            self.driver.execute_script('arguments[0].click();', cmt)
            self.wait_until_comment_cleared(cmt, timeout)

        except:
            return False

        return True
    
    def get_number_of_posts(self):
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

    def click_first_post(self):
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

    def dont_save_login_info(self):
        """
        Clicks 'Not Now' button when prompted with 'Save Your Login Info?'
        """
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Not Now"]'))).click()
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cmbtv button'))).click()
            return True
        except:
            return False

    def next_post(self): 
        """
        Moves to the next post
        """
        try:
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)
            return True
        except:
            return False

    def is_private(self):
        """
        Checks if an account is private
        """
        try:
            self.driver.find_element(By.XPATH, '//*[text()="This Account is Private"]')
            return True        
        except:
            return False

    def quit(self):
        """
        Quit driver
        """
        try:
            self.driver.quit()
        except:
            print("** Failed to close browser**")


def remove_blanks(lst):
    """
    Removes empty elements from a list
    """
    return [el for el in lst if el != '']


def remove_carriage_ret(lst):
    """
    Remove carriage return - \r from a list
    """
    return list(map(lambda el: el.replace('\r',''), lst))


def load_comments(fname):
    """
    Reads comments from a file and returns a list of comments
    """
    with open(fname,'rb') as fh:
        content = fh.read()
        lines = content.decode('utf-8').split('\n')
        comments = remove_carriage_ret(lines)
        comments = remove_blanks(comments)
        return comments


def bmp_emoji_safe_text(text):
    """
    Returns bmp emoji safe text
    ChromeDriver only supports bmp emojis - unicode < FFFF
    """
    transformed = [ch for ch in text if ch <= '\uFFFF']
    return ''.join(transformed)



