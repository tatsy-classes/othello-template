import time
import argparse
import threading
import subprocess

from server import MatchServer


def run(server, n_match):
    server.run(n_match)


def match(f1, f2, n_match):
    server = MatchServer()
    thread = threading.Thread(target=run, args=(server, n_match))
    thread.start()
    time.sleep(0.1)

    p1 = subprocess.Popen(["python", f1], shell=False, stdout=subprocess.DEVNULL)
    time.sleep(0.1)
    p2 = subprocess.Popen(["python", f2], shell=False, stdout=subprocess.DEVNULL)
    time.sleep(0.1)

    p1.communicate()
    p2.communicate()
    thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match between two players")
    parser.add_argument("--file1", type=str, default="player.py")
    parser.add_argument("--file2", type=str, default="player.py")
    parser.add_argument("-n", "--n_match", type=int, default=10)
    args = parser.parse_args()

    match(args.file1, args.file2, args.n_match)
