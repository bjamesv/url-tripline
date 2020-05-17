from twilio.rest import Client

def send_sms(twilio_sid, twilio_auth_token, twilio_from_number, us_mobile_number, message):
    """
    Send SMS via Twilio

    Keyword Arguments:
    twilio_sid  -- String, Twilio account SID (34 character "AC*" format)
    twilio_auth_token  -- String, Twilio secret auth token
    twilio_from_number  -- String, representing sending 10-digit US number
    us_mobile_number  -- String, 10-digit US number to receive the SMS
    message  -- String, representing the message to send
    """
    client = Client(twilio_sid, twilio_auth_token)

    sms_message = client.messages.create(
        body=message,
        from_='+1{}'.format(twilio_from_number),
        to='+1{}'.format(us_mobile_number))
