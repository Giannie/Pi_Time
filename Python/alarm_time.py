#!/usr/bin/python

import time
import string
import datetime
import subprocess
from crontab import CronTab
from time import sleep
try:
    import BBC_playlist
    import pywapi
    import texttospeech
except:
    pass

wait_time = 1
select = 1
right = 2
down = 4
up = 8
left = 16

colour_def = 5


def main_screen(lcd, lcd_string, play_state):
    message_return(lcd, lcd_string)
    if sum(play_state) > 0:
        lcd.write(0xCF)
        lcd.write(sum(play_state) - 1, True)
        lcd.write(0x80)


def button_test(n, press_before):
    wait = time.time() - press_before
    if n in [1, 2, 4, 8, 16] and wait_time / 4.0 < wait < 30:
        return True
    else:
        return False


def gen_setting(setting, hour, minute):
    set_string = setting + ' ' * (16 - len(setting)) + '\n' + add_zero(hour) + ':' + add_zero(minute) + " " * 11
    return set_string


def message_gen(string1, string2):
    if len(string1) < 17:
        string1 += ' ' * (16 - len(string1))
    if len(string2) < 17:
        string2 += ' ' * (16 - len(string2))
    return string1 + '\n' + string2


def message_return(lcd, message_string):
    lcd.message(message_string)
    lcd.write(0x80)


def get_time():
    cron = CronTab('pi')
    job = cron.find_comment('Alarm').next()
    alarm_hour = int(str(job.hour))
    alarm_min = int(str(job.minute))
    return [alarm_hour, alarm_min, not (job.is_enabled())]


def add_zero(time_int):
    if int(time_int) < 10:
        return "0" + str(time_int)
    else:
        return str(time_int)


def cur_time():
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    now = datetime.datetime.now()

    current_hour = add_zero(str(now.hour))
    current_min = add_zero(str(now.minute))
    current_day = add_zero(str(now.day))
    current_mon = add_zero(str(now.month))

    dow = weekdays[now.weekday()]

    current_time = current_hour + ":" + current_min
    current_date = dow + ' ' + current_day + "/" + current_mon

    line1 = current_time + ' ' * (16 - len(current_time + current_date)) + current_date

    return line1


def update_crontab():
    proc = subprocess.Popen(['crontab', '-lu', 'pi'], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    return output


def alarm_time(crontab, line2):
    proc = subprocess.Popen(['crontab', '-lu', 'pi'], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    if output == crontab:
        return [output, line2]
    else:
        cron = CronTab('pi')
        job = cron.find_comment('Alarm').next()

        alarm_hour = add_zero(str(job.hour))
        alarm_min = add_zero(str(job.minute))
        alarm_on = job.is_enabled()

        alarm_string = alarm_hour + ':' + alarm_min

        if alarm_on:
            line2 = "Alarm: " + alarm_string
        else:
            line2 = "Alarm off"

        line2 = line2

        return [output, line2]


def set_alarm(hour, minute, on):
    cron = CronTab('pi')
    job = cron.find_comment('Alarm').next()

    job.clear()
    job.hour.on(hour)
    job.minute.on(minute)
    if on:
        job.enable()
    else:
        job.enable(False)
    cron.write()
    return


def toggle_alarm():
    cron = CronTab('pi')
    job = cron.find_comment('Alarm').next()
    
    if job.is_enabled():
        job.enable(False)
    else:
        job.enable()
    cron.write()

def mpc_artists():
    art = []
    for i in range(27):
        art.append([])
    p1 = subprocess.Popen(["mpc", 'list', 'artist'], stdout=subprocess.PIPE)
    artists = p1.stdout.read()
    artists = artists.split('\n')
    artists_temp = []
    for artist in artists:
        if len(artist) > 3:
            if artist[0:5] == "The ":
                artist = artist[4:] + " The"
        artists_temp.append(artist)
    artists_temp.sort()
    for artist in artists_temp:
        if artist != '' and not (artist[0].lower() in string.lowercase):
            art[26] += [artist]
        elif len(artist) > 3 and artist[-4:] != " The" or 0 < len(artist) < 4:
            art[string.lowercase.index(artist[0].lower())] += [artist]
        elif artist[-4:] == " The":
            art[string.lowercase.index(artist[0].lower())] += (["The " + artist[0:-4]])
    return art


def mpc_albums(artist):
    p1 = subprocess.Popen(["mpc", "ls", artist], stdout=subprocess.PIPE)
    albums = p1.stdout.read()
    paths = albums.split('\n')[:-1]
    albums = []
    for album in paths:
        length = len(artist) + 1
        album = album[length:]
        albums.append(album)
    return [albums, paths]


def mpc_playlists():
    p1 = subprocess.Popen(["mpc", "lsplaylists"], stdout=subprocess.PIPE)
    playlists = p1.stdout.read()
    playlists = playlists.split('\n')[:-1]
    playlists.sort()
    return playlists


def mpc_load(playlist):
    subprocess.call(["mpc", "clear"])
    subprocess.call(["mpc", "load", playlist])


def mpc_add(path):
    subprocess.call(["mpc", "clear"])
    subprocess.call(["mpc", "add", path])


def mpc_play():
    subprocess.call(["mpc", "play"])


def mpc_random_check():
    p1 = subprocess.Popen("mpc", stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "volume"], stdin=p1.stdout, stdout=subprocess.PIPE)
    s = p2.stdout.read()
    s = s.split(' ')
    s = s[9]
    return s


def check_playing():
    playing = 0
    random = 0
    p1 = subprocess.Popen("mpc", stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "playing"], stdin=p1.stdout, stdout=subprocess.PIPE)
    play_string = p2.stdout.read()
    p1 = subprocess.Popen("mpc", stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "volume"], stdin=p1.stdout, stdout=subprocess.PIPE)
    s = p2.stdout.read()
    s = s.split(' ')
    random_string = s[9]
    if len(play_string) > 0:
        playing = 1
    if random_string == "on":
        random = 2
    return [playing, random]


