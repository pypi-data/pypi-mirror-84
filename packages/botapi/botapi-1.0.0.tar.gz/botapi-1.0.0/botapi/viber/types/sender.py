from typing import Optional

from .base import ViberObject, ViberField


class Sender(ViberObject):
    """
    Represents a Viber sender media object
    """

    name = ViberField()
    avatar = ViberField()

    def __init__(self, name: Optional[str] = None, avatar: Optional[str] = None):
        """
        :param name: The sender’s name to display. Max 28 characters
        :param avatar: The sender’s avatar URL.
            Avatar size should be no more than 100 kb.
            Recommended 720x720
        """
        self.name = name
        self.avatar = avatar
