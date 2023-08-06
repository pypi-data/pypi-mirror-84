from .base import ViberObject, ViberField


class Map(ViberObject):
    """
    Represents a Viber button object

    Examples:
    https://developers.viber.com/docs/tools/keyboard-examples/
    """
    __min_api_version__ = 6

    latitude = ViberField(alias='Latitude')
    longitude = ViberField(alias='Longitude')

    def __init__(
        self,
        latitude: str,
        longitude: str
    ):
        """
        Object, which includes map configuration for open-map action with internal type

        :param latitude: Location latitude (format: “12.12345”)
        :param longitude: Location longitude (format: “3.12345”)
        """
        self.latitude = latitude
        self.longitude = longitude
