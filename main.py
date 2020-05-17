import threading
from time import sleep
from datetime import datetime, timedelta
import json

from flask import Flask
from filelock import FileLock

import alert
import url_watch

URL_FILENAME = 'url.txt'
JS_LOADED_STRING='ConsumerPageHeading-title'
HREF_CLASS_NAME='Consumer-reservation' # watch these anchors
STARTING_CHANGE_LIST=set() #empty
ALERT_MOBILE_NUMBER='555.555.5555'.replace('.','')
CHANGE_MESSAGE_PREFIX="**Red-alert**: new pickup!"
REVERSE_CHANGE_MESSAGE_PREFIX="Yellow-alert: pickup over"
WEEKLY_ALERT=True
WEEKLY_ALERT_NUMBER='555.555.5555'.replace('.','')
WEEKLY_MSG="🍕's available today!"
DEBUG_EMPTY_CHANGES=False
LOCK_FILENAME = 'url.lock'

def log(message):
    """print to stdout as basic Google App Engine "structured log"
    https://cloud.google.com/run/docs/logging#run_manual_logging-python
    """
    entry = dict(severity='NOTICE',
                 component=__name__,
                 message=message)
    print(json.dumps(entry))

def watch(flask_context):
    with app.app_context():
        # initialize
        previous_changes = STARTING_CHANGE_LIST
        weekly_msg_sent = datetime.utcnow()-timedelta(days=7) #at least 1 week ago
        log("worker loop started")
        while True:
            with FileLock('/tmp/'+LOCK_FILENAME) as lock, open(URL_FILENAME) as url_file:
                log("lock obtained")
                url = url_file.read().strip()
                try:
                    output = url_watch.get_changes(url, JS_LOADED_STRING, HREF_CLASS_NAME)
                    if output['success']:
                        changes = output['result']
                        log(str(changes))
                        if DEBUG_EMPTY_CHANGES and not changes:
                            log(output['debug'])
                    else:
                        log(str(output))
                        continue
                except Exception as e:
                    log(str(e))
                    continue
                old = previous_changes
                previous_changes = changes #save
                if changes.difference(old):
                    opened=str(changes.difference(old))[:75]
                    message="{} {} {}...".format(CHANGE_MESSAGE_PREFIX,url,opened)
                    alert.send_sms(ALERT_MOBILE_NUMBER, message)
                    # Send weekly red-alert!
                    if (datetime.utcnow() >= weekly_msg_sent+timedelta(days=7)
                            and WEEKLY_ALERT):
                        alert.send_sms(WEEKLY_ALERT_NUMBER, WEEKLY_MSG)
                        weekly_msg_sent = datetime.utcnow() # mark send time
                else:
                    if old.difference(changes):
                        gone = str(old.difference(changes))[:80]
                        message="{} {}...".format(REVERSE_CHANGE_MSG_PREFIX,gone)
                sleep(120) # wait
            # retry
            sleep(30)

app = Flask(__name__)

log("running worker thread")
threading.Thread(target=watch, args=(app,)).start()

@app.route('/')
def status():
    try:
        with open('/tmp/'+LOCK_FILENAME) as lockfile:
            opened = ' '+'/tmp/'+LOCK_FILENAME+' exists!'
    except FileNotFoundError:
        opened = ''
    return 'Lock status: '+opened

if __name__ == '__main__':
    # local test server
    app.run(host='127.0.0.1', port=8080, debug=True)