def mpc_screen(lcd):
    press_before = time.time()
    mpc_settings = ["Play", "Pause", "Stop", "Next", "Prev", "Random", "Sleep", "Cancel Sleep", "Load"]
    random_check = 0
    mpc_string_prev = ''
    mpc_setting = 0
    current_random = 'off'
    while True:
        n = lcd.buttons()
        if mpc_setting == 5:
            if time.time() - random_check > 5:
                current_random = mpc_random_check()
            mpc_string = message_gen(mpc_settings[mpc_setting], "Currently " + current_random)
        else:
            mpc_string = message_gen(mpc_settings[mpc_setting], '')
        if mpc_string != mpc_string_prev:
            message_return(lcd, mpc_string)
            arrows(lcd)
            mpc_string_prev = mpc_string
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                mpc_setting = (mpc_setting + 1) % len(mpc_settings)
            elif n == down:
                mpc_setting = (mpc_setting - 1) % len(mpc_settings)
            elif n == left or n == right:
                break
            elif n == select and mpc_setting < 5:
                subprocess.call(["mpc", mpc_settings[mpc_setting].lower()])
                if mpc_settings[mpc_setting].lower() == "stop":
                    subprocess.call(["mpc", "clear"])
                break
            elif n == select and mpc_setting == 5:
                ran_strings = ["on", "off"]
                if current_random == "off":
                    ran = 0
                else:
                    ran = 1
                subprocess.call(["mpc", "random", ran_strings[ran]])
                break
            elif n == select and mpc_setting == 6:
                sleep_menu(lcd)
                break
            elif n == select and mpc_setting == 7:
                proc = subprocess.Popen(["pgrep", "-f", "sleep"], stdout=subprocess.PIPE)
                output = proc.stdout.read()
                output = output.replace('\n', ' ')[:-1]
                output = output.split(' ')
                command = ["kill"] + output
                subprocess.call(command)
                break
            elif n == select and mpc_setting == 8:
                type_menu(lcd)
                break
        sleep(0.1)


