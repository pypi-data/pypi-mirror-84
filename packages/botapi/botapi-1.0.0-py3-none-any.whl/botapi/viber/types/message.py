from abc import abstractmethod

from .base import ViberObject, ViberField
from .keyboard import Keyboard


class Message(ViberObject):
    """
    Represents a Viber message object with general message parameters

    https://developers.viber.com/docs/api/rest-bot-api/#general-send-message-parameters
    """

    tracking_data = ViberField()
    keyboard = ViberField(base=Keyboard)

    @property
    @abstractmethod
    def message_type(self):
        raise NotImplementedError
