from gfaaccesslib.gfa import GFA

IP = '172.16.12.251'
IP = "127.0.0.1"
PORT = 32000

gfa = GFA(IP, PORT)

ans = gfa.pid.remote_set_components(1, 2, 3)
