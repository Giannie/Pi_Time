from pitftgpio import PiTFT_GPIO
import alarm_time
from time import sleep
import subprocess

pitft = PiTFT_GPIO(buttons=[False,True,True,True])

def check_backlight():
    with open("/sys/class/gpio/gpio252/value", "r") as bfile:
        if int(bfile.read()):
            return True
        else:
            return False


while True:
    if pitft.Button2:
        pitft.Backlight(False)
        subprocess.call("sudo -u pi xinput set-prop 'stmpe-ts' 'Device Enabled' 0",shell=True)
    if pitft.Button3:
        pitft.Backlight(True)
        subprocess.call("sudo -u pi xinput set-prop 'stmpe-ts' 'Device Enabled' 1",shell=True)
    if pitft.Button4 and check_backlight():
        alarm_time.toggle_alarm()
    sleep(0.1)
