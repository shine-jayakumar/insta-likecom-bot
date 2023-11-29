
from typing import List, Tuple
import random
from modules.constants import APP_VERSION


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


def get_delay(delay: tuple, default: tuple = (1,10)) -> Tuple[int]:
    """ Returns a random delay value between (st,en) """
    if not delay:
        return random.randint(default[0], default[1])
    if len(delay) < 2:
        return delay[0]
    return random.randint(delay[0], delay[1])


def get_random_index(total_items: int, nreq: int, all_specifier=111) -> list:
    """
    Generates random index numbers based on value of argname
    """
    if not nreq:
        return []
    if nreq == all_specifier or nreq > total_items:
        nreq = total_items
    return random.sample(range(total_items), nreq)


def generate_random_comment(comments):
    """
    Returns a random comment from a list of comments
    """
    return comments[random.randint(0, len(comments)-1)]


def display_intro():

    intro = f"""
     ___ _  _ ___ _____ _      _    ___ _  _____ ___ ___  __  __     ___  ___ _____ 
    |_ _| \| / __|_   _/_\ ___| |  |_ _| |/ | __/ __/ _ \|  \/  |___| _ )/ _ |_   _|
     | || .` \__ \ | |/ _ |___| |__ | || ' <| _| (_| (_) | |\/| |___| _ | (_) || |  
    |___|_|\_|___/ |_/_/ \_\  |____|___|_|\_|___\___\___/|_|  |_|   |___/\___/ |_|  
    
    insta-likecom-bot {APP_VERSION}
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
    
    """
    print(intro)