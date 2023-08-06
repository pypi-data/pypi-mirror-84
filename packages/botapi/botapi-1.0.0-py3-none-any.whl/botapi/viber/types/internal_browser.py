from typing import Optional

from .base import ViberObject, ViberField


class InternalBrowser(ViberObject):
    """
    Represents a Viber internal browser object

    Examples:
    https://developers.viber.com/docs/tools/keyboard-examples/
    """

    __min_api_version__ = 3

    action_button = ViberField(alias='ActionButton')
    action_predefined_url = ViberField(alias='ActionPredefinedURL')
    title_type = ViberField(alias='TitleType')
    custom_title = ViberField(alias='CustomTitle')
    mode = ViberField(alias='Mode')
    footer_type = ViberField(alias='FooterType')
    action_reply_data = ViberField(alias='ActionReplyData', min_api_version=6)

    def __init__(
        self,
        action_button: Optional[str] = None,
        action_predefined_url: Optional[str] = None,
        title_type: Optional[str] = None,
        custom_title: Optional[str] = None,
        mode: Optional[str] = None,
        footer_type: Optional[str] = None,
        action_reply_data: Optional[str] = None
    ):
        """
        Object, which includes internal browser configuration for
        open-url action with internal type

        More info: https://developers.viber.com/docs/tools/keyboards/#keyboard-examples

        :param action_button:
        :param action_predefined_url:
        :param title_type:
        :param custom_title:
        :param mode:
        :param footer_type:
        :param action_reply_data:
        """
        self.action_button = action_button
        self.action_predefined_url = action_predefined_url
        self.title_type = title_type
        self.custom_title = custom_title
        self.mode = mode
        self.footer_type = footer_type
        self.action_reply_data = action_reply_data
