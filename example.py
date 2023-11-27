import socket
import argparse

from match import MatchServer


class BasePlayer(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((MatchServer.TCP_IP, MatchServer.TCP_PORT))
        self.bufsize = MatchServer.BUF_SIZE

    def play(self):
        pass

    def ready(self):
        self.sock.send(bytes("ready", "ascii"))
        go_msg = self.sock.recv(self.bufsize).decode("ascii")
        if go_msg != "go":
            raise Exception("Match server might submit 'go' before match starts!!")

        self.print("Waiting...")
        data = self.sock.recv(self.bufsize)
        self.print(data.decode("ascii"))

    def print(self, msg, *args, **kwargs):
        print("client: " + msg, *args, **kwargs)


class RandomPlayer(BasePlayer):
    def __init__(self):
        super(RandomPlayer, self).__init__()
        pass

    def play(self):
        pass


def get_player(name: str) -> BasePlayer:
    if name == "random":
        return RandomPlayer()
    else:
        raise Exception(f"Player with name {name:s} is not registered!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch othello player")
    parser.add_argument("--name", type=str, default="random", choices=["random"])
    args = parser.parse_args()

    player = get_player(args.name)
    player.ready()
