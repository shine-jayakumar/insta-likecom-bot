
import re
import random

def parse_delay(delay:str, default: tuple = (1,10)) -> tuple:
    """
    Parses delay value and returns start and end range
    """
    if not delay:
        return default

    match = re.match(r'(\d+),\s*(\d+)', delay)
    if match:
        st, en = map(int, match.groups())
        if st > en:
            return ()
        if max(st,en) > 100 or min(st,en) < 1:
            return ()
        return (st, en)
    
    match = re.match(r'\d+', delay)
    if match:
        st = int(match.group(0))
        return (st,) if st > 0 and st <= 100 else default
    return default 

def get_delay(delay: tuple, default: tuple = (1,10)):
    """ Returns a random delay value between (st,en) """
    if not delay:
        return random.randint(default[0], default[1])
    if len(delay) < 2:
        return delay[0]
    return random.randint(delay[0], delay[1])

# delay = parse_delay('4,4')
# print(delay)

print(get_delay((2,10)))