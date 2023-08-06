from typing import Optional

from .base import ViberObject, ViberField


class Webhook(ViberObject):
    url = ViberField()
    event_types = ViberField()
    send_name = ViberField()
    send_photo = ViberField()

    def __init__(
        self,
        url: str,
        event_types: Optional[list] = None,
        send_name: Optional[bool] = None,
        send_photo: Optional[bool] = None
    ):
        """
        :param url: Account webhook URL to receive callbacks & messages from users.
            Webhook URL must use SSL
            Note: Viber doesn’t support self signed certificates

        :param event_types: Indicates the types of Viber events that the account
            owner would like to be notified about.
            Don’t include this parameter in your request to get all events.
            Default: [
              "delivered",
              "seen",
              "failed",
              "subscribed",
              "unsubscribed",
              "conversation_started"
           ]

        :param send_name: Indicates whether or not the bot should receive the user name.
            Default: false

        :param send_photo: Indicates whether or not the bot should
            receive the user photo.
            Default: false
        """
        self.url = url
        self.event_types = event_types
        self.send_name = send_name
        self.send_photo = send_photo
