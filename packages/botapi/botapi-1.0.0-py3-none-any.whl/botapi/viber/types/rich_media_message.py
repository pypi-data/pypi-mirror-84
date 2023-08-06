from typing import Optional

from .base import ViberField
from .keyboard import Keyboard
from .message import Message
from .rich_media import RichMedia


class RichMediaMessage(Message):
    """
    Represents a Viber rich media message object

    https://developers.viber.com/docs/api/rest-bot-api/
    #rich-media-message--carousel-content-message
    """

    __min_api_version__ = 7
    message_type = ViberField(default='rich_media', alias='type')
    rich_media = ViberField(base=RichMedia)
    alt_text = ViberField()

    def __init__(
        self,
        rich_media: RichMedia,
        alt_text: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None
    ):
        """
        :param rich_media: RichMedia object to send

        :param alt_text: Backward compatibility text, limited to 7,000 characters

        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            max 4000 characters
        """
        self.rich_media = rich_media
        self.alt_text = alt_text
        self.tracking_data = tracking_data
        self.keyboard = keyboard
