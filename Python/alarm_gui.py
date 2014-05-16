#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This is a trivial PyGTK example
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009


import gtk
import time
import pango
from time import sleep
from crontab import CronTab
import alarm_time
import subprocess
import sys


class PyApp(gtk.Window):
    def __init__(self):
        self.clock_color = '"dark blue"'
        self.text_color = "'purple'"
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
        
        self.create_main_screen()
        self.create_set_alarm_screen()
        self.create_menu_screen()
        
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
        self.show_main_screen()
        self.shown = True

    def create_main_screen(self):
        self.clock_label = gtk.Label()
        self.clock_label.modify_font(pango.FontDescription("helvetica 40"))
        self.date_label = gtk.Label()
        self.date_label.modify_font(pango.FontDescription("helvetica 24"))
        self.alarm_label = gtk.Label()
        self.alarm_label.modify_font(pango.FontDescription("helvetica 24"))

        self.update_clock()
        self.update_alarm()
        btn_menu = gtk.Button('<span color=' + self.text_color + 'font="14">Menu</span>')
        btn_menu.child.set_use_markup(True)
        btn_menu.connect("clicked", self.show_menu_screen)
        btn_toggle_alarm = gtk.Button('<span color="purple" font="14">Alarm Off</span>')
        btn_toggle_alarm.child.set_use_markup(True)
        btn_toggle_alarm.connect("clicked", self.toggle_alarm)
        self.btn_toggle_alarm = btn_toggle_alarm
        self.update_alarm_button()
        btn_set_alarm = gtk.Button('<span color="purple" font="14">Set Alarm</span>')
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
        btn_set_alarm_cancel.set_label('<span color="purple" font="15">Cancel</span>')
        btn_set_alarm_cancel.connect("clicked",self.cancel_set_alarm)
        btn_set_alarm_cancel.child.set_use_markup(True)

        btn_set_alarm_screen = gtk.Button()
        btn_set_alarm_screen.set_label('<span color="purple" font="15">Set Alarm</span>')
        btn_set_alarm_screen.connect("clicked",self.set_alarm)
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

        self.vbox_set_alarm_window = gtk.VBox(False,0)
        self.vbox_set_alarm_window.pack_start(self.valign_set_alarm)
#        vbox_set_alarm_buttons = gtk.VBox(False,0)
        valign_set_alarm_buttons = gtk.Alignment(0.5,1,0,0)
        hbox_set_alarm_buttons = gtk.HBox(True,5)
        halign_set_alarm_buttons = gtk.Alignment(0,0,0,0)
        halign_set_alarm_buttons.add(hbox_set_alarm_buttons)
        hbox_set_alarm_buttons.add(btn_set_alarm_screen)
        hbox_set_alarm_buttons.add(btn_set_alarm_cancel)
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

    def create_menu_screen(self):
        system_button = gtk.Button('<span color="purple" font="15">System</span>')
        music_button = gtk.Button('<span color="purple" font="15">Music</span>')
        cancel_button = gtk.Button('<span color="purple" font="15">Cancel</span>')

        system_button.child.set_use_markup(True)
        music_button.child.set_use_markup(True)
        cancel_button.child.set_use_markup(True)

        cancel_button.connect("clicked", self.menu_cancel)

        menu_vbox = gtk.VBox(True, 0)

        menu_vbox.pack_start(system_button)
        menu_vbox.pack_start(music_button)
        menu_vbox.pack_start(cancel_button)

        self.menu_vbox = menu_vbox

    def show_menu_screen(self, widget=None):
        self.clear_screen()
        self.add(self.menu_vbox)
        self.show_all()

    def menu_cancel(self, widget=None):
        self.show_main_screen()


    def clear_screen(self,widget=None):
        for child in self.get_children():
            self.remove(child)
    
    def show_main_screen(self,widget=None):
        self.clear_screen()
        self.add(self.main_screen_vbox)
        self.show_all()
    
    def update_clock(self):
        self.clock_label.set_markup('<span color=' + self.clock_color + '>' + time.strftime('%H:%M:%S') + '</span>')
        self.date_label.set_markup('<span color="purple">' + time.strftime('%A %d/%m/%Y') + '</span>')
        return True
    
    def update_alarm(self):
        a_time = alarm_time.alarm_time(self.output,self.line2)
        self.output = a_time[0]
        self.line2 = a_time[1]
        self.alarm_label.set_markup('<span color="purple">' + self.line2 +'</span>')
        if self.line2.split(' ')[1] == 'off':
            self.alarm_bool = False
        else:
            self.alarm_bool = True
        return True
        
    def update_alarm_button(self):
        if self.alarm_bool:
            self.btn_toggle_alarm.set_label('<span color="purple" font="14">Alarm Off</span>')
        else:
            self.btn_toggle_alarm.set_label('<span color="purple" font="14">Alarm On</span>')
        self.btn_toggle_alarm.child.set_use_markup(True)
        return True
    
    def plug_on(self, widget=None):
        subprocess.Popen("/usr/local/bin/plug_on.sh")
    
    def plug_off(self, widget=None):
        subprocess.Popen("/usr/local/bin/plug_off.sh")
    
    def toggle_alarm(self, widget=None):
        alarm_time.toggle_alarm()
        self.update_alarm()
    
    def on_clicked(self, widget=None):
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
        self.clear_screen()
        self.add(self.vbox_set_alarm_window)
        self.show_all()
    
    def cancel_set_alarm(self, widget=None):
        self.clear_screen()
        self.show_main_screen()
        self.alarm_hour_setting = 7
        self.alarm_minute_setting = 0
        self.update_alarm_set_screen()
    
    def change_alarm_screen(self, widget=None):
        if widget == self.add_hour_btn:
            self.alarm_hour_setting += 1
        elif widget == self.subtract_hour_btn:
            self.alarm_hour_setting -= 1
        elif widget == self.add_minute_btn:
            self.alarm_minute_setting += 5
        elif widget == self.subtract_minute_btn:
            self.alarm_minute_setting -= 5
        self.alarm_hour_setting = self.alarm_hour_setting % 24
        self.alarm_minute_setting = self.alarm_minute_setting % 60
        self.update_alarm_set_screen()
    
    def update_alarm_set_screen(self):
        self.alarm_minute.set_markup('<span color="purple">'+ alarm_time.add_zero(self.alarm_minute_setting) + '</span>')
        self.alarm_hour.set_markup('<span color="purple">'+ alarm_time.add_zero(self.alarm_hour_setting) + '</span>')
    
    def set_alarm(self,widget=None):
        alarm_time.set_alarm(int(self.alarm_hour_setting), int(self.alarm_minute_setting), True)
        self.update_alarm()
        self.update_alarm_button()
        self.cancel_set_alarm()

clock = PyApp()
gtk.timeout_add(200, clock.update_clock)
gtk.timeout_add(1000, clock.update_alarm)
gtk.timeout_add(1000, clock.update_alarm_button)
gtk.main() 