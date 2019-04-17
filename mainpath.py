#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C  #we're importing the motor function
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM #we're importing other functions related to speed
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.display import Display
from time import sleep
import os
import sys
import time

lmR = LargeMotor('outA')
lmL = LargeMotor('outB')
lift = MediumMotor('outC')
tank_pair = MoveTank(OUTPUT_A,OUTPUT_B)

gy = GyroSensor()
gy.MODE_GYRO_ANG

sound = Sound()

# 1.435 rotations == 12 inches
# 0.119583 rotations == 1 inch

const_speed = 25


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

def move_bot(distance, direction): #distance in inches; true for direction = forward, flase for direction = backwards

    wheel_rotations = distance * 0.119583

    if (direction == "forward"):
        tank_pair.on_for_rotations(const_speed,const_speed,wheel_rotations)
    if (direction == "reverse"):
        tank_pair.on_for_rotations(-(const_speed),-(const_speed),wheel_rotations)
        

def turn_bot(direction):
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


def lift_fork(direction):
    if (direction == "up"):
        lift.on_for_seconds(speed = 10, seconds = 2.3)
    if (direction == "down"):
        lift.on_for_seconds(speed = -10, seconds = 2.3)

move_bot(24,"forward")
turn_bot("right")
move_bot(12,"reverse")
lift_fork("up")

