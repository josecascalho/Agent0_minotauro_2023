#!/usr/bin/env python3
import time
import middleware.mysocket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000      # The port used by the server


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.s = middleware.mysocket.Socket(host,port)

    def print_message(self, data):
        print("Data:", data)

    def connect(self):
        self.s.c_connect()

    def execute(self, action, value, sleep_t=0.1):
        return self.s.c_send_msg(action,value,sleep_t)

def main():
    client = Client(HOST, PORT)
    res = client.connect()
    if res != -1:
        while True:
            command = input("Insert action value pairs:").split()
            if len(command) != 2:
                action, value = "", ""
            else:
                action, value = command
            print("Action Value pair:", action, ":", value)
            msg = client.execute(action, value)
            # test
            client.print_message(msg)


if __name__ == "__main__":
    main()
