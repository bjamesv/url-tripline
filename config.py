# Simple Python module defining configurable url-tripline settings

TWILIO_ACCOUNT_SID='ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
TWILIO_AUTH_TOKEN='your_auth_token' #TODO: migrate to berglas
US_TWILIO_NUMBER='555.555.5555'.replace('.','')

URL_FILENAME = 'url.txt'
JS_LOADED_STRING='ConsumerPageHeading-title'
HREF_CLASS_NAME='Consumer-reservation' # watch these anchors
STARTING_CHANGE_LIST=set() #empty
ALERT_ON_NEW=True # setting False will switch behavior of CHANGE_MESSAGE / REVERSE_CHANGE_MESSAGE 

ALERT_MOBILE_NUMBER='555.555.5555'.replace('.','')
CHANGE_MESSAGE_PREFIX="**Red-alert**: new pickup!"
REVERSE_CHANGE_MESSAGE_PREFIX="Yellow-alert: pickup over"

WEEKLY_ALERT=True
WEEKLY_ALERT_NUMBER='555.555.5555'.replace('.','')
WEEKLY_MSG="🍕's available today!"

DEBUG_EMPTY_CHANGES=False
LOCK_FILENAME = 'url.lock'
