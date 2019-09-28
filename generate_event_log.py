"""
This file generates a fake event log to stdout. You can pipe it to a csv file.
It will create a fixed number of events that operate on a fixed number of videos with a fixed number of frames.
You can assume that all frames are 1280x720 pixel in size. Boxes may lie completely outside of these borders.

The possible events are:

BoxCreated(frame_id: str, box_id: str, x: float, y: float, width: float, height: float, timestamp: float, labeler: str)
BoxDeleted(box_id: str, timestamp: float, labeler: str)
BoxMoved(box_id: str, x: Optional[float], y: Optional[float], width: Optional[float], height: Optional[float], timestamp: float, labeler: str)
BoxAttributeChanged(box_id: str, attribute_key: str, attribute_value: Optional[str], timestamp: float, labeler: str)
BoxConnected(box_a_id: Optional[str], box_b_id: Optional[str], timestamp: float, labeler: str)


Example usage:
python generate_event_log.py >> output.csv
"""
from __future__ import annotations
import random
from typing import List, Dict, Tuple, Optional, TypeVar
from uuid import uuid4


def main() -> None:
    # tiny
    # num_events = 10
    # num_frames = 1
    # small
    # num_events = 100
    # num_frames = 100
    # medium
    num_events = 2000
    num_frames = 500
    fill_event_log(num_frames=num_frames, num_events=num_events)


def fill_event_log(num_frames: int, num_events: int) -> None:
    frames_for_video = generate_frames(num_frames=num_frames)
    generate_events(frames_for_video=frames_for_video, num_events=num_events)


def generate_frames(num_frames: int) -> Dict[str, List[str]]:
    num_videos = 1
    frames_for_video = dict()
    for _ in range(num_videos):
        video_id = generate_uuid()
        # print(f'video_added, {video_id}')
        frames_for_video[video_id] = list()
        frame_ids = generate_frame_ids(num_frames)
        for frame_id in frame_ids:
            print(f'frame_added, {frame_id}')
            frames_for_video[video_id].append(frame_id)
    return frames_for_video


def generate_frame_ids(num_frames: int) -> List[int]:
    potential_ids = list(range(1, 1000))
    return list(random.choices(potential_ids, k=num_frames))


def generate_events(frames_for_video: Dict[str, List[str]], num_events: int) -> None:
    labelers = [
        'Sergio Villanueva',
        'Ryleigh Tapia',
        'Kennedi Mcneil',
        'Madisyn Huber',
        'Gracelyn Hobbs',
        'Nyasia Le',
        'Jorge Mason',
        'Heidy Archer',
        'Kaleb Davies',
        'Keagan Haney',
        'Nicholas Estes',
        'Alfredo Duarte',
        'Janet Russo',
        'Taryn Meyer',
        'Bella Simpson',
        'Lina Walker',
        'Ella Howe',
        'Pierce Walls',
        'Raul Conner',
        'Evelyn Turner',
    ]
    attributes = {
        'label': ['car', 'pedestrian', 'rider', 'bicycle', 'motorcycle', 'bus', 'truck'],
        'is_parking': ['true', 'false'],
        'is_crossing': ['true', 'false']
    }
    metadata_generator = MetadataGenerator(labelers=labelers)

    num_events_created = 0
    existing_boxes = set()
    possible_events = ['box_created', 'box_deleted', 'box_moved', 'box_attribute_changed']
    event_probabilities = [0.3, 0.05, 0.25, 0.4]
    # generate random events
    while num_events_created < num_events:
        event_type = random.choices(possible_events, event_probabilities)[0]
        if len(existing_boxes) == 0 or event_type == 'box_created':
            new_box_id = generate_box_created_event(frames_for_video=frames_for_video,
                                                    metadata_generator=metadata_generator)
            existing_boxes.add(new_box_id)
        elif event_type == 'box_deleted':
            deleted_box_id = generate_box_deleted_event(existing_boxes=list(existing_boxes),
                                                        metadata_generator=metadata_generator)
            existing_boxes.remove(deleted_box_id)
        elif event_type == 'box_moved':
            generate_box_moved_event(existing_boxes=list(existing_boxes), metadata_generator=metadata_generator)
        elif event_type == 'box_attribute_changed':
            generate_box_attribute_changed_event(existing_boxes=list(existing_boxes), attributes=attributes,
                                                 metadata_generator=metadata_generator)
        else:
            raise ValueError(f'Invalid event type {event_type}')
        num_events_created += 1


def generate_box_created_event(frames_for_video: Dict[str, List[str]], metadata_generator: MetadataGenerator) -> str:
    video_id = random.choice(list(frames_for_video.keys()))
    frame_id = random.choice(frames_for_video[video_id])
    box_id = generate_uuid()
    x, y, width, height = generate_coordinates()
    timestamp, labeler = metadata_generator.generate_metadata()
    print(f'box_created, {frame_id}, {box_id}, {x}, {y}, {width}, {height}')
    return box_id


def generate_box_deleted_event(existing_boxes: List[str], metadata_generator: MetadataGenerator) -> str:
    box_id = random.choice(existing_boxes)
    timestamp, labeler = metadata_generator.generate_metadata()
    print(f'box_deleted, {box_id}')
    return box_id


def generate_box_moved_event(existing_boxes: List[str], metadata_generator: MetadataGenerator) -> None:
    box_id = random.choice(existing_boxes)
    x, y, width, height = generate_coordinates()
    x, y, width, height = maybe_none(x), maybe_none(y), maybe_none(width), maybe_none(height)
    timestamp, labeler = metadata_generator.generate_metadata()
    print(f'box_moved, {box_id}, {x}, {y}, {width}, {height}')


def generate_box_attribute_changed_event(existing_boxes: List[str], attributes: Dict[str, List[str]],
                                         metadata_generator: MetadataGenerator) -> None:
    box_id = random.choice(existing_boxes)
    attribute_id = random.choice(list(attributes.keys()))
    attribute_value = random.choice(attributes[attribute_id])
    attribute_value = maybe_none(attribute_value)
    timestamp, labeler = metadata_generator.generate_metadata()
    print(f'box_attribute_changed, {box_id}, {attribute_id}, {attribute_value}')


def generate_uuid() -> str:
    return str(uuid4())


def generate_coordinates() -> Tuple[float, float, float, float]:
    x = random.uniform(-20, 1300)
    y = random.uniform(-20, 740)
    width = random.uniform(5, 500)
    height = random.uniform(5, 500)
    return x, y, width, height


class MetadataGenerator:
    def __init__(self, labelers: List[str]) -> None:
        self._labelers: List[str] = labelers
        self._last_timestamp: float = 0.0

    def generate_metadata(self) -> Tuple[float, str]:
        self._last_timestamp += random.uniform(0, 10)
        labeler = random.choice(self._labelers)
        return self._last_timestamp, labeler


T = TypeVar('T')


def maybe_none(value: T) -> Optional[T]:
    weights = [0.8, 0.2]
    return random.choices([value, None], weights)[0]


if __name__ == '__main__':
    random.seed(42)
    main()
