from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups


class OnBoxCreatedEventListener(EventListener):
    def __init__(self):
        self.state = DictionaryState()

    def handle(self, frame_id: int, box_id: str, x: float, y: float, width: float, height: float):
        self.state.insert(StateGroups.BOX, box_id,
                          {'x': x, 'y': y, 'width': width, 'height': height, 'frame_id': frame_id})
