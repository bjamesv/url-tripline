import threading
from time import sleep
import json

from flask import Flask
from filelock import FileLock

import alert

URL_FILENAME = 'url.txt'
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

def watch():
    log("worker loop started")
    while True:
        with FileLock('/tmp/'+LOCK_FILENAME) as lock, open(URL_FILENAME) as url_file:
            log("lock obtained")
            url = url_file.read().strip()
            message="Test-Test! Order @ {}".format(url)
            alert.send_sms(ALERT_MOBILE_NUMBER, message)
            sleep(60)# TODO, remove debug
        # retry
        sleep(30)

log("running worker thread")
threading.Thread(target=watch).start()

app = Flask(__name__)

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
