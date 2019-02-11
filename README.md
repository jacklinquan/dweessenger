# dweessenger
[![PyPI version](https://badge.fury.io/py/dweessenger.svg)](https://badge.fury.io/py/dweessenger) 

A simple python package for messaging through free dweet service.

Dweet is a simple machine-to-machine (M2M) service from https://dweet.io/ .
Messages are encrypted with AES CBC mode.
Only bytes and str types are supported.

Please consider [![Paypal Donate](https://github.com/jacklinquan/images/blob/master/paypal_donate_button_200x80.png)](https://www.paypal.me/jacklinquan) to support me.

## Installation
`pip install dweessenger`

## Usage
```
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
```
