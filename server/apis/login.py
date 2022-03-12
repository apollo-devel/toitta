from flask import jsonify, request, session
from server.models.user import User
from server.main import app


@app.route('/api/login', methods=['POST'])
def login():
    body = request.json
    user = User._collection.find_one({'email': body['email']})

    if not user:
        return jsonify({'error': { 'message': 'ユーザーが存在しません。' }}), 400
    
    hashed_password = User.encrypt(body['password'])
    if user['hashed_password'] != hashed_password:
        return jsonify({'error': { 'message': 'パスワードが一致しません。' }}), 400
    
    
    del user['hashed_password']
    
    user['_id'] = str(user['_id'])
    session['user'] = user
    return jsonify(user)
