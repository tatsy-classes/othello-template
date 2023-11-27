import subprocess

if __name__ == "__main__":
    ps = subprocess.Popen(["python", "server.py"], shell=False)
    pp = subprocess.Popen(["python", "player.py"], shell=False)
    ps.communicate()
    pp.communicate()
