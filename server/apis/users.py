from flask import jsonify, request
from server.main import app

@app.route('/api/users', methods=['POST'])
def register():
    body = request.json
    app.logger.info(body)
    return jsonify(body)

