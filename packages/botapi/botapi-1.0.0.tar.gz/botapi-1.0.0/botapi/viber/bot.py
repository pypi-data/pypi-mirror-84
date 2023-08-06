from typing import Optional

from botapi.core.session import BotSession
from botapi.utils.log import viber_logger
from . import types
from .utils.constants import API_URL
from .utils.validators import check_response


class Bot(BotSession):
    """
    Provides work with Viber API
    """

    def __init__(
        self,
        token: str,
        **kwargs
    ):
        super().__init__(
            headers={
                'X-Viber-Auth-Token': token
            },
            **kwargs
        )

    async def request(self, method: str, data: Optional[dict] = None) -> dict:
        """
        This is coroutine.

        Makes request to Viber API and then checks response

        :param method: viber api method, ex. send_message, set_webhook etc.
        :param data: data to send
        :return: response
        """
        viber_logger.debug(f' Request to Viber API. Method: {method}. Data: {data}')
        async with self.session.post(
            **self._request_kwargs,
            url=''.join([API_URL, method]),
            json=data
        ) as response:
            return await check_response(method, response)

    async def set_webhook(
        self,
        url: str,
        event_types: Optional[list] = None,
        send_name: Optional[bool] = None,
        send_photo: Optional[bool] = None
    ) -> dict:
        """
        This is coroutine.

        Setting webhook to receive incoming updates

        :param url: Account webhook URL to receive callbacks & messages from users.
            Webhook URL must use SSL Note: Viber doesn’t support
            self signed certificates

        :param event_types: Indicates the types of Viber events that the
            account owner would like to be notified about.
            Don’t include this parameter in your request to get all events.
            Possible values: delivered, seen, failed, subscribed,
            unsubscribed  and conversation_started

        :param send_name: optional. Indicates whether or not the bot
            should receive the user name. Default false

        :param send_photo: optional. Indicates whether or not the bot
            should receive the user photo. Default false

        :return: response
        """
        webhook = types.Webhook(url, event_types, send_name, send_photo)
        return await self.request('set_webhook', webhook.serialize())

    async def remove_webhook(self) -> dict:
        """
        This is coroutine.

        Remove bot webhook

        :return: response
        """
        return await self.request('set_webhook')

    async def get_account_info(self) -> dict:
        """
        This is coroutine.

        Gets viber bot info

        :return: response
        """
        return await self.request('get_account_info')

    async def get_user_details(self, user_id: str) -> dict:
        """
        This is coroutine.

        Gets bot subscriber info

        :param user_id: subscriber user id
        :return: response
        """
        return await self.request('get_user_details', {'id': user_id})

    async def get_online(self, user_ids: list) -> dict:
        """
        This is coroutine.

        Gets online status of bot subscribers

        :param user_ids: list with subscribers id
        :return: response
        """
        return await self.request('get_online', {'ids': user_ids})

    async def send_message(
        self,
        receiver: str,
        text: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends text message to user.

        :param receiver: subscribed valid user id
        :param text: the text of the message
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        text_message = types.TextMessage(text, tracking_data, keyboard)
        data = {
            'receiver': receiver,
            **text_message.serialize(add_min_api_ver=True)
        }
        return await self.request('send_message', data=data)

    async def send_picture(
        self,
        receiver: str,
        media: str,
        text: Optional[str] = None,
        thumbnail: Optional[str] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends picture to user.

        :param receiver: subscribed valid user id
        :param media: URL of the image (JPEG, PNG, non-animated GIF).
            Example: http://www.example.com/path/image.jpeg.
            Animated GIFs can be sent as URL messages or file messages.
            Max image size: 1MB on iOS, 3MB on Android.
        :param text: Description of the photo. Can be an empty string if irrelevant.
            required. Max 120 characters
        :param thumbnail: URL of a reduced size image (JPEG, PNG, GIF).
            optional. Recommended: 400x400. Max size: 100kb.
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        picture_message = types.PictureMessage(
            text,
            media,
            thumbnail,
            tracking_data,
            keyboard
        )
        return await self.request('send_message', data={
            'receiver': receiver,
            **picture_message.serialize(add_min_api_ver=True)
        })

    async def send_video(
        self,
        receiver: str,
        media: str,
        size: int,
        duration: Optional[int] = None,
        thumbnail: Optional[str] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends video to user

        :param receiver: subscribed valid user id
        :param media: URL of the video (MP4, H264). Max size 26 MB.
            Only MP4 and H264 are supported. The URL must have a resource with a .mp4
            file extension as the last path segment.
            Example: http://www.example.com/path/video.mp4.
            The file must be
        :param size: Size of the video in bytes
        :param duration: Video duration in seconds; will be displayed to the receiver
        :param thumbnail: URL of a reduced size image (JPEG).
            Max size 100 kb. Recommended: 400x400. Only JPEG format is supported
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        video_message = types.VideoMessage(
            media,
            size,
            duration,
            thumbnail,
            tracking_data,
            keyboard
        )
        return await self.request('send_message', data={
            'receiver': receiver,
            **video_message.serialize(add_min_api_ver=True)
        })

    async def send_file(
        self,
        receiver: str,
        media: str,
        size: int,
        file_name: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends file to user

        :param receiver: subscribed valid user id
        :param media: URL of the file. Max size 50 MB.
            See forbidden file formats for unsupported file types:
            https://developers.viber.com/docs/api/rest-bot-api/#forbiddenFileFormats
        :param size: Size of the file in bytes
        :param file_name: Name of the file. File name should include extension.
            Max 256 characters (including file extension).
            Sending a file without extension or with the wrong extension
            might cause the client to be unable to open the file
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        file_message = types.FileMessage(
            media,
            size,
            file_name,
            tracking_data,
            keyboard
        )
        return await self.request('send_message', data={
            'receiver': receiver,
            **file_message.serialize(add_min_api_ver=True)
        })

    async def send_contact(
        self,
        receiver: str,
        name: str,
        phone_number: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends contact to user

        :param receiver: subscribed valid user id
        :param name: Name of the contact. Max 28 characters
        :param phone_number: Phone number of the contact. Max 18 characters
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        contact = types.Contact(name, phone_number)
        contact_message = types.ContactMessage(contact, tracking_data, keyboard)
        return await self.request('send_message', data={
            'receiver': receiver,
            **contact_message.serialize(add_min_api_ver=True)
        })

    async def send_location(
        self,
        receiver: str,
        latitude: str,
        longitude: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends location to user

        :param receiver: subscribed valid user id
        :param latitude: latitude (±90°)
        :param longitude: longitude (±180°)
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        location = types.Location(latitude, longitude)
        location_message = types.LocationMessage(location, tracking_data, keyboard)
        return await self.request('send_message', data={
            'receiver': receiver,
            **location_message.serialize(add_min_api_ver=True)
        })

    async def send_url(
        self,
        receiver: str,
        media: str,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends url to user

        :param receiver: subscribed valid user id
        :param media: URL. Max 2,000 characters
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        url_message = types.UrlMessage(media, tracking_data, keyboard)
        return await self.request('send_message', data={
            'receiver': receiver,
            **url_message.serialize(add_min_api_ver=True)
        })

    async def send_sticker(
        self,
        receiver: str,
        sticker_id: int,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends sticker to user

        :param receiver: subscribed valid user id
        :param sticker_id: Unique Viber sticker ID.
            For examples visit the sticker IDs page:
            https://developers.viber.com/docs/tools/sticker-ids
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        sticker_message = types.StickerMessage(sticker_id, tracking_data, keyboard)
        return await self.request('send_message', data={
            'receiver': receiver,
            **sticker_message.serialize(add_min_api_ver=True)
        })

    async def send_rich_media(
        self,
        receiver,
        rich_media: types.RichMedia,
        tracking_data: Optional[str] = None,
        keyboard: Optional[types.Keyboard] = None
    ) -> dict:
        """
        This is coroutine.

        Sends Rich Media to user.
        More info:
        https://developers.viber.com/docs/api/rest-bot-api/
        #rich-media-message--carousel-content-message

        :param receiver: subscribed valid user id
        :param rich_media: types.RichMedia object
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply.
            optional. max 4000 characters
        :param keyboard: types.Keyboard object to attach in request data
        :return: response
        """
        rich_media_message = types.RichMediaMessage(rich_media, tracking_data, keyboard)
        return await self.request('send_message', data={
            'receiver': receiver,
            **rich_media_message.serialize(add_min_api_ver=True)
        })

    async def send_broadcast(
        self,
        broadcast_list: list,
        message: types.Message
    ) -> dict:
        """
        This is coroutine.

        Sends message to many users.
        Every user must be subscribed and have a valid user id.
        The maximum list length is 300 receivers.

        :param broadcast_list: list with subscribers id
        :param message: type.Message object
        :return: response
        """
        return await self.request('send_message', data={
            'broadcast_list': broadcast_list,
            **message.serialize(add_min_api_ver=True)
        })
