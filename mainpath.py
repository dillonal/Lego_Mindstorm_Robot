#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C  #  we're importing the motor function
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM #  we're importing other functions related to speed
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.display import Display
from time import sleep
import os
import sys
import time
import math
from math import acos, cos, sin
from textwrap import wrap

lmR = LargeMotor('outA')
lmL = LargeMotor('outB')
lift = MediumMotor('outC')
tank_pair = MoveTank(OUTPUT_A,OUTPUT_B)
steer_pair = MoveSteering(OUTPUT_B,OUTPUT_A)

cs = ColorSensor()
us = UltrasonicSensor()

gy = GyroSensor()
gy.MODE_GYRO_ANG

sound = Sound()

lcd = Display()

# 1.4 rotations == 12 inches
# 0.116667 rotations == 1 inch
#sound.play_tone(1500, 1)

const_speed = 25
move_direction_counter = 0
move_direction_counter_plus_minus = 0
xCord = 6
yCord = -6
barcode_counter = 0

def show_text(string, font_name='courB24', font_width=15, font_height=24):
    lcd.clear()
    strings = wrap(string, width=int(180/font_width))
    for i in range(len(strings)):
        x_val = 89-font_width/2*len(strings[i])
        y_val = 63-(font_height+1)*(len(strings)/2-i)
        lcd.text_pixels(strings[i], False, x_val, y_val, font=font_name)
    lcd.update()


def move_bot(distance, direction): #distance in inches; true for direction = forward, flase for direction = backward

    global xCord
    global yCord
    global move_direction_counter
    global move_direction_counter_plus_minus

    wheel_rotations = distance * 0.116667

    if (direction == "forward"):
        move_direction_counter_plus_minus = 1
        tank_pair.on_for_rotations(const_speed,const_speed,wheel_rotations)

    if (direction == "reverse"):
        move_direction_counter_plus_minus = 0
        tank_pair.on_for_rotations(-(const_speed),-(const_speed),wheel_rotations)

    if (move_direction_counter_plus_minus == 1 and (move_direction_counter % 2 == 0 )):      
        yCord = yCord + distance                                                              
    elif (move_direction_counter_plus_minus == 0 and (move_direction_counter % 2 == 0 )):      
        yCord = yCord - distance                                                             
    elif (move_direction_counter_plus_minus == 1 and (move_direction_counter % 2 != 0)):      
        xCord = xCord + distance                                                             
    else:                                                                                     
        xCord = xCord - distance                                                            

    my_text = 'X CORD: ' + str(xCord)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)
    my_text = 'Y CORD: ' + str(yCord)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)

    sleep(2)

def turn_bot(direction):
    global move_direction_counter
    move_direction_counter = move_direction_counter + 1
    if (direction == "right"):
        steer_pair.on_for_degrees(100,30,162)
    elif (direction == "left"):
        steer_pair.on_for_degrees(-100,30,165)

    sleep(2)


def lift_fork(direction):
    if (direction == "up"):
        lift.on_for_seconds(speed = 10, seconds = 1.1)
    if (direction == "down"):
        lift.on_for_seconds(speed = -10, seconds = 1.1)

    sleep(2)


def barcode_scan():                                         # true - Black; false - Not Black        Pattern: Black White Black White   #can read correct color from 22 mm or closer
    pattern = [1,6,1,6]             
    readings = [0,0,0,0]
    global barcode_counter
    global xCord
    global yCord
    loop_counter = 0

    tank_pair.on(5,5)

    while ((readings != pattern) and (loop_counter < 26)):
        loop_counter = loop_counter + 1
        color = cs.color
        print(str(color))
        sleep(0.51)
        if (color == 1 and pattern != readings):                                                    # change to match correct barcode index 1
            readings[0] = 1
            while (readings[0] == pattern[0]):
                loop_counter = loop_counter + 1
                color = cs.color
                print(str(color))
                sleep(0.51)
                if (color != 1 and color != 0 and pattern != readings):                                            # change to match correct barcode index 2
                    readings[1] = 6
                    while (readings[1] == pattern[1]):
                        loop_counter = loop_counter + 1
                        color = cs.color
                        print(str(color))
                        sleep(0.51)
                        if (color == 1 and pattern != readings):                                    # change to match correct barcode index 3
                            readings[2] = 1
                            while (readings[2] == pattern[2]):
                                loop_counter = loop_counter + 1
                                color = cs.color
                                print(str(color))
                                sleep(0.51)
                                if (color != 1 and color != 0):                            # change to match correct barcode index 4
                                    readings[3] = 6
                                    tank_pair.off(brake=True)
                                    sound.speak("Barcode Matched")
                                    lmL.on_for_rotations(-10,0.23)
                                    lmR.on_for_rotations(-10,0.25)
                                    turn_bot("left")
                                    tank_pair.on_for_rotations(10,10,0.3)
                                    lift_fork("up")
                                    tank_pair.on_for_rotations(-10,-10,0.4)
                                    turn_bot("right")
                                    break


                                else:
                                    readings[0] = 0
                                    readings[1] = 0
                                    readings[2] = 0
                                    readings[3] = 0
                                    break

                        elif (readings == pattern):
                            break

                        else:
                            readings[0] = 0
                            readings[1] = 0
                            readings[2] = 0
                            readings[3] = 0
                            break

                elif (readings == pattern):
                    break

                else:
                    readings[0] = 0
                    readings[1] = 0
                    readings[2] = 0
                    readings[3] = 0
                    break

    tank_pair.off(brake=True)
    if (barcode_counter % 2 == 0 and readings != pattern):
        xCord = xCord + 48
    elif (barcode_counter % 2 != 0 and readings != pattern):
        xCord = xCord - 48

    my_text = 'X CORD: ' + str(xCord)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)
    my_text = 'Y CORD: ' + str(yCord)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)
    
    barcode_counter = barcode_counter + 1


def iGPS():
    radialDistanceA = float(input("Radial Distance from A: "))
    radialDistanceC = float(input("Radial Distance from C: "))
    radialDistanceD = float(input("Radial Distance from D: "))

    b = 126

    sound.speak("Click")

    my_text = 'Radial Distance A: ' + str(radialDistanceA)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)
    my_text = 'Radial Distance C: ' + str(radialDistanceC)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)
    my_text = 'Radial Distance D: ' + str(radialDistanceD)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)

    d = ((radialDistanceA * radialDistanceA) + ( b * b) - (radialDistanceC * radialDistanceC)) / (2 * radialDistanceA * b)
    C = acos(d)
    iGPSxCord = radialDistanceA * sin(C) - 6
    iGPSyCord = radialDistanceA * cos(C) + 6

    my_text = 'X Cordinate: ' + str(iGPSxCord)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)
    my_text = 'Y Cordinate: ' + str(iGPSyCord)
    show_text(my_text, 'courB14', 9, 14)
    sleep(2)


def Collision_Avoidance():
    tank_pair.on(25,25)
    distance = us.distance_centimeters_continuous
    while distance > 40:
        distance = us.distance_centimeters_continuous

def main():
    #Input functions needed to complete the task at hand
    
if __name__ == "__main__":
    main()

#brickrun -r ./Python_ev3_codes/mainpath.py
