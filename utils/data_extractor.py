class DataExtractor:
    @staticmethod
    def extract(arguments: list, types: list, values: list) -> dict:
        data = {}
        for i, value in enumerate(values):
            data[arguments[i]] = DataExtractor._cast(value, types[i])

        return data

    @staticmethod
    def _cast(initial_value: str, new_type: type):
        """
        cast a string value to another type (new_type) and handles the value error exception

        :param initial_value: value as a string
        :param new_type: type to be converted to: int, float, str
        :return:
        """

        if new_type == str:
            return initial_value
        elif initial_value.strip() == 'None':
            return None
        else:
            # try:
            return new_type(initial_value.strip())
            # except ValueError:
            #
            #     return None
