from .base import ViberObject, ViberField


class Location(ViberObject):
    """
    Represents a Viber location object
    """

    latitude = ViberField(alias='lat')
    longitude = ViberField(alias='lon')

    def __init__(self, latitude: str, longitude: str):
        """
        :param latitude: From -90 to 90 degrees
        :param longitude: From -180 to 180 degrees
        """
        self.latitude = latitude
        self.longitude = longitude
