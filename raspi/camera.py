import picamera


def take_a_picture(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.rotation = 180
        camera.capture(filename)
