from flask import jsonify, request, session
import pymongo
from models.post import Post
from main import app
from apis import login_required


@app.route('/api/posts', methods=['POST'])
@login_required()
def create_post():
    body = request.json

    error_message = Post.validate(body)
    if error_message:
        return jsonify({'error': { 'message': error_message }}), 400

    if session['user']['_id'] != body['posted_by']:
        return jsonify({'error': { 'message': '投稿者が不正です' }}), 400

    last = Post._collection.find_one({'posted_by': body['posted_by']}, sort=[('created_at', pymongo.DESCENDING)])

    if last and last['content'] == body['content']:
        return jsonify({'error': {'message': 'すでに同じ内容のツイートが投稿されています'}}), 400

    post = Post(content=body['content'],
                posted_by=body['posted_by'])

    post.create()

    body['_id'] = str(post._id)
    return jsonify(body)
