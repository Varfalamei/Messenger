import time
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'text': 'Привет',
        'time': 100,
        'name': 'Nick'
    },
    {
        'text': 'Привет, Nick',
        'time': 200,
        'name': 'Jane'
    }
]


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    now = datetime.now()
    return {
        'status': True,
        'name': 'MessengerAI',
        'time': now.strftime('%Y/%m/%d %H:%M:%S сейчас на сервере'),
    }


@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json.get('name')
    text = request.json.get('text')

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if name == '' or text == '':
        return abort(400)

    message = {
        'text': text,
        'time': time.time(),
        'name': name
    }

    db.append(message)
    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)
    return {'messages': messages[:100]}


app.run()
