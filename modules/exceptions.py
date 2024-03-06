""" 
    exceptions.py - exceptions module for insta-likecom-bot

    insta-likecom-bot v.3.0.5
    Automates likes and comments on an instagram account or tag

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    Copyright (c) 2023 Shine Jayakumar
    LICENSE: MIT
"""

class DuplicateArgumentError(Exception):
    """
    Raise when duplicate arguments are found
    """
    pass

class InvalidProfileFileError(Exception):
    """
    Raise when an invalid profile file is received
    """
    pass

class MandatoryParamsMissingError(Exception):
    """
    Raise when mandatory parameters are missing
    """
    pass

class LoginFailedError(Exception):
    """
    Raise in case of an unsuccessful login
    """
    pass

class ConflictingParamsError(Exception):
    """
    Raise when conflicting parameters are found
    """
    pass

class InvalidAccountError(Exception):
    """
    Raise when an invalid account is found
    """
    pass

class InvalidBrowserError(Exception):
    """
    Raise when an invalid browser is specified
    """
    pass

class InvalidBrowserProfileError(Exception):
    """
    Raise when an invalid browser profile path is received
    """
    pass

class DriverDirectoryMissingError(Exception):
    """
    Raise when the driver directory is missing
    """
    pass

class InvalidLimitsFileError(Exception):
    """
    Raise when an invalid limits json file is received
    """

class LimitsFileMissingError(Exception):
    """
    Raise when limits file is missing
    """

class LimitsExceededError(Exception):
    """
    Raise when limits have exceeded
    """