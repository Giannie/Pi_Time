#!/usr/bin/python

from PIL import Image, ImageDraw
import math
import datetime

height = 240
width = 320
size = (width, height)

def minute_angle(minute):
    return math.pi * minute / 30.0

def hour_angle(hour,minute):
    return (hour + minute/60.0) * math.pi / 6

def second_start(second):
    y = y = height/2 - height/16 * math.cos(minute_angle(second))
    x = width/2 + height/16 * math.sin(minute_angle(second))
    return (int(round(x,0)), int(round(y,0)))

def minute_start(minute):
    y = height/2 - height/8 * math.cos(minute_angle(minute))
    x = width/2 + height/8 * math.sin(minute_angle(minute))
    return (int(round(x,0)), int(round(y,0)))

def minute_end(minute):
    y = height/2 - height/2 * math.cos(minute_angle(minute))
    x = width/2 + height/2 * math.sin(minute_angle(minute))
    return (int(round(x,0)), int(round(y,0)))

def hour_start(hour, minute):
    y = height/2 - height/4 * math.cos(hour_angle(hour, minute))
    x = width/2 + height/4 * math.sin(hour_angle(hour, minute))
    return (int(round(x,0)), int(round(y,0)))

def hour_end(hour, minute):
    y = height/2 - height/2 * math.cos(hour_angle(hour, minute))
    x = width/2 + height/2 * math.sin(hour_angle(hour, minute))
    return (int(round(x,0)), int(round(y,0)))
    
def draw_now(location):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    im = Image.new('RGB', size)
    draw = ImageDraw.Draw(im)

    draw.line([minute_start(minute), minute_end(minute)], fill="#3A1465", width=3)
    draw.line([hour_start(hour, minute), hour_end(hour, minute)], fill="#3A1465", width=3)
    draw.line([second_start(second),minute_end(second)], fill="grey")

    del draw
    im.save(location + '/clock.png','PNG')

if __name__ == "__main__":
    for hour in range(12):
        for minute in range(60):
            im = Image.new('RGB', size)

            draw = ImageDraw.Draw(im)

            draw.line([minute_start(minute), minute_end(minute)], fill="#3A1465", width=3)
            draw.line([hour_start(hour, minute), hour_end(hour, minute)], fill="#3A1465", width=3)

            del draw

            im.save(str(hour) + '-' + str(minute) + '.png', 'PNG')