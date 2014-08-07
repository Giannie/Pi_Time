#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This is a trivial PyGTK example
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009


import gtk
import gobject
import time
import pango
import alarm_time
import subprocess
import sys
import datetime
import time
import draw_clock
from mpd_lib import mpd_client


class PyApp(gtk.Window):
    def __init__(self):
        self.client = mpd_client()
        self.analog = False
        self.press_before = 0
        self.old_second = None
        self.clock_counter = 0
        self.clock_color = '"#EAE6EF"'
        self.text_color = '"#EAE6EF"'
        self.output = ""
        self.line2 = ""
        super(PyApp, self).__init__()
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))

        self.connect("destroy", gtk.main_quit)
#        self.set_position(gtk.WIN_POS_CENTER)
        if sys.platform == 'darwin' or (len(sys.argv) > 1 and sys.argv[1] == 'window'):
            self.set_size_request(320, 240)
        else:
            self.fullscreen()

        drawing_area = gtk.DrawingArea()
        drawing_area.set_size_request(312, 232)
        self.drawing_area = drawing_area

        drawing_area.connect("expose-event", self.create_analog_clock)

        self.create_main_screen()
        self.create_set_alarm_screen()
        self.create_menu_screen()
        self.create_system_screen()
        self.create_analog_clock_screen()
        self.create_music_screen()
        
        btn_on = gtk.Button('<span color="purple" font="15">Plug On</span>')
        btn_on.child.set_use_markup(True)
        btn_on.connect("clicked", self.plug_on)
        btn_off = gtk.Button('<span color="purple" font="15">Plug Off</span>')
        btn_off.child.set_use_markup(True)
        btn_off.connect("clicked",self.plug_off)

#        pause_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PAUSE,gtk.ICON_SIZE_LARGE_TOOLBAR)


