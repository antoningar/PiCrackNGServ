from flask import Flask
from flask import request
from werkzeug.utils import secure_filename

import Script
import JSONHelper

UPLOAD_FOLDER = '/home/pi/dev/api/update'
ALLOWED_EXTENSIONS = {'txt', 'cap'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ping/',methods=['GET'])
def ping():
    return str(1)


@app.route('/networks/',methods=['GET'])
def getNetworks():
    networks = Script.getNetworks()
    return networks

@app.route('/devices/',methods=['POST'])
def getDevices():
    network = request.get_json()
    devices = Script.getDevices(network)
    return devices

@app.route('/handshake/', methods=['POST'])
def getHandshake():
    data = request.get_json()
    network = data['network']
    mac = data['mac']
    Script.getAndSendHandshake(network, mac)
    return "1"

if __name__ == "__main__":
    app.run()
