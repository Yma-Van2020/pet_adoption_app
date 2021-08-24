from flask import Flask,session

app = Flask(__name__)
app.secret_key = 'PLACEHOLDER KEY DO NOT USE IN PRODUCTION'