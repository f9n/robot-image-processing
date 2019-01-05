import RPi.GPIO as GPIO
from contextlib import contextmanager
import time


class Whell(object):
    def __init__(self, forward_pinno, backward_pinno):
        self.forward_pinno = forward_pinno
        self.backward_pinno = backward_pinno

    @contextmanager
    def gpio_init(self):
        try:
            # GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.forward_pinno, GPIO.OUT)
            GPIO.setup(self.backward_pinno, GPIO.OUT)
            # GPIO.setup([self.forward_pinno, self.backward_pinno], GPIO.OUT)
            yield
        except Exception as e:
            print(e)
            print(e.__traceback__)
        finally:
            GPIO.cleanup(self.forward_pinno)
            GPIO.cleanup(self.backward_pinno)
            # GPIO.cleanup([self.forward_pinno, self.backward_pinno])

    def forward(self):
        with self.gpio_init():
            GPIO.output(self.forward_pinno, GPIO.HIGH)
            GPIO.output(self.backward_pinno, GPIO.LOW)

    def backward(self):
        with self.gpio_init():
            GPIO.output(self.forward_pinno, GPIO.LOW)
            GPIO.output(self.backward_pinno, GPIO.HIGH)

    def stop(self):
        with self.gpio_init():
            GPIO.output(self.forward_pinno, GPIO.LOW)
            GPIO.output(self.backward_pinno, GPIO.LOW)


class Whells(object):
    def __init__(
        self,
        left_whell_forward_pinno=11,
        left_whell_backward_pinno=13,
        right_whell_forward_pinno=12,
        right_whell_backward_pinno=16,
    ):
        self.left_whell = Whell(left_whell_forward_pinno, left_whell_backward_pinno)
        self.right_whell = Whell(right_whell_forward_pinno, right_whell_backward_pinno)

    @staticmethod
    def with_config(config):
        whells = Whells(
            left_whell_forward_pinno=config["LEFT_WHELL"]["FORWARD_PINNO"],
            left_whell_backward_pinno=config["LEFT_WHELL"]["BACKWARD_PINNO"],
            right_whell_forward_pinno=config["RIGHT_WHELL"]["FORWARD_PINNO"],
            right_whell_backward_pinno=config["RIGHT_WHELL"]["BACKWARD_PINNO"],
        )
        return whells

    def forward(self, sec=2):
        print("Forwarding....")
        self.left_whell.forward()
        self.right_whell.forward()

    def backward(self, sec=2):
        print("Backwarding....")
        self.left_whell.backward()
        self.right_whell.backward()

    def turn_left(self, sec=2):
        print("Turning Left....")
        self.left_whell.backward()
        self.right_whell.forward()

    def turn_right(self, sec=2):
        print("Turning Right...")
        self.left_whell.forward()
        self.right_whell.backward()

    def stop(self):
        print("Stopping...")
        self.left_whell.stop()
        self.right_whell.stop()
