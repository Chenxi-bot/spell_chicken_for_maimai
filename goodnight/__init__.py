
from nonebot.adapters import Message
from nonebot import on_command, on_keyword, on_message
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg
import json
import sys

sys.path.append(__path__)
from .save import save

good_night = on_command("gn", aliases=set(["晚安", "GN"]), priority=5)


@good_night.handle()
async def say_bye(bot: Bot, event: Event):
    user_id = event.get_user_id()
    
    await bot.send(message=save(), event=event)
