#!/usr/bin/python

import socket
import sys

arg = sys.argv
host = '192.168.0.19'
port = 8000

if len(arg) >= 1 and (arg[1] == 'on' or arg[1] == 'off'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((host, port))
    
    s.send(arg[1])
