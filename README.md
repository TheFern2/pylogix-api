# pylogix-api

Web api for pylogix library

## Video Demo

[![Demo](https://img.youtube.com/vi/JIagCipFybE/0.jpg)](https://www.youtube.com/watch?v=JIagCipFybE)

## Dependencies

- Flask

```
pip install flask
```

## How to Run

Linux or Mac (I don't know many Industrial Engineers with Macs, but hey you never know :) ):

```
python app.py
or
python3 app.py
```

Windows:

```
If there is only one python installed:
python app.py
Else
py -3.7 app.py
```

## Insomnia Setup

I've exported a json file for insomnia for quick and easy testing, just import as a workspace.

Preferences > Data > Import Data

Then setup a pylogix-api-env, those two variables are used within the routes in insomnia:

```
{
  "plc_ip": "192.168.56.106",
  "plc_slot": "2"
}
```

## Usage

In a browser or insomnia you can do the following get requests.

Routes:

```
/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags

/pylogix/v1.0/plc/<ipAddress>/<int:slot>/tags/<tag>

/pylogix/v1.0/plc/192.168.0.10/0/tags/[someTag1; someTag2; someTag3; someTag4]

/pylogix/v1.0/plc/192.168.0.10/0/tags/someArrayTag[x]{a}

/pylogix/v1.0/plc/192.168.0.10/0/tags/someArrayTag[x, y]{a}

/pylogix/v1.0/plc/192.168.0.10/0/tags/someArrayTag[x,y,z]{a}

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

{
  "tags": [
    {
      "status": "Success",
      "tagName": "BaseBOOL",
      "value": "True"
    },
    {
      "status": "Success",
      "tagName": "BaseDINT",
      "value": "-545437484"
    },
    {
      "status": "Success",
      "tagName": "BaseINT",
      "value": "6512"
    }
  ]
}
```

Get a range from a 1 dim array:

```
localhost:5000/pylogix/v1.0/plc/192.168.1.196/2/tags/BaseDINTArray[0]{10}

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

## Contributors

Many thanks to:

- [GitHubDragonFly](https://github.com/GitHubDragonFly)