def sleep_menu(lcd):
    press_before = time.time()
    sleep_time = 0
    sleep_string_prev = ''
    line1 = "Sleep after"
    while True:
        n = lcd.buttons()
        sleep_string = message_gen(line1, str(sleep_time) + " minutes")
        if sleep_string != sleep_string_prev:
            message_return(lcd, sleep_string)
            arrows(lcd)
            sleep_string_prev = sleep_string
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                sleep_time += 5
            elif n == down and sleep_time > 0:
                sleep_time -= 5
            elif n == left or n == right:
                break
            elif n == select:
                if sleep_time != 0:
                    subprocess.Popen(["/usr/local/bin/music_sleep.sh", str(60 * sleep_time)])
                break
        sleep(0.1)


def type_menu(lcd):
    press_before = time.time()
    type_choice = ["Artist", "Playlist"]
    type_set = 0
    type_set_prev = ''
    line1 = "Media Type:"
    while True:
        n = lcd.buttons()
        if type_set != type_set_prev:
            type_string = line1 + ' ' * (16 - len(line1)) + '\n' + type_choice[type_set] + ' ' * (
                16 - len(type_choice[type_set]))
            message_return(lcd, type_string)
            arrows(lcd)
            type_set_prev = type_set
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                type_set = (type_set + 1) % len(type_choice)
            elif n == down:
                type_set = (type_set - 1) % len(type_choice)
            elif n == left or n == right:
                break
            elif n == select:
                if type_set == 1:
                    playlist_menu(lcd)
                    break
                elif type_set == 0:
                    letter_menu(lcd)
                    break
    sleep(0.1)


def playlist_menu(lcd):
    press_before = time.time()
    play_set = 0
    play_set_prev = ''
    line1 = "Choose Playlist:"
    playlists = mpc_playlists()
    while True:
        n = lcd.buttons()
        if play_set != play_set_prev:
            play_string = message_gen(line1, playlists[play_set][:17])
            message_return(lcd, play_string)
            arrows(lcd)
            play_set_prev = play_set
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                play_set = (play_set + 1) % len(playlists)
            elif n == down:
                play_set = (play_set - 1) % len(playlists)
            elif n == right or n == left:
                break
            elif n == select:
                if playlists[play_set][0:3] == "BBC":
                    BBC_playlist.generate()
                    subprocess.call("cp /home/pi/radio/* /var/lib/mpd/playlists", shell=True)
                    subprocess.call("chown mpd:audio /var/lib/mpd/playlists/BBC*", shell=True)
                mpc_load(playlists[play_set])
                mpc_play()
                break
        sleep(0.1)


def letter_menu(lcd):
    press_before = time.time()
    alph = list(string.ascii_uppercase)
    alph.append("Other")
    let_set = 0
    let_set_prev = ''
    line1 = "First letter:"
    while True:
        n = lcd.buttons()
        if let_set != let_set_prev:
            let_string = message_gen(line1, alph[let_set])
            let_set_prev = let_set
            message_return(lcd, let_string)
            arrows(lcd)
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                let_set = (let_set + 1) % len(alph)
            elif n == down:
                let_set = (let_set - 1) % len(alph)
            elif n == left or n == right:
                break
            elif n == select:
                artist_menu(lcd, let_set)
                break
    sleep(0.1)


def artist_menu(lcd, let_set):
    press_before = time.time()
    art_set = 0
    art_set_prev = ''
    line1 = "Choose artist:"
    artists = mpc_artists()[let_set]
    while True:
        n = lcd.buttons()
        if art_set != art_set_prev:
            art_string = message_gen(line1, artists[art_set][:17])
            message_return(lcd, art_string)
            arrows(lcd)
            art_set_prev = art_set
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                art_set = (art_set + 1) % len(artists)
            elif n == down:
                art_set = (art_set - 1) % len(artists)
            elif n == right or n == left:
                break
            elif n == select:
                try:
                    album_menu(lcd, artists, art_set)
                except:
                    message_string = message_gen("Can't play that, ", "sorry")
                    message_return(lcd, message_string)
                    sleep(2)
                break
    sleep(0.1)


