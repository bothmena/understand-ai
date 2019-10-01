import os
import json
import shutil

from abstract.interface import EventListener
from src.state import DictionaryState


class OnEndOfStreamEventListener(EventListener):
    """
    This event is fired at the end of the event log.
    This Event Listener will:
    - Export the state of the application that contains all the information about the frames and boxes to a json file.
    - If clear_state = True, it will reset the state to its initial value
    - If clear_storage = True, it will remove all the images (frames and boxes) from the processing directory.
    """
    def __init__(self, output_dir: str = '/home/bothmena/Projects/PyCharm/ai_training/UnderstandAI/Homework/var/output',
                 processing_dir: str = '/home/bothmena/Projects/PyCharm/ai_training/UnderstandAI/Homework/var/processing',
                 filename: str = 'annotated_data.json', clear_state: bool = False, clear_storage: bool = False):
        self.state = DictionaryState()
        self.output_dir = output_dir
        self.processing_dir = processing_dir
        self.filename = filename
        self.clear_state = clear_state
        self.clear_storage = clear_storage
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def handle(self):
        with open(os.path.join(self.output_dir, self.filename), 'w') as fp:
            json.dump(self.state.state, fp)
        if self.clear_state:
            self.state.reset_state()
        if self.clear_storage:
            shutil.rmtree(self.processing_dir)
