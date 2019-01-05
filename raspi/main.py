#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

from api import image_processing
from config import ROBOT_CONFIG


DEFAULT_PWM_VALUE = 70
RIGHT_LEFT_MULTIPLIER = 0.5
FORWARD_BACKWARD_MULTIPLIER = 0.5

# Left
in1 = 11
# in1 = 17
in2 = 13
# in2 = 27
# Right
in3 = 12
# in3 = 18
in4 = 16
# in4 = 23
# Pwn
en = 32
# en = 12

# Kaldirac pinno
holder_pinno = 18


GPIO.setmode(GPIO.BOARD)
# GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(holder_pinno, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

p = GPIO.PWM(en, 1000)
p.start(DEFAULT_PWM_VALUE)

p_holder = GPIO.PWM(holder_pinno, 50)
p_holder.start(0)


def stand_up():
    p_holder.ChangeDutyCycle(12.5)
    time.sleep(0.2)
    p_holder.stop()


def stand_down():
    p_holder.ChangeDutyCycle(2.5)
    time.sleep(0.2)
    p_holder.stop()


def forward(duration):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(duration)
    clean_up()


def backward(duration):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    time.sleep(duration)
    clean_up()


def turn_90_degree_right():
    turn_right(0.6)


def turn_45_degree_right():
    turn_right(0.33)


def turn_right(duration):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    time.sleep(duration)
    clean_up()


def turn_left(duration):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(duration)
    clean_up()


def clean_up():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def algo():

    # Raspi
    IMAGE_PATH = "cikti.jpeg"
    # IMAGE_PATH = "pictures/blue.jpeg"
    # Resim cek kaydet, sonra api'ye istek at.
    BOX_IN_SIGHT = False
    BOX_IN_HAND = False
    ZONE_IN_SIGHT = False
    COLOR_IN_HAND = ""
    FLAGS = {"red": False, "blue": False, "green": False}

    while True:
        if BOX_IN_HAND:
            if ZONE_IN_SIGHT:
                x, y, _ = image_processing(
                    IMAGE_PATH, COLOR_IN_HAND, FLAGS, "drop_zone"
                )
                if y > 0.6:
                    print("right")
                    turn_right((y - 0.5) * RIGHT_LEFT_MULTIPLIER)
                else:
                    if y < 0.4:

                        print("left")
                        turn_left((0.5 - y) * RIGHT_LEFT_MULTIPLIER)
                    else:
                        if x > 0.95:
                            print("drop")
                            stand_down()
                            backward(0.1)
                            BOX_IN_HAND = False
                            ZONE_IN_SIGHT = False
                            FLAGS[COLOR_IN_HAND] = False
                        else:
                            print("forward")
                            forward((1.0 - x) * FORWARD_BACKWARD_MULTIPLIER)
            else:
                maxX = 0
                rot = 0
                for i in range(8):
                    _x, _y, _ = image_processing(
                        IMAGE_PATH, COLOR_IN_HAND, FLAGS, mode="drop_zone"
                    )
                    turn_45_degree_right()
                    print("right 45")
                    if _x > maxX:
                        maxX = _x
                        rot = i
                for i in range(rot):
                    turn_45_degree_right()
                    print("right 45")

                ZONE_IN_SIGHT = True
        else:
            if BOX_IN_SIGHT:
                print("########## BOX IN SIGHT ############ ")
                x, y, COLOR_IN_HAND = image_processing(
                    IMAGE_PATH, COLOR_IN_HAND, FLAGS, mode="box"
                )
                if y > 0.6:
                    print("right")
                    turn_right((y - 0.5) * RIGHT_LEFT_MULTIPLIER)
                else:
                    if y < 0.4:
                        print("left")
                        turn_left((0.5 - y) * RIGHT_LEFT_MULTIPLIER)
                    else:
                        if x > 0.95:
                            print("hold")
                            forward(0.3)
                            stand_up()
                            BOX_IN_HAND = True
                            BOX_IN_SIGHT = False
                        else:
                            print("forward")
                            forward((1.0 - x) * FORWARD_BACKWARD_MULTIPLIER)

            else:
                maxX = 0
                rot = 0

                for i in range(8):
                    _x, _y, _color = image_processing(
                        IMAGE_PATH, COLOR_IN_HAND, FLAGS, "box"
                    )
                    print(_x, _y, _color)
                    turn_45_degree_right()
                    print("right 45")
                    if _x > maxX:
                        maxX = _x
                        rot = i

                print("############### RETURN ############# ")
                for i in range(rot):
                    turn_45_degree_right()
                    time.sleep(1)
                    print("right 45")

                BOX_IN_SIGHT = True

        print("Finished")

    print("While Finished")


def main():
    try:
        algo()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()

