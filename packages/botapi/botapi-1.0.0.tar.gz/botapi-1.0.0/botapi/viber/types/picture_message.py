from typing import Optional

from .base import ViberField
from .keyboard import Keyboard
from .message import Message


class PictureMessage(Message):
    """
    Represents a Viber picture message object

    https://developers.viber.com/docs/api/rest-bot-api/#picture-message
    """

    message_type = ViberField(default='picture', alias='type')
    text = ViberField()
    media = ViberField()
    thumbnail = ViberField()

    def __init__(
        self,
        text: str,
        media: str,
        thumbnail: Optional[str] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None
    ):
        """
        :param text: Description of the photo. Can be an empty string if irrelevant.
            Max 120 characters

        :param media: The URL must have a resource with a .jpeg, .png or .gif file
            extension as the last path segment.
            Example: http://www.example.com/path/image.jpeg.
            Animated GIFs can be sent as URL messages or file messages.
            Max image size: 1MB on iOS, 3MB on Android.

        :param thumbnail: URL of a reduced size image (JPEG, PNG, GIF).
            Recommended: 400x400. Max size: 100kb.

        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            max 4000 characters
        """
        self.text = text
        self.media = media
        self.thumbnail = thumbnail
        self.tracking_data = tracking_data
        self.keyboard = keyboard
