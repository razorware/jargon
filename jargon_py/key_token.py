import uuid


class KeyToken:

    @property
    def name(self):
        return self.__token

    def __init__(self, token):
        self.__token = token
        self.__handle = uuid.uuid4()

    def __hash__(self):
        return self.__handle.__hash__()

    def __eq__(self, other):
        return self.__handle == other.__handle

    def __ne__(self, other):
        return self.__handle != other.__handle
