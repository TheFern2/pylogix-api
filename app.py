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
    myTags = []
    result = []
    readArray = False
    arrayElementCount = 0

    if tag.startswith('[') and tag.endswith(']'): # array of tags
        tags = (tag[1:-1].replace(' ', '')).split(',')
        for t in tags:
            if not t == '':
                myTags.append(t)

        if len(myTags) > 0:
            ret = comm.Read(myTags)

            comm.Close()

            for i in range(0, len(ret)):
                result.append(str(ret[i].TagName) + ' = ' + str(ret[i].Value))
            
            # TODO
            # Need a full json response here, not just an array of values. 
            # {
            #     "tags": {
            #         "tag": {
            #             "status": "Success",
            #             "tagName": "BaseBOOL",
            #             "value": true
            #         },
            #         "tag": {
            #             "status": "Success",
            #             "tagName": "BaseDINT",
            #             "value": 456464
            #         }
            #     }
            # }

            return jsonify(*result)
        else:
            return jsonify('Not a valid tag!')
    else:
        if tag.endswith('}') and '{' in tag: # 1-dimensional array
            try:
                arrayElementCount = int(tag[tag.index('{') + 1:tag.index('}')])
                readArray = True
                tag = tag[:tag.index('{')]
            except:
                pass
        else:
            pass

        if readArray and arrayElementCount > 0:
            ret = comm.Read(tag, arrayElementCount)
        else:
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
    app.run(host='0.0.0.0')