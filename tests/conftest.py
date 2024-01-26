
import pytest
import os
from dotenv import load_dotenv
from modules.constants import INSTA_URL
from modules.insta import *

load_dotenv('.env')

TEST_INSTA_USER = os.getenv('INSTA_USER', '')
TEST_INSTA_PASS = os.getenv('INSTA_PASS', '')
TEST_INSTA_TARGET_USER = os.getenv('INSTA_TARGET_USER', '')
INSTA_TARGET_STORY_USER = os.getenv('INSTA_TARGET_STORY_USER', '')
INSTA_TARGET_REEL_USER = os.getenv('INSTA_TARGET_REEL_USER', '')
TEST_INSTA_TARGET_TAG = os.getenv('INSTA_TARGET_TAG', '')
NPOSTS = int(os.getenv('NPOSTS', ''))

POST_TAGS = os.getenv('POST_TAGS', '').split(',')

POST_DATE = os.getenv('POST_DATE', '')
POST_TIMESTAMP = float(os.getenv('POST_TIMESTAMP', 0.0))

TEST_INSTA = Insta(
        username=TEST_INSTA_USER,
        password=TEST_INSTA_PASS
    )


@pytest.fixture
def insta():
    return TEST_INSTA

