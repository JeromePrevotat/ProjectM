"""Module to Log in to Twilio and Send a Confirmation Code via Sms."""

import random

from twilio.rest import Client

import resources

def log_to_twilio():
    """Log in to my Twilio Account."""
    account_sid = 'AC527a1bd9c3a6184a8f08095087bd396d'
    auth_token = 'b1e4d3351b6902e2342d55e2d08fb9e3'
    client = Client(account_sid, auth_token)
    return client

def send_code(number):
    """Sends the newly generated Code via Sms."""
    res = resources.Resources('en')
    client = log_to_twilio()
    number_to_send = number
    code_to_send = generate_code()
    client.messages.create( \
        body=res.confirmation_sms + code_to_send, \
        from_='+33644601488', \
        to=number_to_send \
        )
    return code_to_send

def generate_code():
    """Generate a 6 digits Confirmation Code."""
    i = 6
    code = ''
    while i != 0:
        code = code + str(random.randint(0, 9))
        i -= 1
    return code
