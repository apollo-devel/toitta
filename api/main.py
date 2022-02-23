from flask import Flask, jsonify, session

app = Flask(__name__)
app.secret_key = 'DUMMY'

@app.route("/api/hello")
def hello_world():
    if 'count' not in session:
        session['count'] = 0
    session['count'] += 1
    return jsonify({
        'count': session['count'],
        'message': 'hello'
    })