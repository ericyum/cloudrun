from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory database for storing messages
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    message = request.json.get('message')
    if message:
        messages.append(message)
        return jsonify({'status': 'OK'})
    return jsonify({'status': 'Error', 'message': 'Empty message'}), 400

@app.route('/messages')
def get_messages():
    return jsonify(messages)


