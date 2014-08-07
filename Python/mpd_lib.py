from mpd import MPDClient



class mpd_client():
    def __init__(self):
        self.client = MPDClient()
        self.connect()
    
    def connect(self):
        self.client.timeout = None
        self.client.idletimeout = None
        self.client.connect("localhost", 6600)
    
    def playing(self):
        if self.client.status()["state"] == "play":
            return True
        else:
            return False
    
    def stop(self):
        self.client.stop()
        self.client.clear()
        self.client.random(0)
    
    def instant(self):
        self.client.clear()
        self.client.load("AlarmPlaylist")
        self.client.random(1)
        self.client.play()

    def mpd_command(self, command):
        client = self.client
        dict = {"play": client.play, "pause": client.pause, "stop": self.stop, "next": client.next, "previous": client.previous, "instant": self.instant}
        try:
            if command not in ["vol up", "vol down"]:
                dict[command]()
            elif command == "vol up":
                vol = int(client.status()['volume'])
                if vol != -1 and vol < 99:
                    client.setvol(vol + 2)
                elif vol != -1:
                    client.setvol(100)
            elif command == "vol down":
                vol = int(client.status()['volume'])
                if vol != -1 and vol > 1:
                    client.setvol(vol - 2)
                elif vol != -1:
                    client.setvol(0)
        except "ConnectionError":
            client.connect("localhost", 6600)
            dict[command]()