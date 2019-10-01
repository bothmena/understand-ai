from pubsub import pub

from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups, Topics


class OnBoxAttributeChangedEventListener(EventListener):
    def __init__(self):
        self.state = DictionaryState()

    def handle(self, box_id: str, attribute_id: str, attribute_value: str):
        self.state.update(StateGroups.BOX, box_id, (attribute_id, attribute_value))
        if attribute_id == 'label' and attribute_value == 'traffic_light':
            pub.sendMessage(Topics.EXTRACT_BOX, box_id=box_id)
