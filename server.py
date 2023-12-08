import pickle
import socket
import sys

import colorama
import othello
from colorama import Fore
from othello import Player
from tqdm.auto import tqdm


def socket_send(sock: socket.socket, data: bytes) -> None:
    size = len(data)
    prefix = int.to_bytes(size, 4, "little")
    try:
        sock.sendall(prefix + data)
    except socket.error as e:
        print(str(e))


def socket_recv(sock: socket.socket, bufsize: int) -> bytes:
    data = sock.recv(4)
    size = int.from_bytes(data, "little")

    data = b""
    while len(data) < size:
        try:
            req_size = min(bufsize, size - len(data))
            packet = sock.recv(req_size)
        except socket.error as e:
            print(str(e))
            break

        data += packet

    return data


class MatchServer(object):
    TCP_IP: str = "127.0.0.1"
    TCP_PORT: int = 8080
    BUF_SIZE: int = 1024

    def __init__(self):
        colorama.init()
        self.verbose = False
        self.is_done = False
        self.n_black = 0
        self.n_white = 0
        self.n_draw = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(2)
        self.print(f"listen port {self.TCP_PORT:d}")

    def print(self, msg, *args, **kwargs):
        if self.verbose:
            print(Fore.BLUE + "[SERVER]: " + Fore.RESET, end="")
            print(msg, *args, **kwargs)
            sys.stdout.flush()

    def run(self, n_match=1, verbose=False):
        self.verbose = verbose
        black_client, black_addr = self.sock.accept()
        self.print("Got a connection from", black_addr)
        ready_msg = socket_recv(black_client, self.BUF_SIZE).decode("ascii")
        if ready_msg == "ready":
            self.print("Black is ready!")
        else:
            black_client.close()
            raise Exception("Client must send message 'ready'!!")

        white_client, white_addr = self.sock.accept()
        self.print("Got a connection from", white_addr)
        ready_msg = socket_recv(white_client, self.BUF_SIZE).decode("ascii")
        if ready_msg == "ready":
            self.print("White is ready!")
        else:
            white_client.close()
            raise Exception("Client must send message 'ready'!!")

        self.sock.settimeout(1)
        black_client.settimeout(1)
        white_client.settimeout(1)

        pbar = tqdm(range(n_match))
        for _ in pbar:
            self.print("Match start!")
            env = othello.make()
            env.reset()

            socket_send(black_client, bytes("reset", "ascii"))
            socket_send(white_client, bytes("reset", "ascii"))

            while not env.is_done():
                try:
                    client = black_client
                    if env.player == Player.BLACK:
                        client = black_client
                    elif env.player == Player.WHITE:
                        client = white_client
                    else:
                        raise Exception("Unknown player!")

                    socket_send(client, bytes("go", "ascii"))
                    data = pickle.dumps(env.copy())
                    socket_send(client, data)

                    data = socket_recv(client, self.BUF_SIZE)
                    move = pickle.loads(data)
                    env.update(move)

                except Exception as e:
                    print(str(e))
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

            pbar.set_description(f"B:{self.n_black:d}, W:{self.n_white:d}, D:{self.n_draw}")

        socket_send(black_client, bytes("finish", "ascii"))
        black_client.close()
        socket_send(white_client, bytes("finish", "ascii"))
        white_client.close()
        self.sock.close()

        self.is_done = True


if __name__ == "__main__":
    server = MatchServer()
    server.run()
