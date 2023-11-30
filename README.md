# insta-likecom-bot
![License](https://img.shields.io/static/v1?label=license&message=MIT&color=green)
![Open Source](https://img.shields.io/static/v1?label=OpenSource&message=Yes&color=brightgreen)
![Version](https://img.shields.io/static/v1?label=version&message=v.3.0.4&color=blue)
![Issues](https://img.shields.io/github/issues/shine-jayakumar/insta-likecom-bot)
![ClosedIssues](https://img.shields.io/github/issues-closed-raw/shine-jayakumar/insta-likecom-bot)
![Contributors](https://img.shields.io/github/contributors/shine-jayakumar/insta-likecom-bot)
![LastCommit](https://img.shields.io/github/last-commit/shine-jayakumar/insta-likecom-bot)
![TotalCommits](https://badgen.net/github/commits/shine-jayakumar/insta-likecom-bot)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/shine-jayakumar/insta-likecom-bot/issues)


### Automates likes and comments on an instagram account or tag


<p align="center">
<img src="https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/instalikecombot.png"/>
</p>

insta-likecom-bot is an instagram bot written in python to automatically like and comment on an account or tag.

**Table of Contents**
- [Features](#features "Features")
- [Requirements](#requirements "Requirements")
- [Installation](#installation "Installation")
- [Options](#options "Options")
- [Usage](#usage "Usage")
- [Examples](#examples "Examples")
- [Version Updates](#version-updates "Version Updates")
- [Frequenty Asked Questions](#fAQs "FAQs")
- [Report a Bug](#issue "Report an Issue")
- [License](#license "License")
- [Donations](#donations "Donations")


## Features
- Interact with Posts (like, comment, like user comments)
- Interact with Stories (like, comment)
- Interact with Reels (like, comment, like user comments) [NEW] [version >= 3.0.4]
- Like and Comment on posts from followers of an account
- Softban limit check [NEW] [version >= 3.0.4]
- Skip posts/reels already commented [NEW] [version >= 3.0.4]
- Target only stories or reels (skip posts)
- ~~Target Most Recent posts~~ (Deprecated)
- ~~Reloading target to view latest posts~~ (Deprecated)
- Specify the number of posts to like
- Filter post based on tags
- Filter posts within last n years, months, days, hours, mins, secs
- Comes loaded with generic comments
- Load your own comments
- Comments supports emojis (full support with Firefox; only bmp characters with Chrome)
- Add a PS to the comments (postscript)
- Supports Chrome and Firefox
- Headless mode
- Supports profile - load parameters from a json file
- Supports browser profile - save credentials to skip login

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
| target | An instagram account or tag|
| limits | json file defining daily/hourly limits |

Optional Arguments
| Option | Description |
| ------ | ------ |
| -np , --numofposts | number of posts to like |
| -ps , --postscript |  additional text to add after every comment |
| -c , --comments | file containing comments (one comment per line) |
| -oc , --onecomment | specify only one comment |
| -nc , --nocomments | turn off comments |
| -lc, --likecomments | like top n user comments per post |
| -ff, --findfollowers | like/comment on posts from target's followers |
| -fa, --followersamount | number of followers to process (default=all) |
| -il, --inlast | target post within last n days (default=all) ex. 1y, 2M, 3d, 4h, 53m, 10s |
| -ls, --likestory | like stories (use 111 to like all stories)|
| -cs, --commentstory | comment on stories (use 111 to comment on all stories) |
| -os, --onlystory | target only stories and not posts |
| -nr, --numofreels | number of reels to like |
| -nrc, --noreelcomments | turn off reel comments |
| -lrc, --likereelcomments | like top n user comments per reel |
| -or, --onlyreels | target only reels and not posts |
| -mr, --mostrecent | target most recent posts |
| -rr, --reloadrepeat | reload the target n times (used with -mr) |
| -mt, --matchtags | read tags to match from a file |
| -mn, --matchtagnum | minimum tag match count for post to be qualified |
| -ma, --matchalltags | match all tags in matchtags |
| -lm, --limits | json file with limits configuration |
| -et , --eltimeout | max time to wait for elements to be loaded (default=30) |
| -d , --delay | time to wait while moving from one post to another |
| -br, --browser | browser to use [chrome or firefox] (default=chrome) |
| -pr, --profile | loads profile from a json file |
| -bp, --brprofile | loads chrome profile from a path | 

## Usage
**To like and comment every post**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget --limits limits.json
```

**To like and comment on stories**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -ls -cs 20 -lm limits.json
```

**To like and comment on reels**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -nr 10 -lm limits.json
```

**To specify number of posts to like**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -np NOOFPOSTS -lm limits.json
```

**To like and comment on posts from target's followers**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -np NOOFPOSTS -ff -lm limits.json
```

**To specify a delay**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -d DELAY -lm limits.json
```
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -d start,end -lm limits.json
```

**To specify a file with comments**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -c FILE -lm limits.json
```

**To specify only one comment**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -oc TEXT -lm limits.json
```

**To add a text to the end of every comment**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -ps TEXT -lm limits.json
```

**To leave no comments**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -nc -lm limits.json
```

**To like comments from other users**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -ls 5 -lm limits.json
```

**To filter posts within last 2 days**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -il 2d -lm limits.json
```

**To filter posts within last 5 months**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -il 5M -lm limits.json
```

**To filter posts within last 3 years**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -il 3y -lm limits.json
```

**To target most recent posts**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -mr -lm limits.json
```

**To reload target 5 times with most recent posts**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -mr -rr 5 -lm limits.json
```

**To filter posts based on tags**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget --matchtags tags.txt -lm limits.json
```

**To specify a browser**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -br firefox -lm limits.json
```

**To specify a profile**
```
ilcbot.py -pr profile1.json -lm limits.json
```

**To specify a browser profile**
```
ilcbot.py -u yourusername -p yourpassword -t thetarget -bp '/path/to/Profile 1' -lm limits.json
```

## Examples
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 5 -ff -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 20 -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t "#haiku" -ps "Follow me @bob101" -c mycomments.txt -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t "#haiku" -oc "Hello there" -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk --delay 5 --numofposts 30 -lm limits.json
```
```
ilcbot.py -u 'bob101' -p 'b@bpassw0rd1' -t "#haiku" --delay 2,20 -lm limits.json
```
```
ilcbot.py --loadenv --delay 5 --numofposts 10 --headless --nocomments -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -d 5 -np 30 -lc 5 -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 30 -il 3h -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 30 --matchtags tags.txt --ignoretags ignoretags.txt -lm limits.json
```
```
ilcbot.py -pr profile1.json -lm limits.json
```
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 30 --brprofile '/path/to/Profile 1' -lm limits.json
```

**Note: Enclose tagnames (#haiku) in double-quotes/single-quotes when running the script in PowerShell/Bash.**
```
ilcbot.py -u bob101 -p b@bpassw0rd1 -t "#haiku" -ps "Follow me @bob101" -c mycomments.txt
```
```
ilcbot.py -u 'bob101' -p 'b@bpassw0rd1' -t "#haiku" -ps "Follow me @bob101" -c mycomments.txt
```
**Sample profiles**
```
{   
    "username": "bob01",
    "password":"passw0rd",
    "target": "targets.txt",
    "numofposts": "3",
    "matchtags": "tags.txt",
    "ignoretags": "ignore.txt",
    "comments": "comments.txt",
    "viewstory": true,
    "likestory": 1,
    "inlast": "3d",
    "delay": "5",
    "likecomments": 2,
    "nocomments": true
}
```
```
{   
    "username": "bob01",
    "password":"passw0rd",
    "target": ["#haikus", "#photography"],
    "numofposts": "3",
    "matchtags": ["#haiku", "#haikus", "#haikupoetry"],
    "ignoretags": ["#shorts"],
    "comments": "comments.txt",
    "viewstory": true,
    "likestory": 1,
    "inlast": "3d",
    "delay": "5",
    "likecomments": 2,
    "nocomments": true,
    "brprofile" : "/dir/dir1/Profile 1"
}
```
```
{   
    "username": "bob01",
    "password":"passw0rd",
    "target": "#photography",
    "numofposts": 2,
    "comments": ["Beautiful!", "Amazing!", "I can relate to this"],
    "delay": "5,20"
}
```
**Sample target files**
<br/>
targets.txt
```
#haiku
#photography
bob01
elonmusk
```
**Sample file with tags**
<br/>
tagstomatch.txt
```
#gym
#fitness
#stayfit
#healthylife
#workout
```
**Sample file with comments**
<br/>
comments.txt
```
🔥🔥🔥
👏👏
Beyond amazing 😍
You’re the goat
This is fire 🔥
Keep grinding 💪
Insane bro 🔥
The shocker! 😮
Such a beauty 😍❤️
```
**Sample limits configuration file**
<br/>
instalimits.json
```
{
    "daily": {
        "likes": 1000,
        "stories": 1000,
        "story_likes": 600,
        "comment_likes": 1500,
        "accounts": 800,
        "comments": 1000
    },
    "hourly": {
        "likes": 350,
        "accounts": 120,
        "comments": 200
    }
}
```



## Version Updates
Version **v.3.0.4** (latest)

Feature addition:
- Reels interaction added
- Softban limit check added
- Skip already commented posts/reels
- Persistent stats

Changes:
- Introduced InstaWorkFlow class
- Added unit testing
- Updated Stats class - Auto exit on exceeding limits

Bug Fixes:
- auto creation of logs directory
- xpaths for like, Save info buttons updated

<br/>

Version **v.3.0.3**

Bug Fixes:
- Webdriver manager upgraded, enabling script to find latest Chrome drivers
- XPATH for 'like' button updated

Changes:
- Using selenium Service class

<br/>

Version **v.3.0.2**

Feature addition:
- Supports Chrome browser profile - saves credentials
- Supports profiles - loads arguments from a json file
- Supports multiple targets - accepts file, list, or single value
- Delay parameter can accept a range (2-20) or single value (20)
- Ignoretags parameter - skip posts with specific tags present
- Matchtags, Ignoretags parameter accepts tags from a file, list, or as a single value

Changes:
- Script renamed to 'ilcbot.py'
- loadenv parameter deprecated

<br/>

Version **v.2.8** 

Feature addition:
- added option -os, --onlystory - target only stories

Bug Fixes:
- Private account check before opening stories
- Check if story is present

<br/>

Version **v.2.7**

Feature addition:
- added option -ls, --likestory - to like stories
- added option -cs, --commentstory - to comment on stories
- added option -rr, --reloadrepeat - to reload target n times

<br/>

## FAQs

- [How to find Chrome profile path?](https://chromium.googlesource.com/chromium/src/+/master/docs/user_data_dir.md#:~:text=user%20data%20directory.-,Current%20Location,path%20to%20the%20profile%20directory.)


<br/>

## Issue
Report a [bug or an issue](https://github.com/shine-jayakumar/insta-likecom-bot/issues/new)

## LICENSE
[MIT](https://github.com/shine-jayakumar/insta-likecom-bot/blob/master/LICENSE)

## Donations
<a href="https://www.buymeacoffee.com/shinej" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 200px !important;" ></a>
