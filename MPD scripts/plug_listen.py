import socket
import subprocess


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('',8000))

s.listen(5)

while True:
    try:
#    while True:
        conn, addr = s.accept()

        data = conn.recv(1024)
        if data == "on" or data == "off":
            print "trying"
            p1 = subprocess.Popen(["pgrep", "-fl", "plug_"], stdout=subprocess.PIPE)
            if not(p1.stdout.read()):
                print "now trying"
                subprocess.Popen("/usr/local/bin/plug_" + data + ".sh", shell=True)
        
        print data

        conn.close()
    except:
        s.shutdown(1)
        s.close()
        break
