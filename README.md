# pylogix-api

Web api for pylogix library

## Video Demo

[![Demo](https://img.youtube.com/vi/JIagCipFybE/0.jpg)](https://www.youtube.com/watch?v=JIagCipFybE)

## Dependencies

- Flask

```
pip install flask
```

## Usage

In a browser or postman you can do the following get requests.

Routes:

```
/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags

/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags/<tag>

/pylogix/v1.0/plc/192.168.0.10/0/tags/[someTag1, someTag2, someTag3, someTag4]

/pylogix/v1.0/plc/192.168.0.10/0/tags/someArrayTag[x]{y}

/pylogix/v1.0/plc/<ipAddress>/<int:slot>/devices
```

Example on local machine:

Get a tag:

```
localhost:5000/pylogix/v1.0/plc/192.168.0.10/0/tags/someTag

{
  "tag": {
    "status": "Success",
    "tagName": "BaseBOOL",
    "value": true
  }
}
```

Get a list of tags:

```
localhost:5000/pylogix/v1.0/plc/192.168.1.196/2/tags/[BaseBOOL, BaseDINT, BaseINT]

[
  "BaseBOOL = True",
  "BaseDINT = -545437484",
  "BaseINT = 6512"
]
```

Get a range from a 1 dim array:

```
{
  "tag": {
    "status": "Success",
    "tagName": "BaseDINTArray[0]",
    "value": [
      1884903867,
      1524930390,
      -1030834104,
      -1303090544,
      388864688,
      1027141633,
      -39957720,
      58739743,
      1392044477,
      -234739063
    ]
  }
}
```

Example running the request from another machine, replace localhost with the machine ip where the server is running:

```
localhost:5000/pylogix/v1.0/plc/192.168.0.10/0/tags/someTag
```
