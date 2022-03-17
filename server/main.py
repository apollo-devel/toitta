from flask import Flask
import logging

app = Flask(__name__)
app.secret_key = 'DUMMY'
app.config['SESSION_COOKIE_NAME'] = '__session'
app.logger.setLevel(logging.INFO)


from apis import login, users, posts