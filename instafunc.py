
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

import time

class Insta:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.baseurl = "https://www.instagram.com"
        self.targeturl = self.baseurl
        self.username = None
        self.password = None
        self.tag = None
        self.account = None


    def user(self, username, password):
        """
        Loads user's Instagram username and password
        """
        self.username = username
        self.password = password


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


    def open_target(self, max_retry):
        """
        Opens the target account or hashtag
        """
        load_success = False
        retry_count = 0
        while retry_count < max_retry and not load_success:
            try:
                self.driver.get(self.targeturl)
                # if unable to load the page
                if not self.is_page_loaded():
                    print("** Open Target **: Unable to load the page. Retrying...")
                    retry_count += 1
                    time.sleep(1)

                # if not a valid account or tag
                elif not self.validate_target():
                    break
                else:
                    load_success = True
            except:
                break
        return load_success


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
            return True
        except:
            return False


    def like(self):
        """
        Likes a post if not liked already
        """
        try:
            like_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="fr66n"]/button')))
            like_button_span = like_button.find_element(By.XPATH, 'div/span')
            button_status = like_button_span.find_element(By.TAG_NAME, 'svg').get_attribute('aria-label')
            # like only if not already liked
            if button_status == 'Like':
                like_button.click()
            return True
        except:
            return False

    
    def comment(self, text, timeout, max_retry):
        """
        Comments on a post
        """
        comment_success = False
        retry_count = 0
        while retry_count < max_retry and not comment_success:
            try:
                cmt = self.wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Add a comment…"]')))
                cmt.click()
                cmt.send_keys(text)
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="post-comment-input-button"]'))).click()
                # self.driver.find_element(By.XPATH, '//button[@data-testid="post-comment-input-button"]').click()
                
                start = time.time()
                end = 0
                while cmt.text != '' and (end - start) < timeout:
                    end = time.time()

                comment_success = True
            except StaleElementReferenceException:
                print("** Comment **: Couldn't capture the comment field. Re-capturing")
                retry_count += 1
        return comment_success
    

    def get_number_of_posts(self):
        """
        Returns number of post for an account or tag
        """
        try:
            num_of_posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="g47SY "]'))).text
            num_of_posts = num_of_posts.replace(',','')
            return int(num_of_posts)
        except:
            return None
    

    def click_first_post(self):
        """
        Clicks on the first post found for an account
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="v1Nh3 kIKUG _bz0w"]'))).click()
            return True
        except:
            return False
    

    def dont_save_login_info(self):
        """
        Clicks 'Not Now' button when prompted with 'Save Your Login Info?'
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Not Now"]'))).click()
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