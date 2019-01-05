import os
import cv2
import numpy as np

MEDIAN_BLUR_RANGE = 17

RED_THRESHOLD = 64
GREEN_THRESHOLD = 32
BLUE_THRESHOLD = 32

DROP_THRESHOLD = 96


DROP_ZONE_COLORS = {"red": "yellow", "green": "cyan", "blue": "magenta"}


def get_image(path):
    return cv2.imread(path)


def get_contours(color_matrix, title="unknown", filename="", threshold=64):
    image = cv2.cvtColor(color_matrix, cv2.COLOR_GRAY2RGBA)

    display_image(image, title=title, filename=filename)

    image = cv2.medianBlur(image, MEDIAN_BLUR_RANGE)
    ret, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    display_image(image, title="{}-threshold".format(title), filename=filename)

    image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    contours = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    return contours


def check_distance(contours, maxX=0, maxY=0, color="", set_color=""):
    _color = color
    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cntX = int(M["m01"] / M["m00"])
            if cntX > maxX:
                maxX = cntX
                maxY = int(M["m10"] / M["m00"])
                _color = set_color

    return maxX, maxY, _color


def check_drop_zone_color(color):
    c1 = 0
    c2 = 0
    if color == "yellow":
        c1 = 1
        c2 = 2
    if color == "cyan":
        c1 = 1
        c2 = 0
    if color == "magenta":
        c1 = 0
        c2 = 2

    return c1, c2


def display_image(img, title="image", filename=""):
    pwd = os.getcwd()
    dirpath = os.path.join(pwd, "raspi_images", filename)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    new_filename = os.path.join(dirpath, "{}.png".format(title))
    print(new_filename)
    print("Write image")
    cv2.imwrite(new_filename, img)


def find_box(img, filename="", flags={}):
    print("Find Box")
    display_image(img, title="real", filename=filename)
    print("Displayed Image.")

    xSize, ySize, _ = img.shape
    img = cv2.medianBlur(img, MEDIAN_BLUR_RANGE)
    sortedImgIndex = np.argsort(img, 2)

    display_image(img, title="blur", filename=filename)
    for j in range(xSize):
        for i in range(ySize):
            img[j, i, sortedImgIndex[j, i, 2]] = (
                img[j, i, sortedImgIndex[j, i, 2]] - img[j, i, sortedImgIndex[j, i, 1]]
            )
            img[j, i, sortedImgIndex[j, i, 1]] = 0
            img[j, i, sortedImgIndex[j, i, 0]] = 0

    maxX = 0
    maxY = 0
    color = ""
    print(flags)
    if not flags["red"]:
        print("Red Searching...")
        contours = get_contours(
            img[:, :, 2], title="red", filename=filename, threshold=RED_THRESHOLD
        )
        maxX, maxY, color = check_distance(
            contours, maxX=maxX, maxY=maxY, color=color, set_color="red"
        )

    if not flags["green"]:
        print("Green Searching...")
        contours = get_contours(
            img[:, :, 1], title="green", filename=filename, threshold=GREEN_THRESHOLD
        )
        maxX, maxY, color = check_distance(
            contours, maxX=maxX, maxY=maxY, color=color, set_color="green"
        )

    if not flags["blue"]:
        print("Blue Searching...")
        contours = get_contours(
            img[:, :, 0], title="blue", filename=filename, threshold=BLUE_THRESHOLD
        )
        maxX, maxY, color = check_distance(
            contours, maxX=maxX, maxY=maxY, color=color, set_color="blue"
        )

    maxNormX = maxX / xSize
    maxNormY = maxY / ySize
    return maxNormX, maxNormY, color


def find_drop_zone(img, color_in_hand, filename=""):
    print("Find Drop Done")
    drop_zone_color = DROP_ZONE_COLORS[color_in_hand]
    xSize, ySize, _ = img.shape

    img = cv2.medianBlur(img, MEDIAN_BLUR_RANGE)
    sortedImgIndex = np.argsort(img, 2)
    c1, c2 = check_drop_zone_color(drop_zone_color)
    print("Start For Loop")
    for j in range(xSize):
        for i in range(ySize):
            img[j, i, sortedImgIndex[j, i, 2]] = np.max(
                2 * img[j, i, sortedImgIndex[j, i, 1]]
                - img[j, i, sortedImgIndex[j, i, 2]],
                0,
            )
            img[j, i, sortedImgIndex[j, i, 1]] = (
                img[j, i, sortedImgIndex[j, i, 1]] - img[j, i, sortedImgIndex[j, i, 0]]
            )
            img[j, i, sortedImgIndex[j, i, 0]] = 0
            img[j, i, sortedImgIndex[j, i, c1]] = (
                img[j, i, sortedImgIndex[j, i, c1]]
                + img[j, i, sortedImgIndex[j, i, c2]]
            ) / 2

    print("Finished For Loop")

    contours = get_contours(img[:, :, c1], title="drop_zone", threshold=DROP_THRESHOLD)
    maxX, maxY, _ = check_distance(contours)

    maxNormX = maxX / xSize
    maxNormY = maxY / ySize
    return maxNormX, maxNormY


def main(imagename="", imagepath="", mode="", filename="", flags={}, color_in_hand=""):
    img = get_image(imagepath)
    print("Mode is '{}'".format(mode))
    if mode == "box":
        return find_box(img, flags=flags, filename=imagename)
    elif mode == "drop_zone":
        return find_drop_zone(img, color_in_hand, filename=imagename), ""
    else:
        return "", "", ""
