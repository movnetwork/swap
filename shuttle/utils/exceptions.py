#!/usr/bin/env python
# coding=utf-8


class APIError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return "(%s) %s" % (self.error_detail, self.error_message)
        else:
            return self.error_message


class ClientError(Exception):
    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message


class InvalidURLError(Exception):

    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return "%s" % self.error_message


class NotFoundError(Exception):

    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return "%s" % self.error_message


class AddressError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return "%s, %s" % (self.error_message, self.error_detail)
        return "%s" % self.error_message


class BalanceError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return "%s, %s" % (self.error_message, self.error_detail)
        return "%s" % self.error_message


class NetworkError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return "%s, %s" % (self.error_message, self.error_detail)
        return "%s" % self.error_message
