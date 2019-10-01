from abstract.interface import Event


class FrameAddedEvent(Event):
    @property
    def args_names(self) -> list:
        return ['frame_id']

    @property
    def args_types(self) -> list:
        return [int]


class BoxCreatedEvent(Event):
    @property
    def args_names(self) -> list:
        return ['frame_id', 'box_id', 'x', 'y', 'width', 'height']

    @property
    def args_types(self) -> list:
        return [int, str, float, float, float, float]


class BoxDeletedEvent(Event):
    @property
    def args_names(self) -> list:
        return ['box_id']

    @property
    def args_types(self) -> list:
        return [str]


class BoxMovedEvent(Event):
    @property
    def args_names(self) -> list:
        return ['box_id', 'x', 'y', 'width', 'height']

    @property
    def args_types(self) -> list:
        return [str, float, float, float, float]


class BoxAttributeChangedEvent(Event):
    @property
    def args_names(self) -> list:
        return ['box_id', 'attribute_id', 'attribute_value']

    @property
    def args_types(self) -> list:
        return [str, str, str]
