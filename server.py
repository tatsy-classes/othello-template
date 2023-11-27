import sys
import pickle
import socket
import argparse

import othello
import colorama
from colorama import Fore


class MatchServer(object):
    TCP_IP: str = "127.0.0.1"
    TCP_PORT: int = 8080
    BUF_SIZE: int = 65536

    def __init__(self):
        colorama.init()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        self.print(f"listen port {self.TCP_PORT:d}")

    def print(self, msg, *args, **kwargs):
        print(Fore.BLUE + "[SERVER]: " + Fore.RESET, end="")
        print(msg, *args, **kwargs)
        sys.stdout.flush()

    def run(self):
        client, addr = self.sock.accept()
        self.print("Got a connection from", addr)

        ready_msg = client.recv(self.BUF_SIZE).decode("ascii")
        self.print(ready_msg)
        if ready_msg != "ready":
            client.close()
            raise Exception("Client must send message 'ready' in the beginning!!")

        env = othello.make()
        env.reset()
        while not env.is_done():
            client.send(bytes("go", "ascii"))
            data = pickle.dumps(env)
            client.send(pickle.dumps(env))

            data = client.recv(self.BUF_SIZE)
            move = pickle.loads(data)
            env.step(move)

            print(env)
            print()

        client.send(bytes("finish", "ascii"))
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match between two players specified")
    parser.add_argument("--name1", type=str, default="example.py")
    parser.add_argument("--name2", type=str, default="example.py")
    args = parser.parse_args()

    server = MatchServer()
    server.run()
