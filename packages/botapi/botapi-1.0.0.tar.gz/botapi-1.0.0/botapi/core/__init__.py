import asyncio
import sys

from .api_object import BaseObjectMeta, BotObject
from .field import Field
from .mixins import FieldSerializeMixin
from .session import BotSession

if sys.platform.startswith('win'):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

__all__ = (
    'Field',
    'FieldSerializeMixin',
    'BaseObjectMeta',
    'BotObject',
    'BotSession'
)
