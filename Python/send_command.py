import socket
import sys

if len(sys.argv) < 2 or sys.argv[1] not in ['on','off']:
    print "Argument must be on or off"
    exit(1)

message = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.19', 8000))
s.sendall(message)
s.close()