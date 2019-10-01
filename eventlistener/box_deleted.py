from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups
import os


class OnBoxDeletedEventListener(EventListener):
    def __init__(self):
        self.state = DictionaryState()

    def handle(self, box_id: str):
        box = self.state.query(StateGroups.BOX, box_id)
        if 'path' in box and os.path.isfile(box['path']):
            os.remove(box['path'])
        self.state.remove(StateGroups.BOX, box_id)
