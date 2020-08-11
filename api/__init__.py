from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
import mysql.connector
import json
import jsonpickle
import os
import time

UPLOAD_FOLDER = '/home/pi/dev/api/update'
ALLOWED_EXTENSIONS = {'txt', 'cap'}

config = {
  'user': 'petrou',
  'password': '',
  'host': '127.0.0.1',
  'database': 'PiCrackNG',
  'raise_on_warnings': True,
  'use_unicode': True,
  'charset' : "utf8"
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Just a check to be sure connection is ok
@app.route('/ping/',methods=['GET'])
def ping():
    return str(1)

#Bouchon pour devices
@app.route('/devices/',methods=['POST'])
def getDevices():
    bssid = request.get_json() 
    #scan network
    #return devices
    return "[{\"manuf\": \"Samsung\", \"mac\": \"09:A7:B7\"},{\"manuf\": \"Iphone\", \"mac\": \"17:H2:0T\"}]"

#Bouchon pour le  handshake
@app.route('/handshake/', methods=['POST'])
def getHangshake():
    data = request.get_json()
    mac = data['mac']
    coord = data['coord']
    print(mac)
    print(coord)
    #dump device
    return "1"

#Get all networks   
@app.route('/networks/',methods=['GET'])
def getNetworks():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("SELECT * from network")
    cursor.execute(query)

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)

#Add new network
@app.route('/network',methods=['POST'])
def addNetwork():
    file = request.files['file']
    if not (file and allowed_file(file.filename)):
        return -1
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    data = (
        request.form.get('bssid'),
        request.form.get('essid'),
        request.form.get('longitude'),
        request.form.get('latitude'),
        file_path
    )

    print(data)

    rq = (
        "INSERT INTO network (bssid, essid, longitude, latitude, handshake) "
        "VALUES (%s,%s,%s,%s,%s)"
    )

    cursor.execute(rq,data)
    cnx.commit()
    cursor.close()

    return str(cursor.lastrowid)



if __name__ == "__main__":
    app.run()
