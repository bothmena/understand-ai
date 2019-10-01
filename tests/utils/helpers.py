import numpy as np

from utils.helpers import iou

image = np.ones(shape=(1700, 2500, 3))
fully_contained = [(2000, 1100, 300, 300)]
not_contained = [(2600, 1800, 300, 300), (-500, -500, 300, 300), (-500, 200, 300, 300), (400, -500, 300, 300)]
partly_contained = [(2400, 1600, 300, 300), (-100, -100, 300, 300)]


def test_iou_fully_contained():
    for x, y, w, h in fully_contained:
        result, (x_in, y_in, width_in, height_in) = iou(image, x, y, w, h)
        assert result == 1., \
            "value = {} for values x = {} / y = {} / width = {} / height = {} but it should be = 1". \
                format(result, x, y, w, h)
        assert x == x_in, 'x and x_in should be equal'
        assert y == y_in, 'y and y_in should be equal'
        assert w == width_in, 'w and width_in should be equal'
        assert h == height_in, 'h and height_in should be equal'


def test_iou_partly_contained():
    for x, y, w, h in partly_contained:
        result, _ = iou(image, x, y, w, h)
        assert 0. < result < 1., \
            "value = {} for values x = {} / y = {} / width = {} / height = {} but it should be between 0 & 1". \
                format(result, x, y, w, h)


def test_iou_not_contained():
    for x, y, w, h in not_contained:
        result, _ = iou(image, x, y, w, h)
        assert result == 0., \
            "value = {} for values x = {} / y = {} / width = {} / height = {} but it should be = 0". \
                format(result, x, y, w, h)


if __name__ == "__main__":
    test_iou_fully_contained()
    print("Fully contained passed")
    test_iou_partly_contained()
    print("Partly contained passed")
    test_iou_not_contained()
    print("Not contained passed")
