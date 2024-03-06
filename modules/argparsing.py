""" 
    argparsing.py - module to parse command-line arguments

    insta-likecom-bot v.3.0.5
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

import argparse
from modules.constants import APP_VERSION


# ====================================================
# Argument parsing
# ====================================================
description = "Automates likes and comments on an instagram account or tag"
usage = "ilcbot.py -u --username -p --password -t --target [OPTIONS]"
#[-le --loadenv] [-np NOOFPOSTS] [-ps TEXT] [-c FILE | -nc] [-d DELAY] [-hl --headless]"
examples="""
Examples:
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk -np 20
ilcbot.py -u bob101 -p b@bpassw0rd1 -t '#haiku' -ps "Follow me @bob101" -c mycomments.txt
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk --delay 5 --numofposts 30 --headless
ilcbot.py --loadenv --delay 5 --numofposts 10 --headless --nocomments
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk --delay 5 --inlast 3M
ilcbot.py -u bob101 -p b@bpassw0rd1 -t elonmusk --delay 10,60 -vs -ls 3 -cs 3
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    usage=usage,
    epilog=examples,
    prog='ilcbot')


# optional arguments
parser.add_argument('-u','--username', metavar='', type=str, help='Instagram username')
parser.add_argument('-p','--password', metavar='', type=str, help='Instagram password')
parser.add_argument('-t', '--target',  metavar='', type=str, help='target (account or tag)')

parser.add_argument('-np', '--numofposts', type=int, metavar='numposts', help='number of posts to like')
parser.add_argument('-ps', '--postscript', type=str, metavar='text', help='additional text to add after every comment')
parser.add_argument('-ff', '--findfollowers', action='store_true', help="like/comment on posts from target's followers")
parser.add_argument('-fa', '--followersamount', type=int, metavar='nfollowers', help='number of followers to process (default=all)')
parser.add_argument('-lc', '--likecomments', type=int, nargs='?', metavar='ncomments', help='like top n user comments per post')
parser.add_argument('-il', '--inlast', type=str, metavar='', help='target post within last n years (y), months (M), days (d), hours (h), mins (m), secs (s)')

parser.add_argument('-vs', '--viewstory', action='store_true', help='view stories')
parser.add_argument('-ls', '--likestory', type=int, nargs='?', metavar='nstories', help='like stories (default=all)')
parser.add_argument('-cs', '--commentstory', type=int, nargs='?', metavar='ncomments', help='comments on stories (no comments if option not used)')
parser.add_argument('-os', '--onlystory', action='store_true', help='target only stories and not posts')

parser.add_argument('-nr', '--numofreels', type=int, nargs='?', metavar='nreels', help='number of reels to like')
parser.add_argument('-nrc', '--noreelcomments', action='store_true', help='turn off reel comments')
parser.add_argument('-lrc', '--likereelcomments', type=int, nargs='?', metavar='ncomments', help='like top n user comments per reel')
parser.add_argument('-or', '--onlyreels', action='store_true', help='target only reels and not posts')

parser.add_argument('-mr', '--mostrecent', action='store_true', help='target most recent posts')
parser.add_argument('-rr', '--reloadrepeat', type=int, metavar='ntimes', help='reload the target n times (used with -mr)')

parser.add_argument('-mt', '--matchtags', type=str, metavar='tag_file', help='read tags to match from a file')
parser.add_argument('-it', '--ignoretags', type=str, metavar='tag_file', help='read tags to ignore from a file')
match_group = parser.add_mutually_exclusive_group()
match_group.add_argument('-mn', '--matchtagnum', type=int, metavar='count', help='minimum tag match count for post to be qualified')
match_group.add_argument('-ma', '--matchalltags', action='store_true', help='match all tags in matchtags')

comments_group = parser.add_mutually_exclusive_group()
comments_group.add_argument('-c', '--comments', type=str, metavar='file', help='file containing comments (one comment per line)')
comments_group.add_argument('-oc', '--onecomment', type=str, metavar='text', help='specify only one comment')
comments_group.add_argument('-nc', '--nocomments', action='store_true', help='turn off comments')

parser.add_argument('-sc', '--skipcommented', action='store_true', help='skip posts already commented')

parser.add_argument('-lm', '--limits', type=str, metavar='file', help='json file with limits configuration')

parser.add_argument('-pr', '--profile', type=str, metavar='', help='loads profile from a json file')
parser.add_argument('-bp', '--brprofile', type=str, metavar='', help='loads chrome profile from a path')
parser.add_argument('-et', '--eltimeout',  type=int, metavar='', help='max time to wait for elements to be loaded (default=30)')
parser.add_argument('-d', '--delay', type=str, metavar='min,max', help='time to wait during post switch default=1,10')
parser.add_argument('-br', '--browser',  type=str, metavar='', choices = ('chrome', 'firefox'), help='browser to use [chrome|firefox] (default=chrome)')
parser.add_argument('-hl', '--headless',  action='store_true', help='headless mode')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {APP_VERSION}')

