import os
import shutil

from abstract.interface import EventListener
from src.state import DictionaryState
from utils.constants import StateGroups


class OnFrameAddedEventListener(EventListener):
    """
    This Event Listener will:
    - Move the frame image file from the input directory (frames_path) to the processing directory.
    - Save the frame data to the state of the app (filename, path, ...)
    """
    def __init__(self, frames_path: str = '/home/bothmena/Projects/PyCharm/ai_training/UnderstandAI/Homework/var/input',
                 processing_dir: str = '/home/bothmena/Projects/PyCharm/ai_training/UnderstandAI/Homework/var/processing',
                 frame_ext: str = 'png'):
        self.frames_path = frames_path
        self.processing_dir = processing_dir
        self.frame_ext = frame_ext
        self.state = DictionaryState()
        os.makedirs(os.path.join(self.processing_dir, 'frames'), exist_ok=True)
        os.makedirs(os.path.join(self.processing_dir, 'boxes'), exist_ok=True)

    def handle(self, frame_id: int) -> None:
        """
        :param frame_id: id of the frame
        """
        filename = '{}.{}'.format(frame_id, self.frame_ext)
        path = os.path.join(self.processing_dir, 'frames', filename)
        # os.rename(os.path.join(self.frames_path, filename), path)
        shutil.copyfile(os.path.join(self.frames_path, filename), path)
        self.state.insert(StateGroups.FRAME, frame_id, {'filename': filename, 'path': path})
