     ___ _  _ ___ _____ _      _    ___ _  _____ ___ ___  __  __     ___  ___ _____ 
    |_ _| \| / __|_   _/_\ ___| |  |_ _| |/ | __/ __/ _ \|  \/  |___| _ )/ _ |_   _|
     | || .` \__ \ | |/ _ |___| |__ | || ' <| _| (_| (_) | |\/| |___| _ | (_) || |  
    |___|_|\_|___/ |_/_/ \_\  |____|___|_|\_|___\___\___/|_|  |_|   |___/\___/ |_| 

# insta-likecom-bot
![MIT License](https://img.shields.io/github/license/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL)

### Automates likes and comments on an instagram account or tag

insta-likecom-bot is an instagram bot written in python to automatically like and comment on an account or tag.

**Table of Contents**
- [Features](#Features "Features")
- [Requirements](#Requirements "Requirements")
- [Installation](#Installation "Installation")
- [Options](#Options "Options")
- [Usage](#Usage "Usage")
- [Examples](#Examples "Examples")
- [License](#LICENSE "License")

## Features
- Likes and Comments on all the posts for an account/tag
- Specify the number of posts to like
- Comes loaded with generic comments
- Load your own comments
- Comments supports emojis
- Add a PS to the comments
- Skip comments and just like a post
- Build in random time delays
- Specify time delays after each post
- CrazyMode to like and post comments with minimum delay

## Requirements
- Python 3
- Chrome Browser

View the [requirements.txt](https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/requirements.txt)

## Installation
```sh
pip install -r requirements.txt
```
## Options
| Option | Description |
| ------ | ------ |
| -u | Instagram username |
| -p | Instagram password |
| -t | target instagram account or hashtag (ex: -t someaccount11 or -t #haiku) |
| -pn | number of posts to like (ex: -pn 30) (optional) |
| -ps | add a text to the end of a comment (ex: -ps "check out my page @someaccount11") (optional) |
| -comments | file with comments. Only 1 comment per line (optional) |
| -crazy | runs with minimum delay between each posts. 1 - on, 0 - off (default) (ex: -crazy 1) (optional) |
| -delay | delay between each post in seconds (ex: -delay 3). Has no affect when -crazy is set (optional) |

## Usage
**To like and comment every post**
```
instalikecombot.py -u <username> -p <password> -t <target>
```
    
**To specify number of posts to like**
```
instalikecombot.py -u <username> -p <password> -t <target> -pn <no_of_posts>
```
    
**To specify a delay**
```
instalikecombot.py -u <username> -p <password> -t <target> -delay <delay_in_seconds>
```

**To specify a file with comments**
```
instalikecombot.py -u <username> -p <password> -t <target> -comments <comment_file>
```

**To add a text to the end of a comment**
```
instalikecombot.py -u <username> -p <password> -t <target> -ps "text"
```

**To leave no comments**
```
instalikecombot.py -u <username> -p <password> -t <target> -nocom 1
```

**To run in crazymode**
```
instalikecombot.py -u <username> -p <password> -t <target> -crazy 1
```

## Examples
```
instalikecombot.py -u randomjack01 -p somePASSWw0@d -t #haiku
```
```
instalikecombot.py -u randomjack01 -p somePASSWw0@d -t somerandomaccount032 -pn 10 -crazy 1
```
```
instalikecombot.py -u randomjack01 -p somePASSWw0@d -t somerandomaccount032 -comments mycomments.txt -delay 5
```
```
instalikecombot.py -u randomjack01 -p somePASSWw0@d -t somerandomaccount032 -ps "Check out my page @someaccount11"
```
    
## LICENSE
[MIT](https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/LICENSE)
