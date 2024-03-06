
import pytest
from random import choice as rand_choice
from .conftest import INSTA_TARGET_REEL_USER


TEST_STORY_COMMENTS = [
    'It is beautiful', 'Wow!', 
    "Nice!", 'love it', "Amazing"
]

def test_login(insta):
    if insta.validate_login() == True:
        assert True
    else:
        assert insta.login() == True


def test_open_target(insta):
    insta.target(accountname=INSTA_TARGET_REEL_USER)
    assert insta.open_target() == True


def test_is_reels_present(insta):
    assert insta.is_reels_present() == True


def test_open_reel(insta):
    assert insta.open_reels() == True


def test_click_first_reel(insta):
    assert insta.click_first_reel() == True


def test_like_reel(insta):
    assert insta.like_reel() == True


def test_comment_reel(insta):
    assert insta.comment_on_reel(rand_choice(TEST_STORY_COMMENTS), 5) == True


def test_next_reel(insta):
    assert insta.next_reel() == True


def test_like_reel_comments(insta):
    assert insta.like_reel_comments() == True


