
""" 
    constants.py - contains constants

    insta-likecom-bot v.3.0.4
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

from dotenv import load_dotenv
import os


APP_VERSION = 'v.3.0.4'


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


COMMENTS = ["My jaw dropped", "This is amazing", "Awe-inspiring", "Sheeeeeeesh!","Out of this world",
"So beautiful ❤️", "So perfect ❤️", "Oh my lawd 😍", "I love this ❤️", "🔥🔥🔥", "👏👏",
"Beyond amazing 😍", "You’re the goat", "This is fire 🔥", "Keep grinding 💪", "Insane bro 🔥",
"The shocker! 😮", "Such a beauty 😍❤️", "Hell yeah 🔥", "Straight like that! 🔥", "Classy dude",
"Keep doing what you doing 🙌", "Freaking gorgeous 😍", "Keep going 💪", "You’re fabulous ❤️",
"This made my day 😍", "You’re literally unreal 😮", "I'm so obssessed", "Always popping off",
"Just like that 🔥", "Good vibes only ❤️", "This is mood ❤️", "The vibes are immaculate", "I adore you 🌺",
"You never fail to impress me😩", "These are hard 🔥", "Slaying as always 😍", "Blessing my feed rn 🙏",
"This is incredible ❤️", "Vibes on point 🔥", "You got it 🔥", "Dope!", "This is magical! ✨"]
