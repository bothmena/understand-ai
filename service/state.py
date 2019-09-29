from abstract.service import State
from typing import Union
from utils.exception.state import ItemExistException, ItemNotFoundException


class DictionaryState(State):

    @property
    def state(self):
        return self._state

    def init_state(self) -> dict:
        """
        define the initial state, should be called to initialize and reset the state

        :return: initial state value
        """
        return {'frames': {}, 'boxes': {}}

    def insert(self, group: str, key: Union[str, int], value: dict):
        """
        insert an item in the state, the method should not override existing items

        :param group: either frames or boxes
        :param key: frame_id or box_id
        :param value: value
        :raise: ItemExistException if the item exist already
        """
        if self.query(group, key) is None:
            self.state[group][key] = value
        else:
            raise ItemExistException()

    def update(self, group: str, key: Union[str, int], value: dict):
        """
        update an existing item in the state

        :param group: either frames or boxes
        :param key: frame_id or box_id
        :param value: updated value
        :raise: ItemNotFoundException if the item to be updated does not exist
        """
        if self.query(group, key) is None:
            raise ItemNotFoundException()
        else:
            self.state[group][key] = value

    def query(self, group: str, key: str) -> Union[dict, None]:
        """
        :param group: either frames or boxes
        :param key: frame_id or box_id
        :return: dictionary with all queried item attributes, or None if not found.
        """
        try:
            return self.state[group][key]
        except KeyError:
            return None
