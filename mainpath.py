#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C  #  we're importing the motor function
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

lmR = LargeMotor('outA')
lmL = LargeMotor('outB')
lift = MediumMotor('outC')
tank_pair = MoveTank(OUTPUT_A,OUTPUT_B)

cs = ColorSensor()

gy = GyroSensor()
gy.MODE_GYRO_ANG

sound = Sound()

# 1.435 rotations == 12 inches
# 0.119583 rotations == 1 inch

const_speed = 25
move_direction_counter = 0                                          #new
move_direction_counter_plus_minus = 0                               #new
xCord = 0                                                           #new
yCord = 0                                                           #new


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def move_bot(distance, direction): #distance in inches; true for direction = forward, flase for direction = backward

    global xCord
    global yCord
    global move_direction_counter
    global move_direction_counter_plus_minus

    wheel_rotations = distance * 0.119583

    if (direction == "forward"):
        move_direction_counter_plus_minus = 1
        tank_pair.on_for_rotations(const_speed,const_speed,wheel_rotations)

    if (direction == "reverse"):
        move_direction_counter_plus_minus = 0
        tank_pair.on_for_rotations(-(const_speed),-(const_speed),wheel_rotations)

    if (move_direction_counter_plus_minus == 1 and (move_direction_counter % 2 == 0 )):        #new
        yCord = yCord + distance                                                              #new
        sound.play_tone(1500, 1)
    elif (move_direction_counter_plus_minus == 0 and (move_direction_counter % 2 == 0 )):      #new
        yCord = yCord - distance                                                              #new
        sound.play_tone(1500, 1)
    elif (move_direction_counter_plus_minus == 1 and (move_direction_counter % 2 != 0)):       #new
        xCord = xCord + distance                                                              #new
        sound.play_tone(1500, 1)
    else:                                                                                      #new
        xCord = xCord - distance                                                              #new
        sound.play_tone(1500, 1)

    print('X CORD: ', str(xCord), '  ', ' Y CORD: ', str(yCord)) 
    #print("Hello")

    sleep(2)

def turn_bot(direction):
    global move_direction_counter
    move_direction_counter = move_direction_counter + 1 #new
    if (direction == "right"):
        gy.MODE_GYRO_RATE
        gy.MODE_TILT_ANG
        angle = gy.angle
        tempangle = gy.angle
        while (abs(angle - tempangle) < 87):
            tank_pair.on_for_seconds(-10,10,0.05)
            angle = gy.angle
    elif (direction == "left"):
        gy.MODE_GYRO_RATE
        gy.MODE_TILT_ANG
        angle = gy.angle
        tempangle = gy.angle
        while (abs(angle - tempangle) < 87):
            tank_pair.on_for_seconds(10,-10,0.05)
            angle = gy.angle

    sleep(2)


def lift_fork(direction):
    if (direction == "up"):
        lift.on_for_seconds(speed = 10, seconds = 2.5)
    if (direction == "down"):
        lift.on_for_seconds(speed = -10, seconds = 2.5)

    sleep(2)


def barcode_scan():                                         # 0 - No color; 1 - Black; 6 - White         Pattern: Black White Black White   #can read correct color from 22 mm or closer
    pattern = [1,6,1,6]
    readings = [0,0,0,0]
    
    sound.speak("Loop Starting")

    while (readings != pattern):
        sound.speak("At the beginning")
        sleep(0.5)
        color = cs.color
        if (color == 1):                                                    # change to match correct barcode index 1
            readings[0] = color
            sound.speak("Index 1 correct")
            sound.speak(str(readings[0]))
            while (readings[0] == pattern[0]):
                sleep(0.5)
                color = cs.color
                if (color == 6):                                            # change to match correct barcode index 2
                    readings[1] = color
                    sound.speak("Index 2 correct")
                    sound.speak(str(readings[1]))
                    while (readings[1] == pattern[1]):
                        sleep(0.5)
                        color = cs.color
                        if (color == 1):                                    # change to match correct barcode index 3
                            readings[2] = color
                            sound.speak("Index 3 correct")
                            sound.speak(str(readings[2]))
                            while (readings[2] == pattern[2]):
                                sleep(0.5)
                                color = cs.color
                                if (color == 6):                            # change to match correct barcode index 4
                                    readings[3] = color
                                    sound.speak("Index 4 correct")
                                    sound.speak(str(readings[3]))
                                    sound.speak("This is the barcode in order")
                                    sound.speak("Index 1")
                                    sound.speak(str(readings[0]))
                                    sound.speak("Index 2")
                                    sound.speak(str(readings[1]))
                                    sound.speak("Index 3")
                                    sound.speak(str(readings[2]))
                                    sound.speak("Index 4")
                                    sound.speak(str(readings[3]))
                                    sound.speak("Barcode Matched")
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

    sound.speak("Completed")


def test():
    tank_pair.on_for_rotations(1,1,1)



def main():

    #move_bot(24,"forward")
    #turn_bot("right")
    #move_bot(12,"reverse")
    #lift_fork("up")
    #sleep(60)

    barcode_scan()

    #test()

if __name__ == "__main__":
    main()

