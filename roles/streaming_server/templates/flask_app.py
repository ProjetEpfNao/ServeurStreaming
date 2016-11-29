import os
import uuid
import time
import threading
import sys
from flask import Flask, request
import logging

FFSERVER_URL = "http://localhost:8090/feed1.ffm"
LENGTH = 4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/flask_app/uploads'
logging.basicConfig(format='%(asctime)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='middleman.log',
                    level=logging.DEBUG)

file_counter = 10

def stream_file(path):
    #print(path)
    os.system("ffmpeg -i " + path + " " + FFSERVER_URL)

def run_stream():
    while 1:
        paths = os.listdir(app.config['UPLOAD_FOLDER'])
        if len(paths) == 0:
            time.sleep(0.1)
            continue
        #print(paths)
        if len(paths) > 10:
            for path in paths[:-1]:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],path))
            paths[:] = [paths[-1]]
            logging.info('Max delay reached. Batch delete executed.')
        path = os.path.join(app.config['UPLOAD_FOLDER'],paths.pop(0))
        stream_file(path)
        try:
            os.remove(path)
        except:
            logging.error('Failed to delete file: '+path)
            #print(path)
            #print(sys.exc_info())
            pass


@app.route('/upload', methods=['POST'])
def upload():
    global file_counter
    file = request.files['file']
    filename = str(file_counter) + ".avi"
    file_counter += 1
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    logging.info('Received and save file to '+filename+' from '+str(request.remote_addr))
    return "1"

if __name__ == '__main__':
    threading.Thread(target=run_stream).start()
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )
