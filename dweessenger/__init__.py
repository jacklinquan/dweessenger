# -*- coding: utf-8 -*-
"""A simple python package for messaging through free dweet service.

Dweet is a simple machine-to-machine (M2M) service from https://dweet.io/ .
Messages are encrypted with AES CBC mode.
Only bytes and str types are supported.

Author: Quan Lin
License: MIT
Requires: cryptodweet

:Example:
>>> from dweessenger import Dweessenger
>>> ds = Dweessenger('YOUR MAILBOX', 'YOUR KEY')
>>> ds.send_message('YOUR MESSAGE')
{u'content': {u'17a1d2b7585d0964432f725f7c5394d072627054b456717778e6028e27bf41e
8': u'6f8ea813da2029107a53fdf5ae9095fb'}, u'thing': u'0ec063a2afa798ca792993d0b
5780c66', u'transaction': u'5fcb54ee-61cb-4f73-850e-5abe29ce2553', u'created': 
u'2019-02-11T03:44:36.179Z'}
>>> ds.get_new_message()
u'YOUR MESSAGE'
>>> ds.get_new_message()
>>> ds.get_latest_message()
u'YOUR MESSAGE'
"""

# Project version
__version__ = '0.1.1'
__all__ = ['Dweessenger', 'DweessengerError']

from datetime import datetime

from cryptodweet import CryptoDweet, from_bytes

UTC_TIME_STRING_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def get_current_utc_time():
    return datetime.utcnow()
    
def get_string_from_utc_time(utc_time):
    return utc_time.strftime(UTC_TIME_STRING_FORMAT)

def get_utc_time_from_string(utc_time_string):
    return datetime.strptime(utc_time_string, UTC_TIME_STRING_FORMAT)
    
def get_time_difference(utc_time1, utc_time2):
    return abs(utc_time1 - utc_time2).total_seconds()

class DweessengerError(Exception):
    """Dweessenger error class."""

class Dweessenger(object):
    """A class for messaging through free dweet service.
    
    Initialization options:
        # With default key and iv, not secure.
        Dweessenger('YOUR MAILBOX')
        # Only set key, and iv is the same as key.
        Dweessenger('YOUR MAILBOX', 'YOUR KEY')
        # Set both key and iv, strongest encryption. 
        Dweessenger('YOUR MAILBOX', 'YOUR KEY', 'YOUR IV')
        
    The given key is padded with space to 16 bytes (if shorter than 16 bytes)
    or padded with space to 32 bytes (if length is between 16 and 32)
    or truncated to 32 bytes (if longer than 32 bytes).
    The given iv is padded with space or truncated to 16 bytes.
    """
    def __init__(
        self,
        mailbox='mailbox',
        aes_cbc_key='aes_cbc_key',
        aes_cbc_iv=None
    ):
        self._mailbox = mailbox
        self._aes_cbc_key = aes_cbc_key
        if aes_cbc_iv is None:
            self._aes_cbc_iv = self._aes_cbc_key
        else:
            self._aes_cbc_iv = aes_cbc_iv
        self._latest_send_message_time = None
        self._latest_send_message = None
        self._latest_get_message_time = None
        self._latest_get_message = None
        
    @property
    def latest_send_message_time(self):
        """The latest send message time."""
        return self._latest_send_message_time
    
    @property
    def latest_send_message(self):
        """The latest send message."""
        return self._latest_send_message
    
    @property
    def latest_get_message_time(self):
        """The latest get message time."""
        return self._latest_get_message_time
    
    @property
    def latest_get_message(self):
        """The latest get message."""
        return self._latest_get_message
    
    def send_message(self, message):
        """Send a message.
        
        :param message: the message to be sent.
        :type message: bytes, str.
        :returns: the response from dweet service.
        :rtype: dict
        """
        utc_datetime = get_current_utc_time()
        time_string = get_string_from_utc_time(utc_datetime)
        
        try:
            response = CryptoDweet(
                self._aes_cbc_key,
                self._aes_cbc_iv
            ).dweet_for(self._mailbox, {time_string: message})
        except Exception as ex:
            raise DweessengerError(str(ex))
        
        self._latest_send_message_time = utc_datetime
        self._latest_send_message = from_bytes(message)
        return response
        
    def get_latest_message(self):
        """Get the latest message.
        
        :returns: the latest message in the mailbox.
        :rtype: str
        """
        try:
            latest_dweet = CryptoDweet(
                self._aes_cbc_key,
                self._aes_cbc_iv
            ).get_latest_dweet_for(self._mailbox)
            content_dict = latest_dweet[0]['content']
            created_time_string = latest_dweet[0]['created'][:23] + u'000Z'
            sent_time_string = list(content_dict.keys())[0]
            message = list(content_dict.values())[0]
            created_time = get_utc_time_from_string(created_time_string)
            sent_time = get_utc_time_from_string(sent_time_string)
        except Exception as ex:
            raise DweessengerError(str(ex))
        
        # If there is too much gap between sent time and created time,
        # it is very likely under duplication attack.
        sent_created_time_gap = get_time_difference(created_time, sent_time)
        if sent_created_time_gap > 10:
            raise DweessengerError(
                'Too much gap between sent time and created time. ' \
                + 'Very likely under duplication attack.'
            )
        
        self._latest_get_message_time = sent_time
        self._latest_get_message = message
        return self._latest_get_message

    def get_new_message(self):
        """Get the new message.
        
        :returns: the new message in the mailbox or None if no new message.
        :rtype: str or None
        """
        last_message_time = self._latest_get_message_time
        this_message = self.get_latest_message()
        this_message_time = self._latest_get_message_time
        if (
            last_message_time is None \
            or this_message_time > last_message_time
        ):
            return this_message
        return None
        
        