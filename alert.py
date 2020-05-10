from twilio.rest import Client

US_TWILIO_NUMBER='555.555.5555'.replace('.','')
TWILIO_ACCOUNT_SID='ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
TWILIO_AUTH_TOKEN='your_auth_token' #TODO: migrate to berglas

def send_sms(us_mobile_number, message):
    auth_token = 
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    sms_message = client.messages.create(
        body=message,
        from_='+1{}'.format(US_TWILIO_NUMBER),
        to='+1{}'.format(us_mobile_number))
