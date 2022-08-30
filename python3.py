from logging import Filter
import jwt
import requests
import json
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from time import time

# convert chat into date format
a, b, c = 0
day, month, year = 0

def other_function(day, month, year):
	return day, month, year

# Enter your Telegram bot token
updater = Updater("",
				use_context=True)

# Enter your API key and your API secret
API_KEY = ''
API_SEC = ''

# create a function to generate a token
# using the pyjwt library
def generateToken():
	token = jwt.encode(

		# Create a payload of the token containing
		# API Key & expiration time
		{'iss': API_KEY, 'exp': time() + 5000},

		# Secret used to generate token signature
		API_SEC,

		# Specify the hashing alg
		algorithm='HS256'
	)
	return token


# create json data for post requests
meetingdetails = {"topic": "The title of your zoom meeting",
				"type": 2,
				"agenda": "test",
				"start_time": "{}-{}-{}T07:29:29Z".format(year, month, day),
			
				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud"
							}
				}

# send a request with headers including
# a token and meeting details
def createMeeting(update: Update, context: CallbackContext):
	day,month,year = update.message.text.split(' ')
	other_function(day,month,year)
	headers = {'authorization': 'Bearer ' + generateToken(),
			'content-type': 'application/json'}
	r = requests.post(
		f'https://api.zoom.us/v2/users/me/meetings',
		headers=headers, data=json.dumps(meetingdetails))

	print("\n creating zoom meeting ... \n")
	# print(r.text)
	# converting the output into json and extracting the details
	y = json.loads(r.text)
	join_URL = y["join_url"]
	meetingPassword = y["password"]
	update.message.reply_text(f'\n here is your zoom meeting link {join_URL} and your \
		password: "{meetingPassword}"\n')

# run the create meeting function
updater.dispatcher.add_handler(MessageHandler(Filters.text, createMeeting))

# run telegram bot
updater.start_polling()