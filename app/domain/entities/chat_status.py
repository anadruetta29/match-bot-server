from enum import Enum

class ChatStatus(str, Enum):
    STARTED = "started"
    FINISHED = "finished"