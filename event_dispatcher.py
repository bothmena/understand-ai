from pubsub import pub
from utils.helpers import event_data_mapper
from utils.constants import Topics


def dispatch(events_file: str):
    with open(events_file, 'r') as f:
        line = f.readline().strip()
        while line:
            attributes = line.split(',')
            topic, data = attributes[0], attributes[1:]

            pub.sendMessage(topic, **event_data_mapper(topic, data))
            line = f.readline().strip()

    pub.sendMessage(Topics.END_OF_STREAM)
