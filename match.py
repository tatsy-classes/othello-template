import socket
import argparse

from othello import Move, Player, make


class MatchServer(object):
    TCP_IP: str = "127.0.0.1"
    TCP_PORT: int = 8080
    BUF_SIZE: int = 1024

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        self.print("Listen:", self.TCP_PORT)

    def run(self):
        client, addr = self.sock.accept()
        self.print("Got a connection from", addr)

        ready_msg = client.recv(self.BUF_SIZE).decode("ascii")
        self.print(ready_msg)
        if ready_msg != "ready":
            client.close()
            raise Exception("Client must send message 'ready' in the beginning!!")

        client.send(bytes("go", "ascii"))
        while True:
            data = client.recv(self.BUF_SIZE)
            if not data:
                break

            text = data.decode("ascii")
            if text == "ready":
                msg = "Great!!!"
                client.send(msg.encode("ascii"))

        client.close()

    def print(self, msg, *args, **kwargs):
        print("server: " + msg, *args, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match between two players specified")
    parser.add_argument("--name1", type=str, default="example.py")
    parser.add_argument("--name2", type=str, default="example.py")
    args = parser.parse_args()

    server = MatchServer()
    server.run()
