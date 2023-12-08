import pickle
import socket
import sys

import colorama
from colorama import Fore
from othello import Env, Move

from server import MatchServer, socket_recv, socket_send


class BasePlayer(object):
    def __init__(self):
        colorama.init(strip=False)
        self.verbose = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((MatchServer.TCP_IP, MatchServer.TCP_PORT))
        self.sock.settimeout(5)
        self.bufsize = MatchServer.BUF_SIZE
        self.reset()

    def print(self, msg, *args, **kwargs):
        if self.verbose:
            print(Fore.GREEN + "[CLIENT]: " + Fore.RESET, end="")
            print(msg, *args, **kwargs)
            sys.stdout.flush()

    def reset(self) -> None:
        pass

    def play(self, env: Env) -> Move:
        raise NotImplementedError()

    def run(self, verbose=False):
        self.verbose = verbose
        socket_send(self.sock, bytes("ready", "ascii"))
        while True:
            msg = socket_recv(self.sock, self.bufsize).decode("ascii")
            if msg == "finish":
                self.print("Finish!")
                break

            elif msg == "reset":
                self.print("Reset!")
                self.reset()

            elif msg == "go":
                data = socket_recv(self.sock, self.bufsize)
                env = pickle.loads(data)
                move = self.play(env)
                data = pickle.dumps(move)
                socket_send(self.sock, data)

            else:
                raise Exception(f"Unknown message received: '{msg:s}'")
