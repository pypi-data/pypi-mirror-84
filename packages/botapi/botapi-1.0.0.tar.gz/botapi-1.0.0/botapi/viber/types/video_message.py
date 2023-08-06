from typing import Optional

from .base import ViberField
from .keyboard import Keyboard
from .message import Message


class VideoMessage(Message):
    """
    Represents a Viber video message object

    https://developers.viber.com/docs/api/rest-bot-api/#video-message
    """

    message_type = ViberField(default='video', alias='type')
    media = ViberField()
    size = ViberField()
    duration = ViberField()
    thumbnail = ViberField()

    def __init__(
        self,
        media: str,
        size: int,
        duration: Optional[int] = None,
        thumbnail: Optional[str] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None
    ):
        """
        :param media: URL of the video. Max size 26 MB.
            Only MP4 and H264 are supported.
            The URL must have a resource with a .mp4
            file extension as the last path segment. The file must be
            Example: http://www.example.com/path/video.mp4.

        :param size: Size of the video in bytes

        :param duration: Video duration in seconds;
            will be displayed to the receiver.
            Max 180 seconds

        :param thumbnail: URL of a reduced size image. Max size 100 kb.
            Recommended: 400x400. Only JPEG format is supported

        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            max 4000 characters
        """
        self.media = media
        self.size = size
        self.duration = duration
        self.thumbnail = thumbnail
        self.tracking_data = tracking_data
        self.keyboard = keyboard
