from flask import Flask

app = Flask(__name__)
app.secret_key = "ayrnbq8742r5nokmnq2cc3pwian23u821u9dfcuem"

from . import routes