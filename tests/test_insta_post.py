import time
import pytest
from .conftest import (
    INSTA_URL,
    TEST_INSTA_USER, 
    TEST_INSTA_PASS,
    TEST_INSTA_TARGET_USER,
    TEST_INSTA_TARGET_TAG, 
    NPOSTS, POST_TAGS,
    POST_DATE, POST_TIMESTAMP
)

def test_mandatory_params(insta):
    assert insta.baseurl == INSTA_URL
    assert insta.username == TEST_INSTA_USER
    assert insta.password == TEST_INSTA_PASS


@pytest.mark.skip("deprecated")
def test_targeturl_tag(insta):
    insta.target(accountname=TEST_INSTA_TARGET_TAG)
    assert insta.targeturl == f"{INSTA_URL}/explore/search/keyword/?q={TEST_INSTA_TARGET_TAG[1:]}"
    # https://www.instagram.com/explore/search/keyword/?q=<keyword here or tag>


def test_launch_insta(insta):
    status = insta.launch_insta()
    assert status == True
    assert insta.driver.current_url == f'{INSTA_URL}/'
    

def test_login(insta):
    assert insta.login() == True
    assert insta.validate_login() == True


def test_save_login_info(insta):
    assert insta.save_login_info() == True


def test_target_user(insta):
    insta.target(accountname=TEST_INSTA_TARGET_USER)
    assert insta.account == TEST_INSTA_TARGET_USER


@pytest.mark.skip('deprecated')
def test_target_tag(insta):
    insta.target(accountname=TEST_INSTA_TARGET_TAG)
    assert insta.tag == TEST_INSTA_TARGET_TAG[1:]


def test_targeturl_user(insta):
    insta.target(accountname=TEST_INSTA_TARGET_USER)
    assert insta.targeturl == f"{INSTA_URL}/{TEST_INSTA_TARGET_USER}"


def test_open_target(insta):
    insta.open_target() == True


def test_is_private(insta):
    insta.is_private() == False


def test_number_of_posts(insta):
    nposts = insta.get_number_of_posts()
    assert isinstance(nposts, int) == True
    assert nposts == NPOSTS


def test_open_first_post(insta):
    assert insta.click_first_post() == True


def test_next_post(insta):
    assert insta.next_post() == True


def test_get_post_tags(insta):
    tags = insta.get_post_tags()
    assert isinstance(tags, list) == True
    assert tags == POST_TAGS


def test_tag_match_count(insta):
    # default minimum match
    result = insta.get_tag_match_count(
        posttags=POST_TAGS,
        matchtags=['#basketballart','#basketball','#poetsofinstagram']
    )
    assert result == True

    # test minimum match
    result = insta.get_tag_match_count(
        posttags=POST_TAGS,
        matchtags=['#basketballart','#basketball','#idontexist'],
        min_match=2
    )
    assert result == True

    # test negative tag match
    result = insta.get_tag_match_count(
        posttags=POST_TAGS,
        matchtags=['#shouldmatch1','#shouldmatch2','#shouldmatch3'],
        min_match=2
    )
    assert result == False


def test_get_post_date(insta):
    postdate, ts = insta.get_post_date()
    assert isinstance(postdate, str) == True
    assert isinstance(ts, float) == True
    assert postdate == POST_DATE
    assert ts == POST_TIMESTAMP


@pytest.mark.skip('To be implemented')
def test_post_within_last(insta):
    pass


def test_is_comment_disabled(insta):
    assert insta.is_comment_disabled() == False


def test_comment(insta):
    result = insta.comment('This is a test', 5)
    assert result == True


def test_is_commented(insta):
    assert insta.is_commented() == True


def test_skip_post_already_commented(insta):
    skipcommented = True
    skip_post = all([skipcommented, insta.is_commented()])
    assert skip_post == True

    skipcommented = False
    comment_eligible = any([not skipcommented, all([skipcommented, not insta.is_commented()])])
    assert comment_eligible == True

    skipcommented = True
    comment_eligible = any([not skipcommented, all([skipcommented, not insta.is_commented()])])
    assert comment_eligible == False


def test_like_comments(insta):
    result = insta.like_comments()
    assert isinstance(result, list) == True
    assert result != []
    for user, comment in result:
        assert isinstance(user, str) == True
        assert isinstance(comment, str) == True
        

def test_like(insta):
    result = insta.like()
    assert result == True or result == None



# insta.driver.find_element(By.XPATH, '//a[contains(@href,"/denver/reels")]').click()
# //div[@class="_aajw"]