# insta-likecom-bot
![License](https://img.shields.io/static/v1?label=license&message=MIT&color=green)
![Open Source](https://img.shields.io/static/v1?label=OpenSource&message=Yes&color=brightgreen)
![Version](https://img.shields.io/static/v1?label=version&message=v.2.1&color=blue)
### Automates likes and comments on an instagram account or tag


<p align="center">
<img src="https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/instalikecombot.png"/>
</p>

insta-likecom-bot is an instagram bot written in python to automatically like and comment on an account or tag.

**Table of Contents**
- [Features](#Features "Features")
- [Requirements](#Requirements "Requirements")
- [Installation](#Installation "Installation")
- [Options](#Options "Options")
- [Usage](#Usage "Usage")
- [Examples](#Examples "Examples")
- [Report a Bug](#Issue "Report an Issue")
- [License](#LICENSE "License")


## Features
- Likes and Comments on all the posts for an account/tag
- Likes and Comments on posts from followers of an account
- Specify the number of posts to like
- Filter post based on tags
- Comes loaded with generic comments
- Load your own comments
- Comments supports emojis (full support with Firefox; only bmp characters with Chrome)
- Add a PS to the comments
- Skip comments and just like a post
- Build in random time delays
- Specify time delays after each post
- Supports Chrome and Firefox
- Headless mode
- Load username, password, and target from .env

## Requirements
- Python 3
- Chrome Browser / Firefox

View the [requirements.txt](https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/requirements.txt)

## Installation
```sh
pip install -r requirements.txt
```
## Options
Required arguments
| Argument | Description |
| ------ | ------ |
| username | Instagram username |
| password | Instagram password |
| target | An instagram account or tag |

Optional Arguments
| Option | Description |
| ------ | ------ |
| -np , --numofposts | number of posts to like |
| -ps , --postscript |  additional text to add after every comment |
| -c , --comments | file containing comments (one comment per line) |
| -oc , --onecomment | specify only one comment |
| -nc , --nocomments | turn off comments |
| -ff, --findfollowers | like/comment on posts from target's followers |
| -fa, --followersamount | number of followers to process (default=all) |
| -mt, --matchtags | read tags to match from a file |
| -mn, --matchtagnum | minimum tag match count for post to be qualified |
| -ma, --matchalltags | match all tags in matchtags |
| -et , --eltimeout | max time to wait for elements to be loaded (default=30) |
| -d , --delay | time to wait while moving from one post to another |
| -br, --browser | browser to use [chrome or firefox] (default=chrome) |

## Usage
**To like and comment every post**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget
```

**To specify number of posts to like**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -np NOOFPOSTS
```

**To like and comment on posts from target's followers**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -np NOOFPOSTS -ff
```

**To specify a delay**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -d DELAY
```

**To specify a file with comments**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -c FILE
```

**To specify only one comment**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -oc TEXT
```

**To add a text to the end of every comment**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -ps TEXT
```

**To leave no comments**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -nc
```

**To specify a browser**
```
instalikecombot.py -u yourusername -p yourpassword -t thetarget -br firefox
```

**To load username, password, and target from .env**
```
instalikecombot.py --loadenv
```

## Examples
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk
```
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 5 -ff
```
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 20
```
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t "#haiku" -ps "Follow me @bob101" -c mycomments.txt
```
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t "#haiku" -oc "Hello there"
```
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t elonmusk --delay 5 --numofposts 30
```
```
instalikecombot.py --loadenv --delay 5 --numofposts 10 --headless --nocomments
```
**Note: Enclose tagnames (#haiku) in double-quotes when running the script in PowerShell/Bash.**
```
instalikecombot.py -u bob101 -p b@bpassw0rd1 -t "#haiku" -ps "Follow me @bob101" -c mycomments.txt
```

## Issue
Report a [bug or an issue](https://github.com/shine-jayakumar/insta-likecom-bot/issues/new)

## LICENSE
[MIT](https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/LICENSE)
