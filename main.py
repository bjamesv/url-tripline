import threading
from time import sleep
from datetime import datetime, timedelta
import json

from flask import Flask
from filelock import FileLock

import alert
import config
import url_watch

# consolidate account arguments into a set we can unpack
ALERT_BASE_ARGS_SET=(config.TWILIO_ACCOUNT_SID,
                     config.TWILIO_AUTH_TOKEN,
                     config.US_TWILIO_NUMBER)

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
        previous_changes = config.STARTING_CHANGE_LIST
        weekly_msg_sent = datetime.utcnow()-timedelta(days=7) #at least 1 week ago
        log("worker loop started")
        while True:
            with FileLock('/tmp/'+config.LOCK_FILENAME) as lock, open(config.URL_FILENAME) as url_file:
                log("lock obtained")
                url = url_file.read().strip()
                try:
                    output = url_watch.get_changes(url, config.JS_LOADED_STRING, config.HREF_CLASS_NAME)
                    if output['success']:
                        changes = output['result']
                        log(str(changes))
                        if config.DEBUG_EMPTY_CHANGES and not changes:
                            log(output['debug'])
                    else:
                        log(str(output))
                        continue
                except Exception as e:
                    log(str(e))
                    continue
                old = previous_changes
                previous_changes = changes #save
                if config.ALERT_ON_NEW: # Check if primary alert is for new or removed items
                    changes = changes.difference(old)
                    reverse_changes = old.difference(changes)
                else:
                    changes = old.difference(changes)
                    reverse_changes = changes.difference(old)
                if changes:
                    preview=str(changes)[:75]
                    message="{} {} {}...".format(config.CHANGE_MESSAGE_PREFIX,url,preview)
                    alert.send_sms(*ALERT_BASE_ARGS_SET, config.ALERT_MOBILE_NUMBER, message)
                    # Send weekly red-alert!
                    if (datetime.utcnow() >= weekly_msg_sent+timedelta(days=7)
                            and config.WEEKLY_ALERT):
                        alert.send_sms(*ALERT_BASE_ARGS_SET, config.WEEKLY_ALERT_NUMBER, config.WEEKLY_MSG)
                        weekly_msg_sent = datetime.utcnow() # mark send time
                else:
                    if reverse_changes:
                        preview = str(reverse_changes)[:80]
                        message="{} {}...".format(config.REVERSE_CHANGE_MSG_PREFIX,preview)
                sleep(120) # wait
            # retry
            sleep(30)

app = Flask(__name__)

log("running worker thread")
threading.Thread(target=watch, args=(app,)).start()

@app.route('/')
def status():
    try:
        with open('/tmp/'+config.LOCK_FILENAME) as lockfile:
            opened = ' '+'/tmp/'+config.LOCK_FILENAME+' exists!'
    except FileNotFoundError:
        opened = ''
    return 'Lock status: '+opened

if __name__ == '__main__':
    # local test server
    app.run(host='127.0.0.1', port=8080, debug=True)
