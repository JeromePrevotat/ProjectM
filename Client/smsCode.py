from twilio.rest import Client

import resources
import random

def logToTwilio():
	account_sid = 'AC527a1bd9c3a6184a8f08095087bd396d'
	auth_token = 'b1e4d3351b6902e2342d55e2d08fb9e3'
	client = Client(account_sid, auth_token)
	return client

def sendCode(number):
	res = resources.Resources('en')
	client = logToTwilio()
	numberToSend = number
	codeToSend = generateCode()
	message = client.messages.create( \
		body = res.confirmationSms + codeToSend, \
		from_ = '+33644601488', \
		to = numberToSend \
		)
	return codeToSend

def generateCode():
	"""Generate a 6 digits Confirmation Code."""
	i = 6
	code = ''
	while i != 0:
		code = code + str(random.randint(0,9))
		i -= 1
	return code