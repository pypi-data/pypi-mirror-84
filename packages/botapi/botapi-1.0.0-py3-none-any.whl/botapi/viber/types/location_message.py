from typing import Optional

from .base import ViberField
from .keyboard import Keyboard
from .location import Location
from .message import Message


class LocationMessage(Message):
    """
    Represents a Viber location message object

    https://developers.viber.com/docs/api/rest-bot-api/#location-message
    """

    message_type = ViberField(default='location', alias='type')
    location = ViberField(base=Location)

    def __init__(
        self,
        location: Location,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None
    ):
        """
        :param location: location to send

        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            max 4000 characters
        """
        self.location = location
        self.tracking_data = tracking_data
        self.keyboard = keyboard
