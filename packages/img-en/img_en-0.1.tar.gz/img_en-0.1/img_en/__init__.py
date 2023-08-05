import numpy
import cv2


def enlarge(img, zoom):
    img = numpy.array(img, dtype=numpy.uint8)
    height, width, channel = img.shape
    finalimg = numpy.random.randint(1, size=(height * zoom, width * zoom, 3), dtype=numpy.uint8)

    for py in range(len(img)):
        for px in range(len(img[py])):
            holdx = px * zoom
            holdy = py * zoom
            finalimg[holdy:holdy + zoom, holdx:holdx + zoom] = img[py][px]
    return finalimg


def load(file):
    return cv2.imread(file)


def show(title, img):
    cv2.imshow(title, img)


def wait(key):
    cv2.waitKey(key)


def save(filename, img):
    cv2.imwrite(filename, img)
    return "Image saved"
