import socket
import datetime
import json
import threading


class Log:
    def __init__(self, log_file_name="report.log"):
        self.__log_file_name = log_file_name

    def print_log(self, msg):
        log_file = open(self.__log_file_name, "a+")
        time = str(datetime.datetime.now())
        log_file.write(time + ": " + msg + "\n")
        log_file.close()

    def set_file_name(self, name):
        self.__log_file_name = name

    def get_file_name(self):
        return self.__log_file_name


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


log = Log()
config = Config()
ip = config.load("ip")


class Server:
    def __init__(self):
        self.online_clients = {}

    def run(self):

        ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ser.bind((ip, 0))
        self.binded_port = ser.getsockname()[1]
        address = ip + ":" + str(self.binded_port)
        config.set_port(self.binded_port)
        print("server is run at ", address)
        log.print_log("server is run at " + address)
        ser.listen(5)
        return ser

    def chat_handle(self, name, dst_name, addr):
        client = self.online_clients[name]

        while dst_name not in self.online_clients:
            pass

        while True:
            msg = client.recv(1024).decode()

            if str(msg) == "":
                print(name, "left the chat")
                client.close()
                log.print_log(name + " >> left the chat")
                self.online_clients.pop(name)
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                left_msg = {"sender_name": addr, "time": time, "msg": "had left the group"}
                left_msg = json.dumps(left_msg)

                if dst_name in self.online_clients:
                    dst_client = self.online_clients[dst_name]
                    dst_client.send(left_msg.encode())

                break

            else:
                recv_cntnt = json.loads(msg)
                time = recv_cntnt["time"]
                sender = recv_cntnt["sender_name"]
                message = recv_cntnt["msg"]
                log.print_log("@ " + time + " " + sender + " send: " + message)

                if dst_name in self.online_clients:
                    dst_client = self.online_clients[dst_name]
                    try:
                        dst_client.send(msg.encode())
                    except BrokenPipeError:
                        client.send("user is offline.".encode())

    def main(self):

        serv = self.run()

        while True:

            if self.online_clients == {}:
                print("waiting for clients...")

            conn, cli_addr = serv.accept()
            cli_inf_json = conn.recv(1024).decode()
            cli_inf = json.loads(cli_inf_json)
            cli_name = cli_inf["name"]

            if cli_name in self.online_clients:
                print("the user is also existed")
                conn.close()
            else:
                dst_name = cli_inf["dst_name"]
                client_addr = cli_addr[0] + ":" + str(cli_addr[1])
                print(client_addr + " joined the chat with name: ", cli_name)
                log.print_log(client_addr + " joined the chat with name: " + cli_name)
                self.online_clients[cli_name] = conn
                chat_thread = threading.Thread(target=self.chat_handle, args=(cli_name, dst_name, client_addr),
                                               daemon=True)
                chat_thread.start()

    def close(self, ser):
        ser.close()
        for client in self.online_clients:
            client.close()


if __name__ == "__main__":
    try:
        server = Server()
        server.main()
    except KeyboardInterrupt:
        log.print_log("server closed.")
        print("server closed.")
        exit(1)
