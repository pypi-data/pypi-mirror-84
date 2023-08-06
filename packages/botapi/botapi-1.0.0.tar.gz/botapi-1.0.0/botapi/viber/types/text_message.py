from typing import Optional

from .base import ViberField
from .keyboard import Keyboard
from .message import Message


class TextMessage(Message):
    """
    Represents a Viber text message object

    https://developers.viber.com/docs/api/rest-bot-api/#text-message
    """

    message_type = ViberField(default='text', alias='type')
    text = ViberField()

    def __init__(
        self, text: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None
    ):
        """
        :param text: The text of the message

        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            max 4000 characters
        """
        self.text = text
        self.tracking_data = tracking_data
        self.keyboard = keyboard
