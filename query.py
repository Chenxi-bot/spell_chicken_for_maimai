from nonebot.adapters import Message
from nonebot import on_command, on_keyword, on_message
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
import json


def show_song(titles, data):
    lines = ""
    for title in titles:
        tmp_title = title[1:]
        line = f"\n{tmp_title}"
        if title[0] == "d":
            line += "（dx难度）"
        line += ": \n"
        tags = {"l": ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"],
                "d": ["dx_lev_bas", "dx_lev_adv", "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"]}
        for tag in tags[title[0]]:
            try:
                line += f"/ {data[tmp_title][tag]}"
            except:
                pass
        lines += line
    if lines == "":
        return "抱歉，没有符合条件的歌曲"
    else:
        return "为您找到以下歌曲：\n" + lines


def query_song(args):
    tags = ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"]
    answer = []
    songs = {}
    with open("/home/maimai/SCHelper/src/plugins/output.json", "r", encoding="utf-8") as f:
        songs = json.loads(f.read())
    # 关于数据，格式为json，读取后的格式为:
    # songs[title] = song_data
    # 其中song_data的结构中至少包含以下键值
    # "title", (("lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas") or/and ("dx_lev_bas", "dx_lev_adv", "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"))
    for song in songs.keys():
        flag1 = 0
        flag2 = 0
        for tag in tags:
            try:
                if float(songs[song][tag]) <= args[1] and float(songs[song][tag]) >= args[0]:
                    flag1 += 1
                if float(songs[song][tag]) <= args[3] and float(songs[song][tag]) >= args[2]:
                    flag2 += 1
            except Exception as e:
                pass
        if flag1 >= 1 and flag2 >= 1:
            answer.append("l" + song)

    tags = ["dx_lev_bas", "dx_lev_adv",
            "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"]
    for song in songs.keys():
        flag1 = 0
        flag2 = 0
        for tag in tags:
            try:
                if float(songs[song][tag]) <= args[1] and float(songs[song][tag]) >= args[0]:
                    flag1 += 1
                if float(songs[song][tag]) <= args[3] and float(songs[song][tag]) >= args[2]:
                    flag2 += 1
            except:
                pass
        if flag1 >= 1 and flag2 >= 1:
            answer.append("d" + song)
    return show_song(answer, songs)


spell = on_command("sc", aliases=set(["拼机"]), priority=5)


@spell.handle()
async def spell_chicken(bot: Bot, event: Event):
    # 对收到的参数进行分割
    data = str(event.get_message()).split(" ")
    # 对参数检验，参数数量是否为4
    if len(data) != 5:
        notice = "错误的格式！\n参考：/拼机 定数范围1 定数范围2 定数范围3 定数范围4"
        await bot.send(event=event, message=notice)
        return
    data = data[1:]
    # 对参数检验，输入是否为浮点数
    try:
        for i in range(len(data)):
            data[i] = float(data[i])
            if data[i] > 15.0 or data[i] < 1:
                await bot.send(event=event, message="输入的数据大小有误！")
                return

        if data[0] > data[1] or data[2] > data[3]:
            await bot.send(event=event, message="是否按照顺序输入？")
            return
    except Exception as e:
        await bot.send(event=event, message=f"输入的数据有误！")
        return
    try:
        await bot.send(event=event, message=query_song(data))
    except Exception:
        await bot.send(event=event, message="您输入的范围过大，由于QQ字数限制目前无法显示，请缩小查询范围")