def album_menu(lcd, artists, art_set):
    press_before = time.time()
    alb_set = 0
    alb_set_prev = ''
    line1 = "Choose album:"
    fun = mpc_albums(artists[art_set])
    albums = fun[0]
    paths = fun[1]
    while True:
        n = lcd.buttons()
        if alb_set != alb_set_prev:
            alb_string = message_gen(line1, albums[alb_set][:17])
            message_return(lcd, alb_string)
            arrows(lcd)
            alb_set_prev = alb_set
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                alb_set = (alb_set + 1) % len(albums)
            elif n == down:
                alb_set = (alb_set - 1) % len(albums)
            elif n == left or n == right:
                break
            elif n == select:
                mpc_add(paths[alb_set])
                mpc_play()
                break
        sleep(0.1)


def cur_track_screen(lcd):
    press_before = time.time()
    time_track = time.time()
    p1 = subprocess.Popen(["mpc", "current"], stdout=subprocess.PIPE)
    song = p1.stdout.read()
    if '-' in song:
        song = song[song.index('-') + 2:-1]
    elif len(song) == 0:
        song = "Nothing playing"
    else:
        song = song[:-1]
    song_string = message_gen("Current song:", song[:17])
    message_return(lcd, song_string)
    while True:
        n = lcd.buttons()
        if time.time() - time_track > 5:
            break
        if button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            break
        sleep(0.1)


def main_menu(lcd, colour):
    sleep(wait_time / 2.0)
    menus = ["Set Alarm", "Weather Report", "Set Backlight", "Power Management", "IP Addresses"]
    menu = 0
    menu_prev = ''
    press_before = time.time()
    while True:
        n = lcd.buttons()
        if menu != menu_prev:
            menu_string = menus[menu] + ' ' * (16 - len(menus[menu])) + "\n" + ' ' * 16
            message_return(lcd, menu_string)
            arrows(lcd)
            menu_prev = menu
        if button_test(n, press_before) and time.time() - press_before > wait_time / 4.0:
            press_before = time.time()
            if n == up:
                menu = (menu + 1) % len(menus)
            elif n == down:
                menu = (menu - 1) % len(menus)
            elif n == left or n == right:
                break
            elif n == select:
                if menu == 0:
                    alarm_set_screen(lcd)
                    break
                elif menu == 1:
                    weather_menu(lcd)
                    break
                elif menu == 2:
                    colour = backlight_menu(lcd)
                    break
                elif menu == 3:
                    power_menu(lcd)
                    break
                elif menu == 4:
                    ip_menu(lcd)
                    break
        sleep(0.1)
    return colour


def alarm_set_screen(lcd):
    settings = ["Set hour:", "Set minute:"]
    setting = 0
    hour = 7
    minute = 0
    set_string_prev = ''
    flash = True
    set_bef = time.time()
    press_before = time.time()
    on = True
    while True:
        n = lcd.buttons()
        if time.time() - press_before > 30:
            break
        set_string = gen_setting(settings[setting], hour, minute)
        if set_string != set_string_prev:
            message_return(lcd, set_string)
            set_string_prev = set_string
        if time.time() - set_bef > 0.5:
            if setting == 0:
                lcd.write(0xC0)
                if flash:
                    message_return(lcd, '  ')
                else:
                    message_return(lcd, add_zero(hour))
            elif setting == 1:
                lcd.write(0xC3)
                if flash:
                    message_return(lcd, '  ')
                else:
                    message_return(lcd, add_zero(minute))
            flash = not flash
            set_bef = time.time()
        if button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == select:
                set_alarm(hour, minute, on)
                break
            elif n == right:
                message_return(lcd, set_string)
                setting = (setting + 1) % len(settings)
            elif n == left:
                message_return(lcd, set_string)
                setting = (setting - 1) % len(settings)
            elif setting == 0:
                if n == up:
                    hour = (hour + 1) % 24
                    set_string = gen_setting(settings[setting], hour, minute)
                    message_return(lcd, set_string)
                    flash = not flash
                    set_string_prev = set_string
                    press_before = time.time()
                elif n == down:
                    hour = (hour - 1) % 24
                    set_string = gen_setting(settings[setting], hour, minute)
                    message_return(lcd, set_string)
                    flash = not flash
                    set_string_prev = set_string
                    press_before = time.time()
            elif setting == 1:
                if n == up:
                    minute = (minute + 5) % 60
                    set_string = gen_setting(settings[setting], hour, minute)
                    message_return(lcd, set_string)
                    flash = not flash
                    set_string_prev = set_string
                    press_before = time.time()
                elif n == down:
                    minute = (minute - 5) % 60
                    set_string = gen_setting(settings[setting], hour, minute)
                    message_return(lcd, set_string)
                    flash = not flash
                    set_string_prev = set_string
                    press_before = time.time()
        sleep(0.1)


