
import pytest
from random import choice as rand_choice
from .conftest import INSTA_TARGET_STORY_USER


TEST_STORY_COMMENTS = [
    'It is beautiful', 'Wow!', "That's deep", 
    "Nicely expressed", 'love it', "That hit me", 
    "I'm gonna write this down"
]


def test_login(insta):
    if insta.validate_login() == True:
        assert True
    else:
        assert insta.login() == True
        

def test_open_target(insta):
    insta.target(accountname=INSTA_TARGET_STORY_USER)
    assert insta.open_target() == True


def test_is_story_present(insta):
    assert insta.is_story_present() == True


def test_open_and_pause_story(insta):
    assert insta.open_story() == True
    assert insta.pause_story() == True


def test_get_total_stories(insta):
    nstories = insta.get_total_stories()
    assert isinstance(nstories, int) == True
    assert nstories > 0


def test_like_story(insta):
    liked = insta.like_story()
    assert (liked == True or liked == None)


def test_comment_story(insta):
    assert insta.comment_on_story(rand_choice(TEST_STORY_COMMENTS)) == True


def test_next_story(insta):
    assert insta.next_story() == True

