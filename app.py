#!flask/bin/python
from flask import Flask, url_for, render_template, make_response
from pylogix import PLC

app = Flask(__name__)

@app.route('/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags', methods=['GET'])
def get_all_tags(ipAddress, slot):
    tags = []
    returnTable = False
    includeLinks = False

    comm = PLC(ipAddress, slot)
    ret = comm.GetTagList()
    comm.Close()

    if ret.Value is None:
        return make_response(ret.Status)

    for tag in ret.Value:
        tags.append(
            {"tagName"    : tag.TagName,
             "dataType"   : tag.DataType
            })

    if returnTable:
        if includeLinks:
            return render_template('TableList.html', values=tags, colnames=['tagName', 'dataType'], title = 'Tag List', url1Title = 'Discover Devices: ', url1Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
        else:
            return render_template('TableList.html', values=tags, colnames=['tagName', 'dataType'], title = 'Tag List')
    else:
        if includeLinks:
            return render_template('TagList.html', tags=tags, url1Title = 'Discover Devices: ', url1Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
        else:
            return render_template('TagList.html', tags=tags)

@app.route('/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags/<tag>', methods=['GET'])
def get_tag(tag, ipAddress, slot):
    comm = PLC(ipAddress, slot)
    regularTags = []
    arrayTags = dict()
    results = []
    readArray = False
    arrayElementCount = 0
    showBoolAsOneZero = False
    returnTable = False
    includeLinks = False

    if tag.startswith('[') and tag.endswith(']'): # array of mixed tags
        tags = (tag[1:-1].replace(' ', '')).split(';')

        for t in tags:
            if not t == '':
                if t.endswith('}') and '{' in t: # 1 or 2 or 3 dimensional array tag
                    try:
                        arrayElementCount = int(t[t.index('{') + 1:t.index('}')])
                        readArray = True
                        t = t[:t.index('{')]
                        arrayTags.update( {t : arrayElementCount} )
                    except:
                        pass
                else:
                    regularTags.append(t)

        if len(regularTags) > 0:
            ret = comm.Read(regularTags)

            if ret[0].Value is None:
                comm.Close()
                return make_response(ret[0].Status)

            for i in range(0, len(ret)):
                if showBoolAsOneZero and (str(ret[i].Value) == 'True' or str(ret[i].Value) == 'False'):
                    results.append(
                        {"tagName"  : str(ret[i].TagName),
                         "value"    : 1 if str(ret[i].Value) == 'True' else 0,
                         "status"   : str(ret[i].Status)
                        })
                else:
                    results.append(
                        {"tagName"  : str(ret[i].TagName),
                         "value"    : str(ret[i].Value),
                         "status"   : str(ret[i].Status)
                        })

        if len(arrayTags) > 0:
            for tag in arrayTags:
                ret = comm.Read(tag, arrayTags[tag])

                if ret.Value is None:
                    comm.Close()
                    return make_response(ret.Status)

                if showBoolAsOneZero and (str(ret.Value[0]) == 'True' or str(ret.Value[0]) == 'False'):
                    newBoolArray = []
                    for val in range(0, len(ret.Value)):
                        newBoolArray.append(1 if str(ret.Value[val]) == 'True' else 0)

                    results.append(
                        {"tagName"  : ret.TagName,
                         "value"    : newBoolArray,
                         "status"   : ret.Status
                        })
                else:
                    results.append(
                        {"tagName"  : ret.TagName,
                         "value"    : ret.Value,
                         "status"   : ret.Status
                        })

        comm.Close()

        if len(regularTags) > 0 or len(arrayTags) > 0:
            if returnTable:
                if includeLinks:
                    return render_template('TableList.html', values=results, colnames=['tagName', 'value', 'status'], title = 'Tags Values', url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True), url2Title = 'Discover Devices: ', url2Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
                else:
                    return render_template('TableList.html', values=results, colnames=['tagName', 'value', 'status'], title = 'Tags Values')
            else:
                if includeLinks:
                    return render_template('TagValues.html', results=results, url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True), url2Title = 'Discover Devices: ', url2Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
                else:
                    return render_template('TagValues.html', results=results)
        else:
            if includeLinks:
                return render_template('TagValues.html', results='', url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True), url2Title = 'Discover Devices: ', url2Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
            else:
                return render_template('TagValues.html', results='')
    else:
        if tag.endswith('}') and '{' in tag: # 1 or 2 or 3 dimensional array
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

            if ret.Value is None:
                comm.Close()
                return make_response(ret.Status)

            if showBoolAsOneZero and (str(ret.Value[0]) == 'True' or str(ret.Value[0]) == 'False'):
                newBoolArray = []
                for val in range(0, len(ret.Value)):
                    newBoolArray.append(1 if str(ret.Value[val]) == 'True' else 0)

                results.append(
                    {"tagName"  : ret.TagName,
                     "value"    : newBoolArray,
                     "status"   : ret.Status
                    })
            else:
                results.append(
                    {"tagName"    : ret.TagName,
                     "value"      : ret.Value,
                     "status"     : ret.Status
                    })
        else:
            ret = comm.Read(tag)

            if ret.Value is None:
                comm.Close()
                return make_response(ret.Status)

            if showBoolAsOneZero and (str(ret.Value) == 'True' or str(ret.Value) == 'False'):
                results.append(
                    {"tagName"  : ret.TagName,
                     "value"    : 1 if str(ret.Value) == 'True' else 0,
                     "status"   : ret.Status
                    })
            else:
                results.append(
                    {"tagName"    : ret.TagName,
                     "value"      : ret.Value,
                     "status"     : ret.Status
                    })

        comm.Close()

        if returnTable:
            if includeLinks:
                return render_template('TableList.html', values=results, colnames=['tagName', 'value', 'status'], title = 'Tags Values', url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True), url2Title = 'Discover Devices: ', url2Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
            else:
                return render_template('TableList.html', values=results, colnames=['tagName', 'value', 'status'], title = 'Tags Values')
        else:
            if includeLinks:
                return render_template('TagValues.html', results=results, url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True), url2Title = 'Discover Devices: ', url2Link = url_for('get_devices', ipAddress=ipAddress, slot=slot, _external=True))
            else:
                return render_template('TagValues.html', results=results)

@app.route('/pylogix/v1.0/plc/<ipAddress>/<int:slot>/devices', methods=['GET'])
def get_devices(ipAddress, slot):
    devices = []
    returnTable = False
    includeLinks = False

    comm = PLC(ipAddress, slot)
    ret = comm.Discover()
    comm.Close()

    if ret.Value == []:
        return make_response('No Devices Discovered')

    for device in ret.Value:
        devices.append(
            {"productName": device.ProductName,
             "revision"   : device.Revision
            })
        
    if returnTable:
        if includeLinks:
            return render_template('TableList.html', values=devices, colnames=['productName', 'revision'], title = 'Device List', url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True))
        else:
            return render_template('TableList.html', values=devices, colnames=['productName', 'revision'], title = 'Device List')
    else:
        if includeLinks:
            return render_template('DeviceList.html', devices=devices, url1Title = 'List Tags: ', url1Link = url_for('get_all_tags', ipAddress=ipAddress, slot=slot, _external=True))
        else:
            return render_template('DeviceList.html', devices=devices)

if __name__ == '__main__':
    app.run(host='0.0.0.0')