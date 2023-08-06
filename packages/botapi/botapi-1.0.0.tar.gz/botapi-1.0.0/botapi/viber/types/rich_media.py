from typing import Optional

from .base import ViberObject, ViberField
from .button import Button
from .favorites_metadata import FavoritesMetadata


class RichMedia(ViberObject):
    """
    Represents a Viber rich media object

    https://developers.viber.com/docs/api/rest-bot-api/
    #rich-media-message--carousel-content-message
    """

    buttons = ViberField(default=[], alias='Buttons')
    bg_color = ViberField(alias='BgColor')
    media_type = ViberField(default='rich_media', alias='Type')
    buttons_group_columns = ViberField(alias='ButtonsGroupColumns')
    buttons_group_rows = ViberField(alias='ButtonsGroupRows')
    favorites_metadata = ViberField(base=FavoritesMetadata, alias='FavoritesMetadata')

    def __init__(
        self,
        buttons: list,
        buttons_group_columns: Optional[int] = None,
        buttons_group_rows: Optional[int] = None,
        bg_color: Optional[str] = None,
        favorites_metadata: Optional[FavoritesMetadata] = None
    ):
        """
        :param buttons: list of RichMediaButton objects.
            Max of 6 * ButtonsGroupColumns * ButtonsGroupRows

        :param buttons_group_columns: Number of columns per carousel content block.
            Default 6 columns. Values: 1-6

        :param buttons_group_rows: 	Number of rows per carousel content block.
            Default 7 rows. Values: 1-7

        :param bg_color: background color. Default: #FFFFFF

        :param favorites_metadata: Object, which describes
            Carousel content to be saved via favorites bot, if saving is available
            see: https://developers.viber.com/docs/tools/keyboards/#favoritesMetadata
        """
        self.buttons = buttons
        self.buttons_group_columns = buttons_group_columns
        self.buttons_group_rows = buttons_group_rows
        self.bg_color = bg_color
        self.favorites_metadata = favorites_metadata

    def add_button(self, button: Button) -> None:
        """
        Append button to buttons array

        :param button: Button object
        :return: None
        """
        self.buttons.append(button)
