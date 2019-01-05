from time import gmtime, strftime

import requests

from config import API_HOST
from camera import take_a_picture


def get_time():
    return strftime("%Y-%m-%d.%H:%M:%S", gmtime())


def get_version():
    API_URL = "http://{}/api/v1/version".format(API_HOST)
    r = requests.get(API_URL)
    result = r.json()
    print(result)


def image_processing(filename, color_in_hand, flags, mode="box"):
    API_URL = "http://{}/api/v1/image_processing".format(API_HOST)
    current_time = get_time()
    new_filename = "{}.jpg".format(current_time)
    # new_filename = "{}.{}".format(current_time, filename)
    print(new_filename)
    take_a_picture(new_filename)
    print(new_filename)
    with open(new_filename, "rb") as f:
        r = requests.post(
            API_URL,
            files={"file": f},
            data={
                "color_in_hand": color_in_hand,
                "flags": "{}, {}, {}".format(
                    flags["red"], flags["blue"], flags["green"]
                ),
                "mode": mode,
            },
        )

    result = r.json()
    print(result)
    return result["x"], result["y"], result["color_in_hand"]
