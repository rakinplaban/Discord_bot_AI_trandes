from flask import Flask
import main
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(debug=True,port=8000)