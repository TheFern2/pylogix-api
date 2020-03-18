#!flask/bin/python
from flask import Flask, jsonify
from pylogix import PLC
import plcConfig

# pylogix setup
comm = PLC(plcConfig.plc_ip, plcConfig.plc_slot)

app = Flask(__name__)

@app.route('/pylogix/plc/v1.0/<tag>', methods=['GET'])
def get_tag(tag):
    return jsonify(comm.Read(tag).Value)


@app.route('/pylogix/plc/v1.0/devices', methods=['GET'])
def get_devices():
    devices = []
    ret = comm.Discover()
    for device in ret.Value:
        json_device = []
        json_device.append(
            {"productName": device.ProductName,
             "revision": device.Revision
            })
        
        devices.append(json_device)
    
    return jsonify({'devices': devices})

if __name__ == '__main__':
    app.run(debug=True)