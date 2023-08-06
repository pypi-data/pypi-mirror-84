from typing import Optional

from .base import ViberObject, ViberField


class Frame(ViberObject):
    """
    Represents a Viber frame object

    Examples:
    https://developers.viber.com/docs/tools/keyboard-examples/
    """

    __min_api_version__ = 6
    border_width = ViberField(alias='BorderWidth')
    border_color = ViberField(alias='BorderColor')
    corner_radius = ViberField(alias='CornerRadius')

    def __init__(
        self,
        border_width: Optional[int] = None,
        border_color: Optional[str] = None,
        corner_radius: Optional[int] = None
    ):
        """
        Object. Draw frame above the background on the button,
        the size will be equal the size of the button

        :param border_width: Width of border
            Possible: 0..10
            Default: 0

        :param border_color: Color of border
            Possible: Hex color #XXXXXX
            Default: #000000

        :param corner_radius: The border will be drawn with rounded corners
            Possible: 0..10
            Default: 0
        """
        self.border_width = border_width
        self.border_color = border_color
        self.corner_radius = corner_radius
