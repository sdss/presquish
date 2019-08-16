# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import


class PresquishError(Exception):
    """A custom core Presquish exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(PresquishError, self).__init__(message)


class PresquishNotImplemented(PresquishError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(PresquishNotImplemented, self).__init__(message)


class PresquishAPIError(PresquishError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Presquish API'
        else:
            message = 'Http response error from Presquish API. {0}'.format(message)

        super(PresquishAPIError, self).__init__(message)


class PresquishApiAuthError(PresquishAPIError):
    """A custom exception for API authentication errors"""
    pass


class PresquishMissingDependency(PresquishError):
    """A custom exception for missing dependencies."""
    pass


class PresquishWarning(Warning):
    """Base warning for Presquish."""


class PresquishUserWarning(UserWarning, PresquishWarning):
    """The primary warning class."""
    pass


class PresquishSkippedTestWarning(PresquishUserWarning):
    """A warning for when a test is skipped."""
    pass


class PresquishDeprecationWarning(PresquishUserWarning):
    """A warning for deprecated features."""
    pass
