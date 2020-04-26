from flask import Flask, render_template, jsonify, request, make_response
from redditBot import selfPost
import os
app = Flask(__name__)

powered = False


@app.route('/')
@app.route('/login')
def login():
    if (request.authorization and request.authorization.username == os.environ['MC_USER'] and request.authorization.password == os.environ['MC_PASS']):
        return render_template("base.html")
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/api/reddit', methods=['POST'])
def outletOn():
    if (validateRedditRequest(request)):
        selfPost(int(request.form['concentration']))
        return jsonify({'success': 'true'})
    return({'success': 'false'})


def validateRedditRequest(req):
    if (req.form['key'] == os.environ['REQUEST_KEY']):
        return True
    return False


@app.route('/redditButtonOnClick', methods=['GET'])
def redditButtonOnClick():
    if request.authorization and request.authorization.username == os.environ['MC_USER'] and request.authorization.password == os.environ['MC_PASS']:
        val = request.args['value']
        selfPost(int(val))
    return ("Must be logged in to use this resource.")


if __name__ == '__main__':
    app.run()
