# insta-likecom-bot
![MIT License](https://img.shields.io/github/license/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL)

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
- [License](#LICENSE "License")

## Features
- Likes and Comments on all the posts for an account/tag
- Specify the number of posts to like
- Comes loaded with generic comments
- Load your own comments
- Comments supports emojis (full support with Firefox; only bmp characters with Chrome)
- Add a PS to the comments
- Skip comments and just like a post
- Build in random time delays
- Specify time delays after each post
- Supports Chrome and Firefox

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
| -nc , --nocomments | turn off comments |
| -et , --eltimeout | max time to wait for elements to be loaded (default=30) |
| -d , --delay | time to wait while moving from one post to another |
| -br, --browser | browser to use [chrome or firefox] (default=chrome) |

## Usage
**To like and comment every post**
```
instalikecombot.py username password target
```
    
**To specify number of posts to like**
```
instalikecombot.py username password target -np NOOFPOSTS
```
    
**To specify a delay**
```
instalikecombot.py username password target -d DELAY
```

**To specify a file with comments**
```
instalikecombot.py username password target -c FILE
```

**To add a text to the end of every comment**
```
instalikecombot.py username password target -ps TEXT
```

**To leave no comments**
```
instalikecombot.py username password target -nc
```

**To specify a browser**
```
instalikecombot.py username password target -br firefox
```

## Examples
```
instalikecombot.py bob101 b@bpassw0rd1 elonmusk
```
```
instalikecombot.py bob101 b@bpassw0rd1 elonmusk -np 20
```
```
instalikecombot.py bob101 b@bpassw0rd1 #haiku -ps "Follow me @bob101" -c mycomments.txt
```
```
instalikecombot.py bob101 b@bpassw0rd1 elonmusk --delay 5 --numofposts 30
```
**Note: Enclose tagnames (#haiku) in double-quotes when running the script in PowerShell/Bash.**
```
instalikecombot.py bob101 b@bpassw0rd1 "#haiku" -ps "Follow me @bob101" -c mycomments.txt
```
## LICENSE
[MIT](https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/LICENSE)
