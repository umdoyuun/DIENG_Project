from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

subprocesses = {}

@app.route('/start', methods=['POST'])
def start():
    global subprocesses
    token = request.form.get('token')
    if token in subprocesses:
        return "Recording already in progress"
    else:
        subprocesses[token] = subprocess.Popen(['python', 'record.py', token])
        return "Recording started"

@app.route('/stop', methods=['POST'])
def stop():
    global subprocesses
    token = request.form.get('token')
    if token in subprocesses:
        subprocesses[token].send_signal(subprocess.signal.SIGINT)
        del subprocesses[token]
        return "Recording stopped"
    else:
        return "No recording in progress"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=9999)

