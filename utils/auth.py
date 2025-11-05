from functools import wraps
from typing import Callable
from aiogram import types
from aiogram.filters import BaseFilter

from utils.config import settings


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in settings.admin_ids


class IsWhitelisted(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if not settings.require_whitelist:
            return True
        
        if message.from_user.id in settings.admin_ids:
            return True
        
        if message.from_user.id in settings.whitelist_users:
            return True
        
        return False


def admin_required(func: Callable):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        if message.from_user.id not in settings.admin_ids:
            await message.reply(
                "⛔ Akses ditolak. Perintah ini hanya untuk administrator."
            )
            return
        return await func(message, *args, **kwargs)
    return wrapper


def whitelist_required(func: Callable):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        if settings.require_whitelist:
            if (message.from_user.id not in settings.whitelist_users and 
                message.from_user.id not in settings.admin_ids):
                await message.reply(
                    "⛔ Akses ditolak. Bot ini memerlukan whitelist untuk digunakan.\n"
                    "Hubungi administrator untuk mendapatkan akses."
                )
                return
        return await func(message, *args, **kwargs)
    return wrapper
