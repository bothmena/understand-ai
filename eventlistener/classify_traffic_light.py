import numpy as np
from pubsub import pub

from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups, Topics


class OnClassifyTrafficLightEventListener(EventListener):
    def __init__(self):
        self.state = DictionaryState()

    def handle(self, box_id: str):
        # query the box for state and load the bbox image
        box = self.state.query(StateGroups.BOX, box_id)
        annotation = ['green', 'red', 'orange', 'off'][np.random.choice([0, 1, 2, 3])]

        pub.sendMessage(Topics.BOX_ATTRIBUTE_CHANGED, box_id=box_id, attribute_id='color', attribute_value=annotation)