#        fix=gtk.Fixed()
#        fix.put(self.clock_label,20,20)
#        fix.put(self.alarm_label,20,60)
#        fix.put(btn1,20,130)
#        self.fix=fix
#        fix2 = gtk.Fixed()
#        fix2.put(btn2,20,130)
#        self.fix2 = fix2
#        self.add(fix)
        #self.show_main_screen()
        self.show_analog_clock()
        self.shown = True

    def create_main_screen(self):
        self.clock_label = gtk.Label()
        self.clock_label.modify_font(pango.FontDescription("helvetica 40"))
        self.date_label = gtk.Label()
        self.date_label.modify_font(pango.FontDescription("helvetica 22"))
        self.alarm_label = gtk.Label()
        self.alarm_label.modify_font(pango.FontDescription("helvetica 24"))

        self.update_clock()
        self.update_alarm()
        btn_menu = gtk.Button('<span color=' + self.text_color + ' font="14">Menu</span>')
        btn_menu.child.set_use_markup(True)
        btn_menu.connect("clicked", self.show_menu_screen)
        btn_toggle_alarm = gtk.Button('<span color=' + self.text_color + ' font="14">Alarm Off</span>')
        btn_toggle_alarm.child.set_use_markup(True)
        btn_toggle_alarm.connect("clicked", self.toggle_alarm)
        self.btn_toggle_alarm = btn_toggle_alarm
        self.update_alarm_button()
        btn_set_alarm = gtk.Button('<span color=' + self.text_color + ' font="14">Set Alarm</span>')
        btn_set_alarm.child.set_use_markup(True)
        btn_set_alarm.connect("clicked", self.set_alarm_screen)

        self.btn_set_alarm = btn_set_alarm
        main_screen_vbox = gtk.VBox(False, 0)
        hbox_main_clock = gtk.HBox(False, 5)
        hbox_main_alarm = gtk.HBox(False, 5)
        hbox_main_buttons = gtk.HBox(True, 1)
        hbox_date = gtk.HBox(False, 5)

        halign_date = gtk.Alignment(0.5, 0, 0, 0)
        halign_date.add(hbox_date)
        hbox_date.add(self.date_label)
        #valign = gtk.Alignment(0, 1, 0, 0)
        #main_screen_vbox.pack_end(valign)
        
        main_screen_text_vbox = gtk.VBox(False, 0)
        #valign2 = gtk.Alignment(0, 0, 0, 0)
        #valign2.add(main_screen_text_vbox)
        
        vbox_main_buttons = gtk.VBox(False, 0)

        hbox_main_clock.add(self.clock_label)
        hbox_main_alarm.add(self.alarm_label)
        hbox_main_buttons.add(btn_toggle_alarm)
        hbox_main_buttons.add(btn_set_alarm)
        hbox_main_buttons.add(btn_menu)

        hbox_main_buttons.set_size_request(-1,40)

        # for item in hbox_main_buttons.get_children():
        #     item.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#3A1465"))
        #     item.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("#3A1465"))
        #     item.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("#3A1465"))
        #     item.modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("#3A1465"))

        btn_style = btn_menu.get_style().copy()
        btn_style.bg[gtk.STATE_NORMAL] = gtk.gdk.color_parse("#3A1465")
        btn_style.bg[gtk.STATE_ACTIVE] = gtk.gdk.color_parse("#3A1465")
        btn_style.bg[gtk.STATE_PRELIGHT] = gtk.gdk.color_parse("#3A1465")
        btn_style.bg[gtk.STATE_SELECTED] = gtk.gdk.color_parse("#3A1465")

        self.btn_style = btn_style

        for item in hbox_main_buttons.get_children():
            item.set_style(self.btn_style)

        halign_main_clock = gtk.Alignment(0.5,0,0,0)
        halign_main_clock.add(hbox_main_clock)
        
        halign_main_alarm = gtk.Alignment(0.5,0,0,0)
        halign_main_alarm.add(hbox_main_alarm)
        
        halign_main_buttons = gtk.Alignment(0.5,0,0,0)
        halign_main_buttons.add(hbox_main_buttons)
        
        
        main_screen_text_vbox.pack_start(halign_main_clock, False,False,10)
        main_screen_text_vbox.pack_start(halign_date, False, False, 0)
        main_screen_text_vbox.pack_start(halign_main_alarm,False,False,10)
        vbox_main_buttons.pack_end(halign_main_buttons, False, False, 0)
        
        main_screen_vbox.pack_start(main_screen_text_vbox)
        main_screen_vbox.pack_start(vbox_main_buttons)
        
        self.main_screen_vbox = main_screen_vbox

    def create_set_alarm_screen(self):
        btn_set_alarm_cancel = gtk.Button()
        btn_set_alarm_cancel.set_label('<span color=' + self.text_color + ' font="14">Cancel</span>')
        btn_set_alarm_cancel.connect("clicked", self.cancel_set_alarm)
        btn_set_alarm_cancel.child.set_use_markup(True)

        btn_set_alarm_screen = gtk.Button()
        btn_set_alarm_screen.set_label('<span color=' + self.text_color + ' font="14">Set Alarm</span>')
        btn_set_alarm_screen.connect("clicked", self.set_alarm)
        btn_set_alarm_screen.child.set_use_markup(True)


        self.vbox_set_alarm = gtk.VBox(False, 0)

        self.set_alarm_table = gtk.Table(5,3,False)

        self.alarm_hour_setting = 7
        self.alarm_minute_setting = 0

        self.alarm_minute = gtk.Label()
        self.alarm_minute.modify_font(pango.FontDescription("helvetica 45"))

        self.alarm_hour = gtk.Label()
        self.alarm_hour.modify_font(pango.FontDescription("helvetica 45"))

        self.update_alarm_set_screen()

        self.alarm_colon = gtk.Label()
        self.alarm_colon.modify_font(pango.FontDescription("helvetica 45"))
        self.alarm_colon.set_markup('<span color="purple">:</span>')

        self.set_alarm_table.attach(self.alarm_hour,0,1,0,1)
        self.set_alarm_table.attach(self.alarm_colon,1,2,0,1)
        self.set_alarm_table.attach(self.alarm_minute,2,3,0,1)

        hbox_set_alarm = gtk.HBox(False,0)
        halign_set_alarm = gtk.Alignment(0.5,0,0,0)
        halign_set_alarm.add(hbox_set_alarm)



        hbox_set_alarm.add(self.set_alarm_table)

        self.vbox_set_alarm.pack_end(halign_set_alarm,False,False,0)

        self.valign_set_alarm = gtk.Alignment(0.5,0.5,0,0)
        self.valign_set_alarm.add(self.vbox_set_alarm)

        self.vbox_set_alarm_window = gtk.VBox(False, 0)
        self.vbox_set_alarm_window.pack_start(self.valign_set_alarm)
