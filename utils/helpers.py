import numpy as np

from src.events import *


def event_data_mapper(event_id: str, values: list) -> dict:
    """
    Given an event_id (box_moved, frame_added, ...) return the data as a dict

    :param event_id:
    :return:
    """
    mapper = {
        'frame_added': FrameAddedEvent(),
        'box_created': BoxCreatedEvent(),
        'box_deleted': BoxDeletedEvent(),
        'box_moved': BoxMovedEvent(),
        'box_attribute_changed': BoxAttributeChangedEvent(),
    }

    return mapper[event_id].get_data(values)


def iou(image: np.ndarray, x: int, y: int, width: int, height: int) -> tuple:
    """
    Calculate the Intersection over Union (IoU) between the box that is contained in the image and the full box.
    values should be between 0 & 1.

    :param x: box top-left point coordinate on x-axe
    :param y: box top-left point coordinate on y-axe
    :param width: box width
    :param height: box height
    :param image: the image
    :return: float: 0 not contained, 1 contained fully, else: contained partially.
    """
    y_in = min(max(y, 0), image.shape[0])
    height_in = min(max(0, y + height), image.shape[0]) - y_in

    x_in = min(max(x, 0), image.shape[1])
    width_in = min(max(0, x + width), image.shape[1]) - x_in

    iou_ = (height_in * width_in) / (height * width)

    return iou_, (x_in, y_in, width_in, height_in)
