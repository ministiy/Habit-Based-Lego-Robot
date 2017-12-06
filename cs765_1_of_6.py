#!/usr/bin/env python3
from ev3dev.ev3 import *
from math import sin,cos
from time import sleep,time
import csv

Sound.beep()

MAX_SENSOR = 100.0 # percent
MAX_MOTOR = 1000.0

BIAS = 0.05
SENSOR_GAIN = 1.0
OUTPUT_GAIN = 1.0

Leds.set_color(Leds.LEFT, Leds.YELLOW)
Leds.set_color(Leds.RIGHT, Leds.YELLOW)

lm = LargeMotor('outB')
rm = LargeMotor('outC')
lm.reset()
rm.reset()
b = Button()

ls = ColorSensor('in2')
#assert ls.connected, "Left sensor not connected to port 2"
rs = ColorSensor('in3')
#assert rs.connected, "Right sensor not connected to port 3"
ls.mode='COL-AMBIENT'
rs.mode='COL-AMBIENT'

lu = UltrasonicSensor('in1')
lu.mode='US-DIST-CM'
ru = UltrasonicSensor('in4')
ru.mode='US-DIST-CM'

def cleanup() :
    print('cleaning up...')
    lm.stop()
    rm.stop()
    print('quiting')
    exit()


btn = Button()
# Do something when state of any button changes:
def right(state):  # neater use of 'if' follows:
    global SENSOR_GAIN
    if state :
        SENSOR_GAIN += 0.05
        print('SENSOR_GAIN:',SENSOR_GAIN)

def left(state):
    global SENSOR_GAIN
    if state :
        SENSOR_GAIN -= 0.01
        print('SENSOR_GAIN:',SENSOR_GAIN)

def up(state):
    global OUTPUT_GAIN
    if state :
        OUTPUT_GAIN += 0.5
        print('OUTPUT_GAIN:',OUTPUT_GAIN)

def down(state):
    global OUTPUT_GAIN
    if state :
        OUTPUT_GAIN -= 0.1
        print('OUTPUT_GAIN:',OUTPUT_GAIN)

def enter(state):
    print('Enter button pressed' if state else 'Enter button released')

def backspace(state):
    print('Backspace button pressed' if state else 'Backspace button released')
    cleanup()

btn.on_left = left
btn.on_right = right
btn.on_up = up
btn.on_down = down
btn.on_enter = enter
btn.on_backspace = backspace

target_ips = 0.1
start_time = time()

it = 0

header = ['left sensor','right sensor' , 'left ultraviolet sensor' , 'right ultraviolet sensor' , 'left motor', 'right motor']
with open('output.csv', 'w', newline="") as output_file:
        wr = csv.writer(output_file,delimiter = ',' , quoting = csv.QUOTE_ALL)
        wr.writerow(header)
while True :
    it += 1
    t = target_ips*it

    ## normalized to lie between 0 and 1 (1 close, 0 far)
    lsv = SENSOR_GAIN*float(ls.value())/MAX_SENSOR
    rsv = SENSOR_GAIN*float(rs.value())/MAX_SENSOR

    luv = 1.0-max(0.0,min(1.0,float(lu.value())/200.0))
    ruv = 1.0-max(0.0,min(1.0,float(ru.value())/200.0))
    
    Leds.set(Leds.LEFT, brightness_pct=lsv)
    Leds.set(Leds.RIGHT, brightness_pct=rsv)

    # if max(lsv,rsv) < 0.1 :
    #     SENSOR_GAIN *=1.05
    #     print('SENSOR_GAIN increased to : %f' %(SENSOR_GAIN))
    # elif min(lsv,rsv) > 0.5 :
    #     SENSOR_GAIN *=0.95
    #     print('SENSOR_GAIN decreased to : %f' %(SENSOR_GAIN))

    # ## LOVE + AGGR
    # lmv = BIAS + (rsv-0.2*lsv)
    # rmv = BIAS + (lsv-0.2*rsv)

    ## AGGR
    lmv = BIAS + rsv - 0.0*lsv - (ruv*2.)
    rmv = BIAS + lsv - 0.0*rsv - (luv*2.)

    lmv *= OUTPUT_GAIN
    rmv *= OUTPUT_GAIN

    if max(lmv,rmv) > MAX_MOTOR :
        lmv -= max_mv - MAX_MOTOR
        rmv -= max_mv - MAX_MOTOR
        # OUTPUT_GAIN *= 0.95
        # print('OUTPUT_GAIN decreased to : %f' %(OUTPUT_GAIN))

    # if min(lmv,rmv) < 0.05 :
    #     OUTPUT_GAIN *= 1.05
    #     print('OUTPUT_GAIN increased to : %f' %(OUTPUT_GAIN))

        
    if (it % 10) == 0 :
        print('ls: %0.3f rs:%0.3f lm: %0.3f rm:%0.3f' %(lsv,rsv,lmv,rmv))

    lmv = int(max(-1000,min(1000,MAX_MOTOR * lmv)))
    rmv = int(max(-1000,min(1000,MAX_MOTOR * rmv)))

    lm.run_forever(speed_sp = lmv)
    rm.run_forever(speed_sp = rmv)

    
    # writing to a csv file called output.csv to store sensory-motor data where
    #   lsv = left colour sensor value
    #   rsv = right colour sensor value
    #   luv = left ultraviolet sensor value
    #   ruv = right ultraviolet sensor value
    #   lmv = left motor value
    #   rmv = right motor value
    with open('output.csv', 'a', newline="") as output_file:
        wr = csv.writer(output_file, delimiter = ',' , quoting=csv.QUOTE_ALL)
        wr.writerow([lsv, rsv, luv, ruv, lmv, rmv])

    btn.process() # Check for currently pressed buttons.

    it_duration = time()-start_time
    sleep_duration = max(0.0,target_ips-it_duration)
    sleep(sleep_duration)
    if (it %50 == 0) :
        print('it dur: %f  (slept for %f)' %(time()-start_time,sleep_duration))
        
    start_time = time()
