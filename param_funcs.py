"""
param_funcs: Contains functions to handle command line parameters
"""

param_translation = {
    '-u': 'INSTA_USER',
    '-p': 'INSTA_PASS',
    '-t': 'TARGET',
    '-pn': 'POSTSTOLIKE',
    '-ps': 'PS',
    '-comments': 'COMMENTS_FILE',
    '-nocom': 'NOCOMMENTS',
    '-crazy': 'CRAZYMODE',
    '-delay': 'DELAY'
}


def check_params_present(params_to_check, sysargs):
    '''
    checks if params_to_check are present in sysargs
    '''
    args = [arg.lower() for arg in sysargs]
    params_present = [param for param in params_to_check if param in args]
    return len(params_present) == len(params_to_check)


def load_params(sysargs, default_params):
    '''
    extracts param:value pair from sysargs and loads it into default_params
    '''
    valid_param_list = ['-u', '-p', '-t', '-pn', '-ps', '-nocom', '-comments', '-crazy', '-delay']
    int_type_params = ['DELAY', 'CRAZYMODE', 'POSTSTOLIKE', 'NOCOMMENTS'] 
    args = [arg.lower() if arg.startswith('-') else arg for arg in sysargs]
    for i in range(1, len(args)):
        if args[i] in valid_param_list:
            translated_param_name = param_translation[args[i]]
            if translated_param_name in int_type_params:
                default_params[translated_param_name] = int(args[i+1])
            else:
                default_params[translated_param_name] = args[i+1]


def display_help():
    usage = """
        insta-likecom-bot v.1
        Automates likes and comments on an instagram account or tag

        Author: Shine Jayakumar
        Github: https://github.com/shine-jayakumar

        License: MIT

        Usage:
        instalikecombot.py -u <username> -p <password> -t <target>
        instalikecombot.py -u <username> -p <password> -t <target> -pn <no_of_posts>
        instalikecombot.py -u <username> -p <password> -t <target> -pn <no_of_posts> -comments <comment_file> -crazy <1/0>

        Options:
            -u              Instagram username
            -p              Instagram password
            -t              target instagram account or hashtag (ex: -t someaccount11 or -t #haiku)
            -pn             number of posts to like (ex: -pn 30)
            -ps             adds text to the end of a comment (ex: -ps "check out my page @someaccount11") (optional)
            -comments       file with comments. Only 1 comment per line (optional)
            -nocom          turn of comments (ex: -nocom 1) (optional)
            -crazy          runs with minimum delay between each posts. 1 - on, 0 - off (default) (ex: -crazy 1) (optional)
            -delay          delay between each post in seconds (ex: -delay 3). Has no affect when -crazy is set (optional)

        Examples:
        instalikecombot.py -u notsofamousbob -p bbsp#%@wod#^%1101 -t elonmusk
        instalikecombot.py -u notsofamousbob -p bbsp#%@wod#^%1101 -t elonmusk -crazy 1
        instalikecombot.py -u notsofamousbob -p bbsp#%@wod#^%1101 -t elonmusk -delay 2 -comments somecomments.txt
        instalikecombot.py -u notsofamousbob -p bbsp#%@wod#^%1101 -t elonmusk -ps "Check out my page @someaccount11"
        """
    print(f"\n\n{usage}\n")

