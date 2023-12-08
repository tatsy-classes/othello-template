import argparse
import os
import subprocess
import sys
import threading
import time

from server import MatchServer


def run(server, n_match, verbose):
    server.run(n_match, verbose)


def client(proc):
    for line in iter(proc.stdout.readline, ""):
        print(line, end="", flush=True)


def match(f1, f2, n_match, verbose=False):
    server = MatchServer()
    thread = threading.Thread(target=run, args=(server, n_match, verbose))
    thread.start()
    time.sleep(0.1)

    args = []
    if verbose:
        args.append("--verbose")

    p1 = subprocess.Popen(
        [sys.executable, f1] + args,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    t1 = threading.Thread(target=client, args=(p1,))
    t1.start()
    time.sleep(0.1)

    p2 = subprocess.Popen(
        [sys.executable, f2] + args,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    t2 = threading.Thread(target=client, args=(p2,))
    t2.start()
    time.sleep(0.1)

    thread.join()
    t1.join()
    t2.join()

    return server.n_black, server.n_white, server.n_draw


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match between two players")
    parser.add_argument("--file1", type=str, default="player.py")
    parser.add_argument("--file2", type=str, default="player.py")
    parser.add_argument("-n", "--n_match", type=int, default=10)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if not os.path.exists(args.file1):
        raise FileExistsError("File not found:" + args.file1)

    if not os.path.exists(args.file2):
        raise FileExistsError("File not found:" + args.file2)

    match(args.file1, args.file2, args.n_match, args.verbose)
