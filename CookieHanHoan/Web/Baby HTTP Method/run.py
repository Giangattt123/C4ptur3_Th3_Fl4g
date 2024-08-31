#!/usr/bin/python3
import flask

app = flask.Flask(__name__)

try:
    FLAG = open('/flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

@app.route('/', methods=['GET'])
def index():
  return flask.send_file('index.html')

@app.route('/src', methods=['GET'])
def source():
  return flask.send_file('run.py')

@app.route('/super-secret-route-nobody-will-guess', methods=['PUT'])
def flag():
  return FLAG

app.run(host='0.0.0.0', port=1337)