from flask import Flask
import logging

app = Flask(__name__)
app.secret_key = 'DUMMY'

app.logger.setLevel(logging.INFO)
