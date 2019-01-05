import RPi.GPIO as GPIO
import time


DEFAULT_PWM_VALUE = 35

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
temp1 = 1

GPIO.setmode(GPIO.BOARD)
# GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p = GPIO.PWM(en, 1000)

pwn_value = DEFAULT_PWM_VALUE
p.start(pwn_value)


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


print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")


while 1:

    x = input("Input:")

    if x == "s":
        print("stop")
        clean_up()

    elif x == "f":
        print("forward")
        print(pwn_value)
        forward(0.6)

    elif x == "b":
        print("backward")
        print(pwn_value)
        backward(0.6)

    elif x == "r":
        print("right")
        print(pwn_value)
        turn_right(0.6)

    elif x == "l":
        print("left")
        print(pwn_value)
        turn_left(0.6)

    elif x == "low":
        print("low")
        p.ChangeDutyCycle(25)

    elif x == "m":
        print("medium")
        pwn_value = 50
        p.ChangeDutyCycle(pwn_value)

    elif x == "h":
        print("high")
        pwn_value = 75
        p.ChangeDutyCycle(pwn_value)

    elif x == "i":
        print("Increate")
        pwn_value += 10
        print(pwn_value)
        p.ChangeDutyCycle(pwn_value)

    elif x == "d":
        print("Decrease")
        pwn_value -= 10
        print(pwn_value)
        p.ChangeDutyCycle(pwn_value)

    elif x == "e":
        GPIO.cleanup()
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
