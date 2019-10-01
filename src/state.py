from abstract.interface import State
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

    def update(self, group: str, key: Union[str, int], value: Union[dict, tuple]):
        """
        update an existing item in the state

        :param group: either frames or boxes
        :param key: frame_id or box_id
        :param value: updated value
        :raise: ItemNotFoundException if the item to be updated does not exist
        """
        if self.query(group, key) is None:
            raise ItemNotFoundException()
        elif isinstance(value, dict):
            self.state[group][key] = value
        else:
            if len(value) != 2:
                raise ValueError('is value is a tuple it should have 2 and only 2 items: key and value')
            att_key, att_val = value
            self.state[group][key][att_key] = att_val

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

    def remove(self, group: str, key: str):
        """
        removes an item from the state.

        :param group: either frames or boxes
        :param key: frame_id or box_id
        """
        if self.query(group, key) is not None:
            del self.state[group][key]
