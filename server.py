import sys
import time
import pickle
import socket

import othello
import colorama
from tqdm import tqdm
from othello import Player
from colorama import Fore


class MatchServer(object):
    TCP_IP: str = "127.0.0.1"
    TCP_PORT: int = 8080
    BUF_SIZE: int = 65536

    def __init__(self):
        colorama.init()
        self.verbose = False
        self.is_done = False
        self.n_black = 0
        self.n_white = 0
        self.n_draw = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(2)
        self.print(f"listen port {self.TCP_PORT:d}")

    def print(self, msg, *args, **kwargs):
        if self.verbose:
            print(Fore.BLUE + "[SERVER]: " + Fore.RESET, end="")
            print(msg, *args, **kwargs)
            sys.stdout.flush()

    def run(self, n_match=1):
        black_client, black_addr = self.sock.accept()
        self.print("Got a connection from", black_addr)
        ready_msg = black_client.recv(self.BUF_SIZE).decode("ascii")
        if ready_msg == "ready":
            self.print("Black is ready!")
        else:
            black_client.close()
            raise Exception("Client must send message 'ready'!!")

        white_client, white_addr = self.sock.accept()
        self.print("Got a connection from", white_addr)
        ready_msg = white_client.recv(self.BUF_SIZE).decode("ascii")
        if ready_msg == "ready":
            self.print("White is ready!")
        else:
            white_client.close()
            raise Exception("Client must send message 'ready'!!")

        pbar = tqdm(range(n_match))
        for _ in pbar:
            self.print("Match start!")
            env = othello.make()
            env.reset()

            while not env.is_done():
                try:
                    client = black_client
                    if env.player == Player.BLACK:
                        client = black_client
                    elif env.player == Player.WHITE:
                        client = white_client
                    else:
                        raise Exception("Unknown player!")

                    client.sendall(bytes("go", "ascii"))
                    time.sleep(0.001)

                    data = pickle.dumps(env)
                    data_size = len(data)

                    client.sendall(int.to_bytes(data_size, 4, "little"))
                    time.sleep(0.01)
                    client.sendall(data)
                    time.sleep(0.001)

                    data = client.recv(self.BUF_SIZE)
                    if not data:
                        break

                    move = pickle.loads(data)
                    env.update(move)
                    time.sleep(0.001)

                except Exception:
                    black_client.close()
                    white_client.close()
                    self.sock.close()
                    return

            nb = env.count(Player.BLACK)
            nw = env.count(Player.WHITE)
            if nb > nw:
                self.n_black += 1
                self.print("Black win!")
            elif nb < nw:
                self.n_white += 1
                self.print("White win!")
            else:
                self.n_draw += 1
                self.print("Draw!")

            pbar.set_description(
                f"B:{self.n_black:d}, W:{self.n_white:d}, D:{self.n_draw}"
            )

        black_client.sendall(bytes("finish", "ascii"))
        black_client.close()
        white_client.sendall(bytes("finish", "ascii"))
        white_client.close()
        self.sock.close()

        self.is_done = True


if __name__ == "__main__":
    server = MatchServer()
    server.run()
