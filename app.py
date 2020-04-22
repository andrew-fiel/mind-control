from flask import Flask, render_template, jsonify, request
from redditBot import selfPost
import os
app = Flask(__name__)

powered = False


@app.route('/')
def hello():
    return render_template("base.html")


@app.route('/api/reddit', methods=['POST'])
def outletOn():
    return processRedditRequest(request.form['key'], request.form['concentration'])


def processRedditRequest(key, cl):
    if (key == os.environ['REQUEST_KEY']):
        selfPost(int(cl))
        success = 'true'
    else:
        success = 'false'
    return jsonify({'success': success})


if __name__ == '__main__':
    app.run()
