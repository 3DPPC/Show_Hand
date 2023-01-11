import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import mss
from PIL import Image
import threading
from pynput.keyboard import Key, Controller
import board
import pwmio
from adafruit_motor import Servo
import digitalio

keyboard = Controller()
GREEN_KEY = 'a'
RED_KEY = 's'
YELLOW_KEY = 'd'
BLUE_KEY = 'j'
ORANGE_KEY = 'k'

def servo_duty_cycle(pulse_ms, frequency=50):
    period_ms = 1.0 / frequency * 1000.0
    duty_cycle = int(pulse_ms / (period_ms / 65535.0))
    return duty_cycle

pinky_led = digitalio.DigitalInOut(board.GP1)
ring_led = digitalio.DigitalInOut(board.GP2)
middle_led = digitalio.DigitalInOut(board.GP3)
index_led = digitalio.DigitalInOut(board.GP4)
thumb_led = digitalio.DigitalInOut(board.GP5)

def light_led(light_name):
    light_name.direction = digitalio.Direction.OUTPUT
    light_name.value = True
    time.sleep(0.5)
    light_name.value = False

pwm_pinky = pwmio.PWMOut(board.D5, duty_cycle=servo_duty_cycle(1.0), frequency=50)
pwm_ring = pwmio.PWMOut(board.D6, duty_cycle=servo_duty_cycle(1.0), frequency=50)
pwm_middle = pwmio.PWMOut(board.D7, duty_cycle=servo_duty_cycle(1.0), frequency=50)
pwm_index = pwmio.PWMOut(board.D8, duty_cycle=servo_duty_cycle(1.0), frequency=50)
pwm_thumb_rotate = pwmio.PWMOut(board.D9, duty_cycle=servo_duty_cycle(1.0), frequency=50)
pwm_thumb_flex = pwmio.PWMOut(board.D10, duty_cycle=servo_duty_cycle(1.0), frequency=50)

pinky = pinky.Servo(pwm_pinky)
ring = ring.Servo(pwm_ring)
middle = middle.Servo(pwm_middle)
index = index.Servo(pwm_index)
thumb_rotate = thumb_rotate.Servo(pwm_thumb_rotate)
thumb_flex = thumb_flex.Servo(pwm_thumb_flex)

def startup_led():
    '#add stuff here'

def button_press(finger, angle):
    '#set given finger to given angle'
    finger.angle = angle
    '#light fingers led'
    if finger == "pinky":
        light_led(pinky_led)
        # light green
        print("green")
        time.sleep(0.1)
    elif finger == "ring":
        # light red
        light_led(ring_led)
        print("red")
        time.sleep(0.1)
            
    elif finger == "middle":
        # light yellow
        light_led(middle_led)
        print("yellow")
        time.sleep(0.1)
    elif finger == "index":
        # light blue
        light_led(index_led)
        print("blue")
        time.sleep(0.1)
    elif finger == "thumb":
        # light orange
        light_led(thumb_led)
        print("orange")
        time.sleep(0.1)

def guitarBot():
    green_pressed = False
    red_pressed = False
    yellow_pressed = False
    blue_pressed = False
    orange_pressed = False
    
    with mss.mss() as sct:
        monitor = {"top": 575, "left": 520, "width": 375, "height": 30}
        meter = {"top": 490, "left": 915, "width": 20, "height": 20}
    while (1):
        img = np.array(sct.grab(monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        lower_green = np.array([45, 75, 100])
        upper_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_mask[0:60, 125:750] = 0
        
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([5, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        red_mask[0:60, 125:750] = 0
        
        lower_yellow = np.array([26, 75, 100])
        upper_yellow = np.array([40, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellow_mask[0:60, 125:750] = 0
        
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_mask[0:60, 125:750] = 0
        
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([12, 255, 255])
        orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
        orange_mask[0:60, 125:750] = 0
        
        mask = green_mask + red_mask + yellow_mask + blue_mask + orange_mask
        res = cv2.bitwise_and(img, img, mask=mask)
        
        for g in green_mask: 
            if g.any() != 0 and not green_pressed:
                keyboard.press(GREEN_KEY)
                green_pressed = True
                button_press(pinky, 30)
                break
        else:
            keyboard.release(GREEN_KEY)
            green_pressed = False
                
        for r in red_mask: 
            if r.any() != 0 and not red_pressed:
                keyboard.press(RED_KEY)
                red_pressed = True
                button_press(ring, 30)
                break
        else:
            keyboard.release(RED_KEY)
            red_pressed = False
                
        for y in yellow_mask: 
            if y.any() != 0 and not yellow_pressed:
                keyboard.press(YELLOW_KEY)
                yellow_pressed = True
                button_press(middle, 30)
                break
        else:
            keyboard.release(YELLOW_KEY)
            yellow_pressed = False
                
        for o in orange_mask: 
            if o.any() != 0 and not orange_pressed:
                keyboard.press(ORANGE_KEY)
                orange_pressed = True
                button_press(thumb_rotate, 30)
                break
        else:
            keyboard.release(ORANGE_KEY)
            orange_pressed = False
                
        for b in blue_mask: 
            if b.any() != 0 and not blue_pressed:
                keyboard.press(BLUE_KEY)
                blue_pressed = True
                button_press(index, 30)
                break
        else:
            keyboard.release(BLUE_KEY)
            blue_pressed = False
                
        cv2.imshow('masked', res)
        cv2.imshow('screen', img)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
if _name_ == '_main_':
    guitarBot()
