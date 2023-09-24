import socket
import time
import json

class Socket:
    def __init__(self, host_ip, port_number):
        self.host = host_ip
        self.port = port_number
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def c_connect(self):
        self.s.connect((self.host, self.port))
        return self.s


    # CLIENT CLIENT CLIENT
    def c_send_msg(self, action, value, sleep_t=0.1):
        self.s.sendall(str.encode(action+" "+value))
        data = self.s.recv(4096)
        # Test
        # print('Received', repr(data))
        message = data.decode()
        # message(ast.literal_eval(data.decode()))
        time.sleep(sleep_t)
        return message

    # SERVER SERVER SERVER
    def settimeout_conn(self, value: float):
        self.conn_client.settimeout(value)

    def s_send_msg(self,data):
        self.conn_client.sendall(data)

#    def s_receive_msg_json(self):
#        data = self.conn_client.recv(1024)
#        return data

    def s_receive_msg(self):
        data = self.conn_client.recv(1024)
        return data.decode().split()

    def s_close(self):
        self.conn_client.close()


    # Wait for connection: Retry every 2 seconds
    def s_connect(self):
        self.s.bind((self.host, self.port))
        self.s.settimeout(2.0)
        self.s.listen()
        timeout = False
        while not timeout:
            try:
                (conn, addr) = self.s.accept()
            except socket.timeout:
                print("Not connected. Try again")
                pass
            else:
                self.s.settimeout(None)
                self.conn_client = conn
                self.addr_client = addr
                return conn,addr