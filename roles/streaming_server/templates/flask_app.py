import os
import sys
from flask import Flask, request
import logging

FFSERVER_URL = "http://localhost:8090/feed1.ffm"
LENGTH = 15

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='middleman.log',
                    level=logging.DEBUG)

def stream_file(file_storage):
    os.write(sys.stdout.fileno(), file_storage.read())

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    stream_file(file)
    logging.info('Received and save file to '+filename+' from '+str(request.remote_addr))
    return "1"

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )
