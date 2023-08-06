from gfaaccesslib.gfa import GFA

IP = '172.16.12.251'
PORT = 32000

gfa = GFA(IP, PORT)

ans = gfa.tests.version()

server = ans.get_ans('version-server')
print(("SERVER VERSION: ",server))

lib = ans.get_ans('version-lib')
print(("LIBRARY VERSION: ",lib))

module = ans.get_ans('version-module')
print(("MODULE VERSION: ", module))
