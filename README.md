# simple-tcp-chat
This is a simple chat program via TCP/IP written in python3.
In this program multiple clients connect to the server. Clients can chat with each other through one or multiple systems in network.

## manual
1) Run `server.py`.

2) Run `client.py`.

**Note**: If at least one of your clients are on diffrent systems you should change **ip** and **port** manualy from `config.json` file in each client system.
You should change them to your server **ip** in your network and the **port** that printed on server program after run.
Then you can run `client.py` and start chat.


**Note**: You can access each system **ip** with [this manual](https://www.dnsstuff.com/scan-network-for-device-ip-address)

## install reqired packages
In this program I use socket,threading and json packages if you dont have them you can install them using pip:

### windows
```bash
pip install socket
```
### linux
```bash
pip3 install socket
```

## contribution

**Feel free to fork. Also I appreciate you if report me any bug.**
