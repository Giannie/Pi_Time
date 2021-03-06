#!/usr/bin/python

try:
    from PIL import Image, ImageDraw
except:
    pass
import math
import datetime

# height = 222
# width = 302
# area_height = 232
# area_width = 312
# size = (width, height)

def minute_angle(minute):
    return math.pi * minute / 30.0

def hour_angle(hour,minute):
    return (hour + minute/60.0) * math.pi / 6

def second_start(second, size):
    area_width = size[0] - 8
    area_height = size[1] - 8
    width = size[0] - 18
    height = size[1] - 18
    y = area_height/2 - height/16 * math.cos(minute_angle(second))
    x = area_width/2 + height/16 * math.sin(minute_angle(second))
    return int(round(x,0)), int(round(y,0))

def second_center(time, size):
    area_width = size[0] - 8
    area_height = size[1] - 8
    width = size[0] - 18
    height = size[1] - 18
    second_now = time.second
    length = height/2 - 4
    y = area_height/2 - length * math.cos(minute_angle(second_now))
    x = area_width/2 + length * math.sin(minute_angle(second_now))
    x -= 4
    y -= 4
    return int(round(x, 0)), int(round(y, 0))

def minute_start(minute, size):
    area_width = size[0] - 8
    area_height = size[1] - 8
    width = size[0] - 18
    height = size[1] -18
    y = area_height/2 - height/8 * math.cos(minute_angle(minute))
    x = area_width/2 + height/8 * math.sin(minute_angle(minute))
    return int(round(x, 0)), int(round(y, 0))

def minute_end(minute, size):
    area_width = size[0] - 8
    area_height = size[1] - 8
    width = size[0] - 18
    height = size[1] - 18
    y = area_height/2 - height/2 * math.cos(minute_angle(minute))
    x = area_width/2 + height/2 * math.sin(minute_angle(minute))
    return (int(round(x,0)), int(round(y,0)))

def hour_start(hour, minute, size):
    area_width = size[0] - 8
    area_height = size[1] - 8
    width = size[0] - 18
    height = size[1] - 18
    y = area_height/2 - height/4 * math.cos(hour_angle(hour, minute))
    x = area_width/2 + height/4 * math.sin(hour_angle(hour, minute))
    return (int(round(x,0)), int(round(y,0)))

def hour_end(hour, minute, size):
    area_width = size[0] - 8
    area_height = size[1] - 8
    width = size[0] - 18
    height = size[1] - 18
    y = area_height/2 - height/2 * math.cos(hour_angle(hour, minute))
    x = area_width/2 + height/2 * math.sin(hour_angle(hour, minute))
    return (int(round(x,0)), int(round(y,0)))
    
def draw_now(location):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    im = Image.new('RGB', size)
    draw = ImageDraw.Draw(im)

    draw.line([minute_start(minute), minute_end(minute)], fill="#3A1465", width=3)
    draw.line([hour_start(hour, minute), hour_end(hour, minute)], fill="#3A1465", width=3)
    #draw.line([second_start(second),minute_end(second)], fill="grey")
    draw.ellipse(bounding_box(second), fill="grey")

    del draw
    im.save(location + '/clock.png','PNG')

def draw_clock_button(location, time, counter):
    hour = time.hour
    minute = time.minute
    second = time.second

    im = Image.new('RGB', size)
    draw = ImageDraw.Draw(im)

    draw.line([minute_start(minute), minute_end(minute)], fill="#3A1465", width=3)
    draw.line([hour_start(hour, minute), hour_end(hour, minute)], fill="#3A1465", width=3)
    #draw.line([second_start(second),minute_end(second)], fill="grey")
    draw.ellipse(bounding_box(second), fill="grey")

    del draw
    im.save(location + '/clock.png','PNG')

def bounding_box(second):
    top = minute_end(second)
    if top[1] < height/2:
        return (top[0] - 3, top[1], top[0] + 3, top[1] + 6)
    else:
        return (top[0] - 3, top[1] - 6, top[0] + 3, top[1])


if __name__ == "__main__":
    for hour in range(12):
        for minute in range(60):
            for second in range(60):
                im = Image.new('RGB', size)

                draw = ImageDraw.Draw(im)

                draw.line([minute_start(minute), minute_end(minute)], fill="#3A1465", width=3)
                draw.line([hour_start(hour, minute), hour_end(hour, minute)], fill="#3A1465", width=3)
                draw.ellipse(bounding_box(second), fill="grey")

                del draw

                im.save(str(hour) + '-' + str(minute) + '-' + str(second) + '.png', 'PNG')