#        vbox_set_alarm_buttons = gtk.VBox(False,0)
        valign_set_alarm_buttons = gtk.Alignment(0.5, 1, 0, 0)
        hbox_set_alarm_buttons = gtk.HBox(True, 1)
        hbox_set_alarm_buttons.set_size_request(-1,40)
        halign_set_alarm_buttons = gtk.Alignment(0,0,0,0)
        halign_set_alarm_buttons.add(hbox_set_alarm_buttons)
        hbox_set_alarm_buttons.add(btn_set_alarm_screen)
        hbox_set_alarm_buttons.add(btn_set_alarm_cancel)

        for item in hbox_set_alarm_buttons.get_children():
            item.set_style(self.btn_style)


        valign_set_alarm_buttons.add(halign_set_alarm_buttons)
        self.vbox_set_alarm_window.pack_end(valign_set_alarm_buttons)

        self.add_hour_btn = gtk.Button()
        self.subtract_hour_btn = gtk.Button()
        add_image = gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_LARGE_TOOLBAR)
        add_image2 = gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_LARGE_TOOLBAR)
        subtract_image = gtk.image_new_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_LARGE_TOOLBAR)
        subtract_image2 = gtk.image_new_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_LARGE_TOOLBAR)
#        self.add_minute_btn = gtk.Button(stock=gtk.STOCK_ADD)
        self.add_minute_btn = gtk.Button()
        self.add_minute_btn.add(add_image)
        self.subtract_minute_btn = gtk.Button()
        self.subtract_minute_btn.add(subtract_image)
        self.add_hour_btn.add(add_image2)
        self.subtract_hour_btn.add(subtract_image2)
        self.set_alarm_table.attach(self.add_hour_btn,0,1,1,2)
        self.set_alarm_table.attach(self.subtract_hour_btn,0,1,2,3)
        self.set_alarm_table.attach(self.add_minute_btn,2,3,1,2)
        self.set_alarm_table.attach(self.subtract_minute_btn,2,3,2,3)

        self.add_hour_btn.connect("clicked", self.change_alarm_screen)
        self.subtract_hour_btn.connect("clicked", self.change_alarm_screen)
        self.add_minute_btn.connect("clicked", self.change_alarm_screen)
        self.subtract_minute_btn.connect("clicked", self.change_alarm_screen)
        
        for item in self.set_alarm_table.get_children():
            if type(item) == type(self.add_hour_btn):
                item.set_style(self.btn_style)

    def create_menu_screen(self):
        system_button = gtk.Button('<span color=' + self.text_color + ' font="15">System</span>')
        music_button = gtk.Button('<span color=' + self.text_color + ' font="15">Music</span>')
        cancel_button = gtk.Button('<span color=' + self.text_color + ' font="15">Cancel</span>')
        clock_button = gtk.Button('<span color=' + self.text_color + ' font="15">Clock</span>')

        system_button.child.set_use_markup(True)
        music_button.child.set_use_markup(True)
        cancel_button.child.set_use_markup(True)
        clock_button.child.set_use_markup(True)

        cancel_button.connect("clicked", self.menu_cancel)
        system_button.connect("clicked", self.show_system_screen)

        music_button.connect("clicked", self.show_music_screen)
        clock_button.connect("clicked", self.show_analog_clock)

        menu_vbox = gtk.VBox(True, 0)
        
        menu_vbox.pack_start(clock_button)
        menu_vbox.pack_start(system_button)
        menu_vbox.pack_start(music_button)
        menu_vbox.pack_start(cancel_button)

        for item in menu_vbox:
            item.set_style(self.btn_style)

        self.menu_vbox = menu_vbox

    def create_system_screen(self):
        self.eth_label = gtk.Label()
        self.wifi_label = gtk.Label()
        self.eth_label.modify_font(pango.FontDescription("helvetica 20"))
        self.wifi_label.modify_font(pango.FontDescription("helvetica 20"))
        self.update_ip()
        system_vbox = gtk.VBox(False, 0)
        system_vbox.add(self.eth_label)
        system_vbox.add(self.wifi_label)
        btn_system_cancel = gtk.Button('<span color=' + self.text_color + ' font="15">Cancel</span>')
        btn_system_cancel.set_style(self.btn_style)
        btn_system_cancel.connect("clicked", self.show_main_screen)
        btn_system_cancel.child.set_use_markup(True)
        btn_system_cancel.set_size_request(-1,40)
        system_vbox.add(btn_system_cancel)
        self.system_vbox = system_vbox
    
    def create_analog_clock_screen(self):
        self.clock_button = gtk.Button()
        self.clock_button.connect("clicked", self.show_main_screen_analog)
        #draw_clock.draw_now('/home/pi/Pi_Time/Python/clock/')
        #self.clock_image = gtk.image_new_from_file('/home/pi/Pi_Time/Python/clock/clock.png')
        #self.clock_image = gtk.image_new_from_file('/home/pi/Pi_Time/Python/clock/' + time.strftime('%I-%M-%S').lstrip('0').replace('-0','-') + '.png')
        #self.clock_button.add(self.clock_image)
        black = gtk.gdk.Color(6400, 6400, 6440)
        self.clock_button.modify_bg(gtk.STATE_NORMAL, black)
        self.clock_button.modify_bg(gtk.STATE_ACTIVE, black)
        self.clock_button.modify_bg(gtk.STATE_PRELIGHT, black)
        self.clock_button.modify_bg(gtk.STATE_SELECTED, black)
        self.clock_button.add(self.drawing_area)

    def create_analog_clock(self, area, event):
        drawable = self.drawing_area.window
        self.drawable = drawable
        self.win_style = self.drawing_area.get_style()
        #self.gc = self.win_style.fg_gc[gtk.STATE_NORMAL]
        self.gc_back = self.drawable.new_gc()
        #self.gc.set_rgb_fg_color(gtk.gdk.color_parse('blue'))
        #self.gc_line = self.win_style.fg_gc[gtk.STATE_NORMAL]
        self.gc_line = self.drawable.new_gc()
        self.gc_circle = self.drawable.new_gc()
        #self.gc.background = gtk.gdk.color_parse('black')
        #self.drawable.background = gtk.gdk.color_parse('black')
        #color = self.drawing_area.get_colormap().alloc("purple")
        #self.gc.foreground = color
        self.gc_line.line_width = 2
        self.gc_circle.line_width = 2
        #print self.gc.clip_mask.width
        #self.drawable.draw_line(self.gc, 10, 10, 20, 30)
        #self.drawable.draw_rectangle(self.gc, True, 0, 0, 312, 232)
        #color = self.drawing_area.get_colormap().alloc("purple")
        #colormap = gtk.gdk.Colormap(gtk.gdk.Visual())
        #color = colormap.alloc_color('purple', writeable=FALSE, best_match=TRUE)
        color = gtk.gdk.color_parse('purple')
        self.gc_line.set_rgb_fg_color(color)
        self.gc_circle.set_rgb_fg_color(gtk.gdk.color_parse('grey'))
        self.gc_back.set_rgb_fg_color(gtk.gdk.color_parse('black'))
        #self.gc_line.set_foreground(gtk.gdk.color_parse('black'))
        #print self.gc_line.foreground
        #self.gc.foreground = gtk.gdk.color('purple')
        self.drawable.draw_rectangle(self.gc_back, True, 0, 0, self.get_size()[0] - 8, self.get_size()[1] - 8)
        #self.drawable.draw_line(self.gc_line, 5 * datetime.datetime.now().second, 10, 20, 30)
        minute_s = draw_clock.minute_start(datetime.datetime.now().minute, self.get_size())
        minute_e = draw_clock.minute_end(datetime.datetime.now().minute, self.get_size())
        minute = minute_s + minute_e
        hour_s = draw_clock.hour_start(datetime.datetime.now().hour,datetime.datetime.now().minute, self.get_size())
        hour_e = draw_clock.hour_end(datetime.datetime.now().hour,datetime.datetime.now().minute, self.get_size())
        hour = hour_s + hour_e
        second_center = draw_clock.second_center(datetime.datetime.now(), self.get_size())
        seconds = second_center + (8, 8, 0, 360*64)
        self.drawable.draw_line(self.gc_line, *minute)
        self.drawable.draw_line(self.gc_line, *hour)
        self.drawable.draw_arc(self.gc_circle, True, *seconds)
    
    def create_music_screen(self):
        music_vbox = gtk.VBox(False, 0)
        
        play_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_LARGE_TOOLBAR)
        pause_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_LARGE_TOOLBAR)
        stop_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_LARGE_TOOLBAR)
        next_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_NEXT, gtk.ICON_SIZE_LARGE_TOOLBAR)
        prev_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PREVIOUS, gtk.ICON_SIZE_LARGE_TOOLBAR)
        add_image_vol = gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_LARGE_TOOLBAR)
        subtract_image_vol = gtk.image_new_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_LARGE_TOOLBAR)
        
        self.play_image = play_image
        self.pause_image = pause_image
        
        button_play = gtk.Button()
        button_pause = gtk.Button()
        #button_pause = gtk.Button()
        button_stop = gtk.Button()
        button_next = gtk.Button()
        button_prev = gtk.Button()
        button_exit = gtk.Button('<span color=' + self.text_color + ' font="15">Exit</span>')
        button_add_vol = gtk.Button()
        button_subtract_vol = gtk.Button()
        button_instant = gtk.Button('<span color=' + self.text_color + ' font="12">Instant\n Music</span>')
        button_choose = gtk.Button('<span color=' + self.text_color + ' font="12">Choose\n Music</span>')
        
        self.button_play = button_play
        self.button_pause = button_pause
        self.button_stop = button_stop
        self.button_next = button_next
        self.button_prev = button_prev
        self.button_exit = button_exit
        self.button_add_vol = button_add_vol
        self.button_subtract_vol = button_subtract_vol
        self.button_instant = button_instant
        self.button_choose = button_choose
        
        self.button_exit.child.set_use_markup(True)
        self.button_instant.child.set_use_markup(True)
        self.button_choose.child.set_use_markup(True)
        
        mpc_label = gtk.Label()
        mpc_label.set_markup('<span color=' + self.clock_color + '>Not Playing</span>')
        mpc_label.modify_font(pango.FontDescription("helvetica 14"))
        mpc_label.set_justify(gtk.JUSTIFY_CENTER)
        mpc_label.set_size_request(320,-1)
        
        volume_label = gtk.Label()
        volume_label.set_markup('<span color=' + self.clock_color + '>N/A</span>')
        volume_label.modify_font(pango.FontDescription("helvetica 18"))
        
        self.mpc_label = mpc_label
        
        #if self.client.client.status()['state'] == "play":
        #    button_play_pause.add(pause_image)
        #else:
        #    button_play_pause.add(play_image)
        button_play.add(play_image)
        button_pause.add(pause_image)
        button_stop.add(stop_image)
        button_next.add(next_image)
        button_prev.add(prev_image)
        button_add_vol.add(add_image_vol)
        button_subtract_vol.add(subtract_image_vol)
        #button.child.set_use_markup(True)
        
        
        #button_pause.connect("clicked", self.mpc_ctrl)
        
        
        table = gtk.Table(5,3,True)
        table.attach(button_play, 1, 2, 1, 2)
        #table.attach(button_pause, 1, 2, 1, 2)
        table.attach(button_stop, 1, 2, 2, 3)
        table.attach(button_prev, 0, 1, 2, 3)
        table.attach(button_next, 2, 3, 2, 3)
        table.attach(button_exit, 2, 3, 4, 5)
        table.attach(button_subtract_vol, 0, 1, 3, 4)
        table.attach(button_add_vol, 2, 3, 3, 4)
        table.attach(button_instant, 0, 1, 4, 5)
        table.attach(button_choose, 1, 2, 4, 5)
        for item in table.get_children():
            item.set_style(self.btn_style)
            if item not in [button_exit, button_choose]:
                item.connect("clicked", self.mpc_ctrl)
        button_pause.set_style(self.btn_style)
        button_pause.connect("clicked", self.mpc_ctrl)
        button_exit.connect("clicked", self.show_main_screen)
        music_vbox.pack_start(table)
        table.attach(mpc_label, 0, 3, 0, 1, yoptions=gtk.EXPAND)
        table.attach(volume_label, 1, 2, 3, 4)
        self.volume_label = volume_label
        self.music_vbox = music_vbox
        self.music_table = table
        table.set_row_spacing(0, 5)
    
    def update_music_screen(self):
        if self.music_vbox in self.get_children():
            try:
                self.client.connect()
            except:
                pass
            if self.client.client.status()['state'] == "play" and self.button_pause not in self.music_table.get_children():
                self.music_table.remove(self.button_play)
                self.music_table.attach(self.button_pause, 1, 2, 1, 2)
            elif self.client.client.status()['state'] != "play" and self.button_play not in self.music_table.get_children():
                self.music_table.remove(self.button_pause)
                self.music_table.attach(self.button_play, 1, 2, 1, 2)
                self.mpc_label.set_markup('<span color=' + self.clock_color + '>Not Playing</span>')
            if self.client.client.status()['state'] in ["play", "pause"]:
                self.mpc_label.set_markup('<span color=' + self.clock_color + '>' + self.client.client.currentsong()['title'] + '\n' + self.client.client.currentsong()['artist'] + '</span>')
            else:
                self.mpc_label.set_markup('<span color=' + self.clock_color + '>Not Playing</span>')
            if self.client.client.status()['volume'] != '-1':
                self.volume_label.set_markup('<span color=' + self.clock_color + '>' + self.client.client.status()['volume'] + '%' + '</span>')
            else:
                self.volume_label.set_markup('<span color=' + self.clock_color + '>N/A</span>')
            self.refresh_music_screen()
        return True
            

    def update_analog_clock(self):
        # if self.old_second != datetime.datetime.now().second:
        #     for child in self.clock_button.get_children():
        #         self.clock_button.remove(child)
        #     self.clock_image.clear()
        #     draw_clock.draw_now('/home/pi/Pi_Time/Python/clock/')
        #     self.clock_image = gtk.image_new_from_file('/home/pi/Pi_Time/Python/clock/clock.png')
        #     #self.clock_image = gtk.image_new_from_file('/home/pi/Pi_Time/Python/clock/' + time.strftime('%I-%M-%S').lstrip('0').replace('-0','-') + '.png')
        #     self.clock_button.add(self.clock_image)
        #     self.old_clock_file = self.clock_file()
        #     self.show_all()
        #     self.old_second = datetime.datetime.now().second
        # return True
        if self.analog:
            self.drawing_area.get_window().invalidate_rect(self.drawing_area.get_allocation(), False)
        return self.analog

    def show_main_screen_analog(self, widget=None):
        self.analog = False
        self.show_main_screen()
    
    def show_music_screen(self, widget=None):
        self.press_before = time.time()
        self.clear_screen()
        self.add(self.music_vbox)
        self.update_music_screen()
        self.show_all()
    
    def refresh_music_screen(self, widget=None):
        self.clear_screen()
        self.add(self.music_vbox)
        self.show_all()
    
    def screensaver(self):
        if time.time() - self.press_before > 300:
            self.show_analog_clock()
        return True
    
    def mpc_ctrl(self, widget=None):
        self.press_before = time.time()
        dict = {self.button_play: "play", self.button_pause: "pause", self.button_stop: "stop", self.button_next: "next", self.button_prev: "previous", self.button_add_vol: "vol up", self.button_subtract_vol: "vol down", self.button_instant: "instant"}
        self.client.mpd_command(dict[widget])
        self.refresh_music_screen()
        #self.show_main_screen()
    
    def clock_file(self):
        return str(datetime.datetime.now().hour % 12) + '-' + str(datetime.datetime.now().minute % 60) + '.png'

    def show_analog_clock(self, widget=None):
        self.analog = True
        gtk.timeout_add(200, self.update_analog_clock)
        self.press_before = time.time()
        self.clear_screen()
        self.add(self.clock_button)
        self.show_all()

    def update_ip(self):
        self.eth_ip = alarm_time.get_ip_address('ethernet')
        self.wifi_ip = alarm_time.get_ip_address('wifi')
        self.eth_label.set_markup('<span color=' + self.clock_color + ' font="20">Ethernet: ' + self.eth_ip + '</span>')
        self.wifi_label.set_markup('<span color=' + self.clock_color + ' font="20">Wifi: ' + self.wifi_ip + '</span>')
        return True

    def show_system_screen(self, widget=None):
        self.press_before = time.time()
        self.clear_screen()
        self.add(self.system_vbox)
        self.show_all()

    def markup_text_color(self, text, color=None):
        if color:
            pass
        else:
            color = self.text_color
        return '<span color=' + color + '>' + text + '</span>'
    
    def show_menu_screen(self, widget=None):
        self.press_before = time.time()
        self.clear_screen()
        self.add(self.menu_vbox)
        self.show_all()

    def menu_cancel(self, widget=None):
        self.press_before = time.time()
        self.show_main_screen()

    def clear_screen(self,widget=None):
        for child in self.get_children():
            self.remove(child)
    
    def show_main_screen(self,widget=None):
        self.press_before = time.time()
        self.clear_screen()
        self.add(self.main_screen_vbox)
        self.show_all()
    
    def update_clock(self):
        self.clock_label.set_markup('<span color=' + self.clock_color + '>' + time.strftime('%H:%M:%S') + '</span>')
        self.date_label.set_markup('<span color=' + self.text_color + '>' + time.strftime('%A %d/%m/%Y') + '</span>')
        return True
    
    def update_alarm(self):
        a_time = alarm_time.alarm_time(self.output,self.line2)
        self.output = a_time[0]
        self.line2 = a_time[1]
        self.alarm_label.set_markup('<span color=' + self.text_color + '>' + self.line2 +'</span>')
        if self.line2.split(' ')[1] == 'off':
            self.alarm_bool = False
        else:
            self.alarm_bool = True
        return True
        
    def update_alarm_button(self):
        if self.alarm_bool:
            self.btn_toggle_alarm.set_label('<span color=' + self.clock_color + ' font="15">' + 'Alarm Off</span>')
        else:
            self.btn_toggle_alarm.set_label('<span color=' + self.clock_color + ' font="15">' + 'Alarm On</span>')
        self.btn_toggle_alarm.child.set_use_markup(True)
        return True
    
    def plug_on(self, widget=None):
        self.press_before = time.time()
        subprocess.Popen("/usr/local/bin/plug_on.sh")
    
    def plug_off(self, widget=None):
        self.press_before = time.time()
        subprocess.Popen("/usr/local/bin/plug_off.sh")
    
    def toggle_alarm(self, widget=None):
        self.press_before = time.time()
        alarm_time.toggle_alarm()
        self.update_alarm()
    
    def on_clicked(self, widget=None):
        self.press_before = time.time()
        if self.shown:
             self.remove(self.vbox)
             self.add(self.fix2)
             self.show_all()
        else:
            self.remove(self.fix2)
            self.add(self.vbox)
            self.show_all()
        self.shown = not(self.shown)

    def set_alarm_screen(self,widget=None):
        self.press_before = time.time()
        self.clear_screen()
        self.add(self.vbox_set_alarm_window)
        self.show_all()
    
    def cancel_set_alarm(self, widget=None):
        self.press_before = time.time()
        self.clear_screen()
        self.show_main_screen()
        self.alarm_hour_setting = 7
        self.alarm_minute_setting = 0
        self.update_alarm_set_screen()
    
    def change_alarm_screen(self, widget=None):
        self.press_before = time.time()
        if widget == self.add_hour_btn:
            self.alarm_hour_setting += 1
        elif widget == self.subtract_hour_btn:
            self.alarm_hour_setting -= 1
        elif widget == self.add_minute_btn:
            self.alarm_minute_setting += 5
        elif widget == self.subtract_minute_btn:
            self.alarm_minute_setting -= 5
        self.alarm_hour_setting = self.alarm_hour_setting % 24
        self.alarm_minute_setting %= 60
        self.update_alarm_set_screen()
    
    def update_alarm_set_screen(self):
        self.alarm_minute.set_markup('<span color=' + self.text_color + '>' + alarm_time.add_zero(self.alarm_minute_setting) + '</span>')
        self.alarm_hour.set_markup('<span color=' + self.text_color + '>' + alarm_time.add_zero(self.alarm_hour_setting) + '</span>')
    
    def set_alarm(self, widget=None):
        self.press_before = time.time()
        alarm_time.set_alarm(int(self.alarm_hour_setting), int(self.alarm_minute_setting), True)
        self.update_alarm()
        self.update_alarm_button()
        self.cancel_set_alarm()

clock = PyApp()
gtk.timeout_add(200, clock.update_clock)
gtk.timeout_add(1000, clock.update_alarm)
gtk.timeout_add(1000, clock.update_alarm_button)
gtk.timeout_add(5000, clock.update_ip)
#gtk.timeout_add(200, clock.update_analog_clock)
gtk.timeout_add(10000, clock.screensaver)
gtk.timeout_add(1000, clock.update_music_screen)
gtk.main()
