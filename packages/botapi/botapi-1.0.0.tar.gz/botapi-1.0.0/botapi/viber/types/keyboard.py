from typing import Optional

from .base import ViberObject, ViberField
from .button import Button
from .favorites_metadata import FavoritesMetadata


class Keyboard(ViberObject):
    """
    Represents a Viber keyboard object

    https://developers.viber.com/docs/tools/keyboards/#keyboards
    """

    kb_type = ViberField(default='keyboard', alias='Type')
    buttons = ViberField(default=[], alias='Buttons')
    bg_color = ViberField(alias='BgColor')
    default_height = ViberField(alias='DefaultHeight')
    custom_default_height = ViberField(alias='CustomDefaultHeight', min_api_version=3)
    height_scale = ViberField(alias='HeightScale', min_api_version=3)
    buttons_group_columns = ViberField(alias='ButtonsGroupColumns', min_api_version=4)
    buttons_group_rows = ViberField(alias='ButtonsGroupRows', min_api_version=4)
    input_field_state = ViberField(alias='InputFieldState', min_api_version=4)
    favorites_metadata = ViberField(base=FavoritesMetadata,
                                    alias='FavoritesMetadata',
                                    min_api_version=6)

    def __init__(
        self,
        buttons: Optional[list] = None,
        bg_color: Optional[str] = None,
        default_height: Optional[bool] = None,
        custom_default_height: Optional[int] = None,
        height_scale: Optional[int] = None,
        buttons_group_columns: Optional[int] = None,
        buttons_group_rows: Optional[int] = None,
        input_field_state: Optional[str] = None,
        favorites_metadata: Optional[FavoritesMetadata] = None
    ):
        """
        :param buttons: list containing keyboard buttons by order

        :param bg_color: Background color of the keyboard.
            Possible values: Valid color HEX value
            Default value: Default Viber keyboard background

        :param default_height: optional. When true - the keyboard will always be
            displayed with the same height as the native keyboard.When false - short
            keyboards will be displayed with the minimal possible height.
            Maximal height will be native keyboard height.
            Default value: False

        :param custom_default_height: optional (api level 3). How much percent
            of free screen space in chat should be taken by keyboard.
            The final height will be not less than height of system keyboard.
            Possible values: 40..70

        :param height_scale: optional (api level 3). Allow use custom aspect ratio
            for Carousel content blocks. Scales the height of the default square block
            (which is defined on client side) to the given value in percents.
            It means blocks can become not square and it can be used to create
            Carousel content with correct custom aspect ratio.
            This is applied to all blocks in the Carousel content
            Possible values: 20..100
            Default value: 100

        :param buttons_group_columns: optional (api level 4).
            Represents size of block for grouping buttons during layout
            Possible values: 1-6
            Default value: 6

        :param buttons_group_rows: optional (api level 4).
            Represents size of block for grouping buttons during layout.
            Possible values: 1-7
            Default value: 2

        :param input_field_state: optional (api level 4).
            Customize the keyboard input field.
            regular - display regular size input field.
            minimized - display input field minimized by default.
            hidden - hide the input field
            Possible values: regular, minimized, hidden
            Default value: regular
        """
        self.buttons = buttons if buttons is not None else []
        self.bg_color = bg_color
        self.default_height = default_height
        self.custom_default_height = custom_default_height
        self.height_scale = height_scale
        self.buttons_group_columns = buttons_group_columns
        self.buttons_group_rows = buttons_group_rows
        self.input_field_state = input_field_state
        self.favorites_metadata = favorites_metadata

    def add_button(self, button: Button) -> None:
        """
        Append button to buttons array

        :param button: Button object
        :return: None
        """
        self.buttons.append(button)
