import sys
import time
import pickle
import socket
from io import BytesIO

import colorama
from server import MatchServer
from othello import Env, Move
from colorama import Fore


class BasePlayer(object):
    def __init__(self):
        colorama.init()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.sock.connect((MatchServer.TCP_IP, MatchServer.TCP_PORT))
        self.bufsize = MatchServer.BUF_SIZE
        self.reset()

    def print(self, msg, *args, **kwargs):
        print(Fore.GREEN + "[CLIENT]: " + Fore.RESET, end="")
        print(msg, *args, **kwargs)
        sys.stdout.flush()

    def reset(self) -> None:
        pass

    def play(self, env: Env) -> Move:
        raise NotImplementedError()

    def run(self):
        self.sock.send(bytes("ready", "ascii"))
        while True:
            msg_data = self.sock.recv(self.bufsize)
            if not msg_data:
                break

            msg = msg_data.decode("ascii")
            if msg == "finish":
                break

            elif msg == "reset":
                self.reset()

            elif msg == "go":
                data = self.sock.recv(4)
                if not data:
                    break

                data_size = int.from_bytes(data, "little")
                data = b""
                while len(data) < data_size:
                    req_size = min(self.bufsize, data_size - len(data))
                    packet = self.sock.recv(req_size)
                    time.sleep(0.001)
                    if not packet:
                        data = None
                        break

                    data += packet

                if not data:
                    break

                bio = BytesIO()
                env = pickle.loads(data)
                move = self.play(env)
                self.print(str(move))
                self.sock.sendall(pickle.dumps(move))

            else:
                raise Exception("Unknown message received:", msg)
