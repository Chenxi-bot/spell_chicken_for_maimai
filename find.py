from nonebot.adapters import Message
from nonebot import on_command, on_keyword, on_message
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
import json


def find_song(args):
    answer = ""
    song_data_path = "/home/maimai/SCHelper/src/plugins/output.json"
    with open(song_data_path, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    for title in data.keys():
        if args[0].upper() in title.upper():
            answer = title
            break
    return show_song(answer, data)


def show_song(title, data):
    line = ""
    for tag in data[title].keys():
        if tag == "title":
            line += "乐曲名："
        elif tag == "artist":
            line += "\n艺术家："
        elif tag == "category":
            line += "\n流派："
        elif tag == "lev_bas":
            line += "\n难度（标准）："
        elif tag == "dx_lev_bas":
            line += "\n难度（DX）："
        elif tag == "version":
            line += "\n版本："
        if tag != "image_file" and tag != "status":
            line += f"{data[title][tag]} "
    if line == "":
        return "抱歉，没有符合条件的歌曲"
    else:
        return "为您找到以下歌曲：\n" + line


query = on_command("f", aliases=set(["查询"]), priority=5)


@query.handle()
async def find(bot: Bot, event: Event):
    data = str(event.get_message()).split(" ")[1:]
    try:
        await bot.send(event=event, message=find_song(data))
    except Exception as e:
        await bot.send(event=event, message=str(e))
        # await bot.send(event=event, message="您输入的范围过大，由于QQ字数限制目前无法显示，请缩小查询范围")
        return