def backlight_menu(lcd):
    col_string = ['Red', 'Yellow', 'Green', 'Teal', 'Blue', 'Violet']
    colours = [lcd.RED, lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.BLUE, lcd.VIOLET]
    setting = colour_def
    set_string_prev = ''
    press_before = time.time()
    while True:
        n = lcd.buttons()
        set_string = message_gen(col_string[setting], '')
        if set_string != set_string_prev:
            message_return(lcd, set_string)
            arrows(lcd)
            lcd.backlight(colours[setting])
            set_string_prev = set_string
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                setting = (setting + 1) % len(col_string)
            elif n == down:
                setting = (setting - 1) % len(col_string)
            elif n == left or n == right:
                break
            elif n == select:
                break
        sleep(0.1)
    return setting


def power_menu(lcd):
    press_before = time.time()
    setting = 0
    setting_prev = ''
    pow_string = ['Shutdown', 'Reboot', 'Cancel']
    while True:
        n = lcd.buttons()
        if setting != setting_prev:
            set_string = message_gen(pow_string[setting], '')
            message_return(lcd, set_string)
            arrows(lcd)
            setting_prev = setting
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                setting = (setting + 1) % len(pow_string)
            elif n == down:
                setting = (setting - 1) % len(pow_string)
            elif n == left or n == right:
                break
            elif setting == 2 and n == select:
                break
            elif n == select:
                confirmation = confirm_menu(lcd)
                if confirmation:
                    if setting == 0:
                        subprocess.call("poweroff")
                    elif setting == 1:
                        subprocess.call("reboot")
                else:
                    break
        sleep(0.1)


def confirm_menu(lcd):
    press_before = time.time()
    setting_confirm = 0
    setting_prev = ''
    confirm = ["Yes", "No"]
    con = "Are you sure?"
    confirmation = False
    while True:
        n = lcd.buttons()
        if setting_confirm != setting_prev:
            set_string = message_gen(con, confirm[setting_confirm])
            message_return(lcd, set_string)
            setting_prev = setting_confirm
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                setting_confirm = (setting_confirm + 1) % len(confirm)
            elif n == down:
                setting_confirm = (setting_confirm - 1) % len(confirm)
            elif n == select and setting_confirm != 1:
                confirmation = True
                break
            elif n == select and setting_confirm == 1:
                confirmation = False
                break
        sleep(0.1)
    return confirmation


def ip_menu(lcd):
    ip_settings = ["Wifi", "Ethernet"]
    press_before = time.time()
    ip_set = 0
    ip_set_prev = ''
    while True:
        n = lcd.buttons()
        if ip_set != ip_set_prev:
            n = lcd.buttons()
            if ip_set == 0:
                p1 = subprocess.Popen(["ifconfig", "wlan0"], stdout=subprocess.PIPE)
            else:
                p1 = subprocess.Popen(["ifconfig", "eth0"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["grep", "inet"], stdin=p1.stdout, stdout=subprocess.PIPE)
            ip_address = p2.stdout.read()
            if len(ip_address) == 0:
                ip_address = "Not connected"
            else:
                ip_address = ip_address.split(' ')
                ip_address = ip_address[11][5:]
            ip_str = message_gen(ip_settings[ip_set], ip_address)
            message_return(lcd, ip_str)
            arrows(lcd)
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                ip_set = (ip_set + 1) % len(ip_settings)
            elif n == down:
                ip_set = (ip_set - 1) % len(ip_settings)
            elif n == select or n == left or n == right:
                break
        sleep(0.1)


def get_ip_address(interface):
    if interface == "ethernet":
        inter = "eth0"
    elif interface == "wifi":
        inter = "wlan0"
    else:
        print "Interface must be wifi or ethernet"
        return False
    p1 = subprocess.Popen(["ifconfig", inter], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "inet"], stdin=p1.stdout, stdout=subprocess.PIPE)
    ip_address = p2.stdout.read()
    if len(ip_address) == 0:
        ip_address = "Not connected"
    else:
        ip_address = ip_address.split(' ')
        ip_address = ip_address[11][5:]
    return ip_address


