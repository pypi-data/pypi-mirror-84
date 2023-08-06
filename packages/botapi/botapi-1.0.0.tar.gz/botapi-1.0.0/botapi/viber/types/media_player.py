from typing import Optional

from .base import ViberObject, ViberField


class MediaPlayer(ViberObject):
    """
    Represents a Viber media player object

    Examples:
    https://developers.viber.com/docs/tools/keyboard-examples/
    """

    __min_api_version__ = 6
    title = ViberField(alias='Title')
    subtitle = ViberField(alias='Subtitle')
    thumbnail_url = ViberField(alias='ThumbnailURL')
    loop = ViberField(alias='Loop')

    def __init__(
        self,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        loop: Optional[bool] = None
    ):
        """
        Object. Specifies media player options.
        Will be ignored if OpenURLMediaType is not video or audio

        :param title: Media player’s title (first line)
        :param subtitle: Media player’s subtitle (second line)
        :param thumbnail_url: The URL for player’s thumbnail (background)
        :param loop: Whether the media player should be looped forever or not
        """
        self.title = title
        self.subtitle = subtitle
        self.thumbnail_url = thumbnail_url
        self.loop = loop
