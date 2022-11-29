from enum import Enum

class OptionType(Enum):
    LIKE = 0
    COMMENT = 1


class StateType(Enum):
    UNREAD = 0
    READ = 1


class ObjectType(Enum):
    OBJECT_POST = 0
    OBJECT_REPLY = 1
