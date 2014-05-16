from alarm_time import get_time, set_alarm

new_setting = get_time()
set_alarm(new_setting[0], new_setting[1], new_setting[2])