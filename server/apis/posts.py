from flask import jsonify, request, session
from bson.objectid import ObjectId
import pymongo
from models.like import Like
from models.post import Post
from models.user import User
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


@app.route('/api/posts', methods=['GET'])
@login_required()
def list_posts():
    results = []
    for post in Post._collection.find(sort=[('created_at', pymongo.DESCENDING)]):
        results.append(_populate(post))
    return jsonify(results)


@app.route('/api/posts/<post_id>/like', methods=['POST'])
@login_required()
def like_post(post_id):
    post = Post._collection.find_one({'_id': ObjectId(post_id)})
    if not post:
        return jsonify({'error': { 'message': '投稿が存在しません' }}), 404
    user_id = session['user']['_id']
    like = Like._collection.find_one({'post': ObjectId(post_id), 'liked_by': ObjectId(user_id)})
    if like:
        return jsonify(_populate(post))
    else:
        like = Like(post=post_id,
                    posted_at=post['created_at'],
                    liked_by=user_id)
        try:
            like.create()
        except pymongo.errors.DuplicateKeyError:
            pass
        like_count = Like._collection.count_documents({'post': ObjectId(post_id)})
        post = Post._collection.find_one_and_update(
            {'_id': ObjectId(post_id)}, 
            {'$set': {'like_count': like_count}},
            return_document=pymongo.ReturnDocument.AFTER)
        return jsonify(_populate(post))


def _populate(post):
    post['_id'] = str(post['_id'])
    posted_by = User._collection.find_one({'_id': post['posted_by']})
    if posted_by:
        posted_by['_id'] = str(posted_by['_id'])
        post['posted_by'] = posted_by
    return post