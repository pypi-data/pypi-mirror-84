from typing import Optional

from .base import ViberField
from .keyboard import Keyboard
from .message import Message


class FileMessage(Message):
    """
    Represents a Viber file message object

    https://developers.viber.com/docs/api/rest-bot-api/#file-message
    """

    message_type = ViberField(default='file', alias='type')
    media = ViberField()
    size = ViberField()
    file_name = ViberField()

    def __init__(
        self,
        media: str,
        size: int,
        file_name: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None
    ):
        """
        :param media: URL of the file.
            Max size 50 MB.
            Forbidden file formats:
            https://developers.viber.com/docs/api/rest-bot-api/#forbiddenFileFormats

        :param size: Size of the file in bytes

        :param file_name: Name of the file. File name should include extension.
            Max 256 characters (including file extension).
            Sending a file without extension or with the wrong extension
            might cause the client to be unable to open the file

        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            max 4000 characters
        """
        self.media = media
        self.size = size
        self.file_name = file_name
        self.tracking_data = tracking_data
        self.keyboard = keyboard
