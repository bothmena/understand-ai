import os

import cv2
from pubsub import pub
import matplotlib.pyplot as plt

from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups, Topics
from utils.helpers import iou


class OnExtractBoxEventListener(EventListener):
    """
    This Event Listener will:
    - Assess if the bounding box is contained (fully or partially) in the image or not.
    - If the BBox is:
        - contained fully: extract the whole BBox and save it
        - contained partially: extract the part that is contained in the image and saved it
        - not contained: does nothing
    - update the label of the box "is_contained" to be either 1 (yes), 0 (no) or 0.5(partly).
    - update the label of the box "path" to be the path where the BBox is saved.
    - publish an event so the annotator annotates the BBox.
    """
    def __init__(self,
                 boxes_path: str = '/home/bothmena/Projects/PyCharm/ai_training/UnderstandAI/Homework/var/processing/boxes',
                 boxes_ext: str = 'png',
                 width_threshold: int = 10,
                 height_threshold: int = 10,
                 ):
        self.state = DictionaryState()
        self.boxes_path = boxes_path
        self.boxes_ext = boxes_ext
        self.width_threshold = width_threshold
        self.height_threshold = height_threshold

    def handle(self, box_id: str):
        # querying the box and converting its data to int instead of float.
        box = self.state.query(StateGroups.BOX, box_id)
        box_data = [box['x'], box['y'], box['width'], box['height']]
        x, y, width, height = list(map(int, box_data))

        frame = self.state.query(StateGroups.FRAME, box['frame_id'])

        # read image and convert colors
        image = cv2.imread(frame['path'])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # check if the box is contained or not and update box attributes
        box_iou, (x_in, y_in, width_in, height_in) = iou(image, x, y, width, height)
        pub.sendMessage(Topics.BOX_ATTRIBUTE_CHANGED, box_id=box_id, attribute_id='is_contained',
                        attribute_value=box_iou)

        if box_iou == 0:
            return
        if width_in < self.width_threshold or height_in < self.height_threshold:
            return

        # extracting the box from the image and saving it.
        box_image = image[y_in:y_in + height_in, x_in:x_in + width_in, :]
        filename = '{}.{}'.format(box_id, self.boxes_ext)
        path = os.path.join(self.boxes_path, filename)
        plt.imsave(path, box_image)

        pub.sendMessage(Topics.BOX_ATTRIBUTE_CHANGED, box_id=box_id, attribute_id='path', attribute_value=path)
        pub.sendMessage(Topics.CLASSIFY_TRAFFIC_LIGHT, box_id=box_id)