def arrows(lcd):
    lcd.write(0xCF)
    lcd.write(3, True)
    lcd.write(0x80)


def get_weather(number):
    """

    :rtype : dict
    """
    weather = pywapi.get_weather_from_weather_com('UKXX0085', units='metric')
    forecasts = weather['forecasts']
    forecast_dict = forecasts[number]
    return forecast_dict


def forecast_menu(lcd, number):
    press_before = time.time()
    fore = Forecast(number)
    high_low_screen = message_gen("High: " + fore.high, "Low: " + fore.low)
    day_text_screen = message_gen(fore.day_text, 'Rain: ' + fore.day_chance_precip)
    night_text_screen = message_gen(fore.night_text, "Rain: " + fore.night_chance_precip)
    if len(fore.day) > 0:
        settings = [message_gen("Full Report", ''), high_low_screen, day_text_screen, night_text_screen]
    else:
        settings = [message_gen("Full Report", ''), high_low_screen, night_text_screen]
    setting = 0
    setting_prev = ''
    full_report1 = fore.full_report1
    full_report2 = fore.full_report2
    while True:
        n = lcd.buttons()
        if setting != setting_prev:
            message_return(lcd, settings[setting])
            arrows(lcd)
            if setting == 2 and len(fore.day) > 0:
                sun_moon(lcd, 0)
            elif setting == 2 or setting == 3:
                sun_moon(lcd, 1)
            setting_prev = setting
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                setting = (setting + 1) % len(settings)
            elif n == down:
                setting = (setting - 1) % len(settings)
            elif n == left or n == right:
                break
            elif n == select:
                if setting == 0:
                    subprocess.call(["mpc", "pause"])
                    texttospeech.play_file(full_report1)
                    texttospeech.play_file(full_report2)
                    subprocess.call(["mpc", "play"])
                    break
                else:
                    break
        sleep(0.1)


def weather_menu(lcd):
    press_before = time.time()
    settings = ["Today", "Tomorrow"]
    setting = 0
    setting_prev = ''
    while True:
        n = lcd.buttons()
        if setting != setting_prev:
            message_string = message_gen(settings[setting], '')
            message_return(lcd, message_string)
            arrows(lcd)
            setting_prev = setting
        if time.time() - press_before > 30:
            break
        elif button_test(n, press_before) and time.time() - press_before > wait_time / 2.0:
            press_before = time.time()
            if n == up:
                setting = (setting + 1) % len(settings)
            elif n == down:
                setting = (setting - 1) % len(settings)
            elif n == left or n == right:
                break
            elif n == select:
                forecast_menu(lcd, setting)
                break
        sleep(0.1)


def sun_moon(lcd, symbol):
    if symbol in [0, 1]:
        symbol += 4
        lcd.write(0x8F)
        lcd.write(symbol, True)
        lcd.write(0x80)


class Forecast:
    def __init__(self, number):
        """

        :type self: dict
        """
        self.forecast = get_weather(number)
        self.high = self.forecast['high']
        self.low = self.forecast['low']
        self.night = self.forecast['night']
        self.night_text = self.night['text']
        self.night_chance_precip = self.night['chance_precip']
        try:
            self.day = self.forecast['day']
            self.day_text = self.day['text']
            self.day_chance_precip = self.day['chance_precip']
        except:
            self.day = ''
        if number == 0 and len(self.day) > 0:
            self.dow = "Today"
        elif number == 0:
            self.dow = "Tonight"
            self.day_text = self.night_text
            self.day_chance_precip = self.night_chance_precip
        else:
            self.dow = self.forecast['day_of_week']
        self.full_report1 = self.dow + " will be " + self.day_text + " with a " \
            + self.day_chance_precip + " percent chance of rain."
        self.full_report2 = "Temperatures will reach a high of " + self.high + " and a low of " + self.low
