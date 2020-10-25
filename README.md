# pylogix-api
Web api for pylogix library

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

/pylogix/v1.0/plc/<ipAddress>/<int:slot>/devices
```

Example on local machine:
```
localhost:5000/pylogix/v1.0/plc/192.168.0.10/0/tags/someTag
```

Example running the request from another machine, replace localhost with the machine ip:
```
localhost:5000/pylogix/v1.0/plc/192.168.0.10/0/tags/someTag
```
