from enum import Enum
import datetime

class MessageType(Enum):
    WARNING = "Warning"
    INFO = "Info"

class Message:
    def __init__(self, text: str, message_type: MessageType):
        self.text = text
        self.message_type = message_type

    def __str__(self):
        now = datetime.datetime.now().strftime("%a, %B %d, %H:%M:%S")
        return f"**{self.message_type.value}**: {self.text}\n{now}"