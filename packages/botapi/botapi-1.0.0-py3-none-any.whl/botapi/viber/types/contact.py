from .base import ViberObject, ViberField


class Contact(ViberObject):
    """
    Represents a Viber contact object
    """

    name = ViberField()
    phone_number = ViberField()

    def __init__(self, name: str, phone_number: str):
        """
        :param name: Name of the contact. Max 28 characters
        :param phone_number: Phone number of the contact. Max 18 characters
        """
        self.name = name
        self.phone_number = phone_number
