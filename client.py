import socket
import threading
from datetime import datetime
import json
import os


class Config:

    def __init__(self, config_file=None):
        if config_file is None:
            self.__config_file = "config.json"
            self.__ip = self.load("ip")

        else:
            try:
                self.__config_file = config_file
                self.__ip = self.load("ip")
                self.online_clients = []

            except KeyError:
                print("can not reading configs")
                exit(1)

    def load(self, name):
        try:
            cnf_file = open(self.__config_file, "r")
            cntnt = json.load(cnf_file)
            cnf_file.close()
            return cntnt[name]
        except Exception:
            print("cant load config file")
            exit(1)

    def get__config_file(self):
        return self.__config_file

    def set__config_file(self, name):
        self.__config_file = name

    def set_port(self, port):
        cnf_file = open(self.__config_file, "w")
        inf_dict = {"port": port, "ip": self.__ip}
        json.dump(inf_dict, cnf_file)
        cnf_file.close()


config = Config()



class Client:
    def __init__(self):
        self.__ip = config.load("ip")
        self.__port = config.load("port")

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.name = input("Enter your name: ")
            dst_name = input("chat with:")
            self.sock.connect((self.__ip, self.__port))
            print("connected to", self.__ip, ":", self.__port)
            connect_inf = {"name": self.name, "dst_name": dst_name}
            connect_inf_json = json.dumps(connect_inf)
            self.sock.send(connect_inf_json.encode())

        except ConnectionRefusedError:
            print("can not connect to server")
            exit(1)

    def recv_msg(self):
        try:
            while True:
                msg = self.sock.recv(1024).decode()
                recv_cntnt = json.loads(msg)
                time = recv_cntnt["time"]
                sender = recv_cntnt["sender_name"]
                message = recv_cntnt["msg"]
                print(time, sender, message, sep=">>")

        except json.decoder.JSONDecodeError:
            print("server down")
            os._exit(1)

    def run(self):
        self.connect()
        recv_msg_th = threading.Thread(target=self.recv_msg, daemon=True)
        recv_msg_th.start()

        while True:
            msg = str(input(""))
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            send_cntnt = {"time": time, "msg": msg, "sender_name": self.name}
            send_json = json.dumps(send_cntnt)
            self.sock.send(send_json.encode())


if __name__ == "__main__":
    client = Client()
    client.run()
