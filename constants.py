
from dotenv import load_dotenv
import os

INSTA_USER = None
INSTA_PASS = None
INSTA_TARGET = None

if os.path.exists('.env'):
    load_dotenv()
    INSTA_USER = os.getenv('INSTA_USER')
    INSTA_PASS = os.getenv('INSTA_PASS')
    INSTA_TARGET = os.getenv('INSTA_TARGET')

def getsettings() -> dict:
    """
    Returns constants as dict
    """
    global INSTA_USER
    global INSTA_PASS
    global INSTA_TARGET

    settings = {
        "username": INSTA_USER,
        "password": INSTA_PASS,
        "target": INSTA_TARGET
    }
    return settings

