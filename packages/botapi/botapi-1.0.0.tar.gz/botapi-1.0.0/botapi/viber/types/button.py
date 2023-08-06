from typing import Optional

from .base import ViberObject, ViberField
from .frame import Frame
from .internal_browser import InternalBrowser
from .map import Map
from .media_player import MediaPlayer


class Button(ViberObject):
    """
    Represents a Viber button object

    Examples:
    https://developers.viber.com/docs/tools/keyboard-examples/
    """

    columns = ViberField(alias='Columns')
    rows = ViberField(alias='Rows')
    bg_color = ViberField(alias='BgColor')
    silent = ViberField(alias='Silent')
    bg_media_type = ViberField(alias='BgMediaType')
    bg_media = ViberField(alias='BgMedia')
    bg_media_scale_type = ViberField(alias='BgMediaScaleType', min_api_version=6)
    image_scale_type = ViberField(alias='ImageScaleType', min_api_version=6)
    bg_loop = ViberField(alias='BgLoop')
    action_type = ViberField(alias='ActionType')
    action_body = ViberField(alias='ActionBody')
    image = ViberField(alias='Image')
    text = ViberField(alias='Text')
    text_v_align = ViberField(alias='TextVAlign')
    text_h_align = ViberField(alias='TextHAlign')
    text_paddings = ViberField(alias='TextPaddings', min_api_version=4)
    text_opacity = ViberField(alias='TextOpacity')
    text_size = ViberField(alias='TextSize')
    open_url_type = ViberField(alias='OpenURLType')
    open_url_media_type = ViberField(alias='OpenURLMediaType')
    text_bg_gradient_color = ViberField(alias='TextBgGradientColor')
    text_should_fit = ViberField(alias='TextShouldFit', min_api_version=6)
    internal_browser = ViberField(base=InternalBrowser, alias='InternalBrowser')
    open_map = ViberField(base=Map, alias='Map')
    frame = ViberField(base=Frame, alias='Frame')
    media_player = ViberField(base=MediaPlayer, alias='MediaPlayer')

    def __init__(
        self,
        action_body: str,
        columns: Optional[int] = None,
        rows: Optional[int] = None,
        bg_color: Optional[str] = None,
        silent: Optional[bool] = None,
        bg_media_type: Optional[str] = None,
        bg_media: Optional[str] = None,
        bg_media_scale_type: Optional[str] = None,
        image_scale_type: Optional[str] = None,
        bg_loop: Optional[bool] = None,
        action_type: Optional[str] = None,
        image: Optional[str] = None,
        text: Optional[str] = None,
        text_v_align: Optional[str] = None,
        text_h_align: Optional[str] = None,
        text_paddings: Optional[list] = None,
        text_opacity: Optional[int] = None,
        text_size: Optional[str] = None,
        open_url_type: Optional[str] = None,
        open_url_media_type: Optional[str] = None,
        text_bg_gradient_color: Optional[str] = None,
        text_should_fit: Optional[bool] = None,
        internal_browser: Optional[InternalBrowser] = None,
        open_map: Optional[Map] = None,
        frame: Optional[Frame] = None,
        media_player: Optional[MediaPlayer] = None
    ):
        """
        The following parameters can be defined for each button in the “buttons”
        array separately. Each button must contain at least one of the
        following optional parameters: text, bg_media, image, bg_color.

        Parameters description, possible and default values:
        https://developers.viber.com/docs/tools/keyboards/#buttons-parameters
        """
        self.action_body = action_body
        self.columns = columns
        self.rows = rows
        self.bg_color = bg_color
        self.silent = silent
        self.bg_media_type = bg_media_type
        self.bg_media = bg_media
        self.bg_media_scale_type = bg_media_scale_type
        self.image_scale_type = image_scale_type
        self.bg_loop = bg_loop
        self.action_type = action_type
        self.image = image
        self.text = text
        self.text_v_align = text_v_align
        self.text_h_align = text_h_align
        self.text_paddings = text_paddings
        self.text_opacity = text_opacity
        self.text_size = text_size
        self.open_url_type = open_url_type
        self.open_url_media_type = open_url_media_type
        self.text_bg_gradient_color = text_bg_gradient_color
        self.text_should_fit = text_should_fit
        self.internal_browser = internal_browser
        self.open_map = open_map
        self.frame = frame
        self.media_player = media_player
