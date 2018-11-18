from twilio.rest import Client

def logToTwilio():
	account_sid = 'AC527a1bd9c3a6184a8f08095087bd396d'
	auth_token = 'b1e4d3351b6902e2342d55e2d08fb9e3'
	client = Client(account_sid, auth_token)
	return client

def sendCode(number):
	if number == '+33669019971':
		client = logToTwilio()
		numberToSend = number
		codeToSend = 'YOLO'
		message = client.messages.create( \
			body='Your ProjectM Confirmation Code is : ' + codeToSend, \
			from_='+33644601488', \
			to=numberToSend \
			)
	else:
		print('WRONG NUMBER')
	return codeToSend