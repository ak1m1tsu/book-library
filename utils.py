from enum import Enum
from sqlalchemy.ext.declarative import DeclarativeMeta

import json


class ClientCommands(Enum):
    GET_BOOK_LIST = 0
    ADD_BOOK = 1
    FIND_BOOK_BY_AUTHOR = 2
    FIND_BOOK_BY_NAME = 3
    DELETE_BOOK = 4
    DISCONNECT_FROM_SERVER = 5
    TURN_OF_SERVER = 6


class ServerResponses(Enum):
    GET_ALL = 'get_all'
    ADD = 'add'
    FIND_BY_NAME = 'find_by_name'
    FIND_BY_AUTHOR = 'find_by_author'
    DELETE = 'del'
    DISCONNECT_USER = 'bye'
    STOP_SERVER = 'stop'


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [
                x for x in dir(obj)
                if not x.startswith('_')
                and x != 'metadata'
                        ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)
