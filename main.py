import threading
from time import sleep
import json

from flask import Flask
from filelock import FileLock

import alert
import url_watch

URL_FILENAME = 'url.txt'
JS_LOADED_STRING='ConsumerPageHeading-title'
HREF_CLASS_NAME='Consumer-reservation' # watch these anchors
LOCK_FILENAME = 'url.lock'
ALERT_MOBILE_NUMBER='555.555.5555'.replace('.','')

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
        previous_changes = set()
        log("worker loop started")
        while True:
            with FileLock('/tmp/'+LOCK_FILENAME) as lock, open(URL_FILENAME) as url_file:
                log("lock obtained")
                url = url_file.read().strip()
                output = url_watch.get_changes(url, JS_LOADED_STRING, HREF_CLASS_NAME)
                if output['success']:
                    changes = output['result']
                    log(str(changes))
                else:
                    log(str(output))
                    continue
                old = previous_changes
                previous_changes = changes #save
                if changes.difference(old):
                    opened=str(changes.difference(old))
                    message="**Red-alert**: new pickup! {} {}".format(url,opened)
                    alert.send_sms(ALERT_MOBILE_NUMBER, message)
                else:
                    if old.difference(changes):
                        gone = str(old.difference(changes))
                        message="Yellow-alert: pickup over {}".format(gone)
                sleep(120) # wait
            # retry
            sleep(30)

app = Flask(__name__)

log("running worker thread")
threading.Thread(target=watch, args=(app,)).start()

@app.route('/')
def hello():
    try:
        with open('/tmp/'+LOCK_FILENAME) as lockfile:
            opened = ' '+'/tmp/'+LOCK_FILENAME+' exists!'
    except FileNotFoundError:
        opened = ''
    return 'Hello World!'+opened

@app.route('/signup', methods=['POST'])
def signup():
    return 'Thanks!'

if __name__ == '__main__':
    # local test server
    app.run(host='127.0.0.1', port=8080, debug=True)
