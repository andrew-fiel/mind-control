from flask import Flask, render_template, jsonify
app = Flask(__name__)

powered = False


@app.route('/')
def hello():
    return render_template("base.html")


@app.route('/api/signalOn', methods=['POST'])
def outletOn():
    return jsonify({'newState': "on",
                    'success': True})


@app.route('/api/signalOff', methods=['POST'])
def outletOff():
    return jsonify({'newState': "off",
                    'success': True})


if __name__ == '__main__':
    app.run()
