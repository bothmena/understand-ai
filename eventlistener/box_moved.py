from pubsub import pub

from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups, Topics


class OnBoxMovedEventListener(EventListener):
    def __init__(self):
        self.state = DictionaryState()

    def handle(self, box_id: str, x: float, y: float, width: float, height: float):
        for key, value in {'x': x, 'y': y, 'width': width, 'height': height}.items():
            if value is not None:
                self.state.update(StateGroups.BOX, box_id, (key, value))

        box = self.state.query(StateGroups.BOX, box_id)
        if 'label' in box and box['label'] == 'traffic_light':
            pub.sendMessage(Topics.EXTRACT_BOX, box_id=box_id)
