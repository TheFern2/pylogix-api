#!flask/bin/python
from flask import Flask, jsonify
from pylogix import PLC

app = Flask(__name__)

@app.route('/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags', methods=['GET'])
def get_all_tags(ipAddress, slot):
    tags = []
    comm = PLC(ipAddress, slot)
    ret = comm.GetTagList()
    comm.Close()

    for tag in ret.Value:
        tags.append(
            {"tagName"    : tag.TagName,
             "dataType"   : tag.DataType
            })
        
    return jsonify({'tags': tags})

@app.route('/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags/<tag>', methods=['GET'])
def get_tag(tag, ipAddress, slot):
    comm = PLC(ipAddress, slot)
    ret = comm.Read(tag)
    comm.Close()

    return jsonify({'tag': {
        'tagName'  : ret.TagName,
        'value'    : ret.Value,
        'status'   : ret.Status
    }})


@app.route('/pylogix/v1.0/plc/<ipAddress>/<int:slot>/devices', methods=['GET'])
def get_devices(ipAddress, slot):
    devices = []
    comm = PLC(ipAddress, slot)
    ret = comm.Discover()
    comm.Close()

    for device in ret.Value:
        devices.append(
            {"productName": device.ProductName,
             "revision"   : device.Revision
            })
        
    return jsonify({'devices': devices})

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.19')