from unittest import result
from nonebot.adapters import Message
from nonebot import on_command, on_keyword, on_message
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
import json


def help_sc():
    help_ = "欢迎使用晨汐bot maimai拼机助手！\n使用方法：\n\t1.输入sc [定数]查询该定数的全部曲目\n\t2.输入sc [定数1] [定数2]查询难度同时包含定数1和定数2的曲目\n\t3.输入sc [定数1下界] [定数1上界] [定数2下界] [定数2上界]查询难度同时包含定数1的范围和定数2的范围的曲目\n\n曲名后有标注（DX）的为DX谱面，未标注为标准谱面"
    return help_


def show_song(titles, data, *etc):
    """输入筛选的歌曲和数据库，转换成Message发送给用户

    参数：
        titles: 歌曲标题，以'd'或者'l'开始，用以区分DX与普通
        data: 歌曲数据库
    """

    if etc != tuple([]):
        lines = ""
        tags = {"l": ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"],
                "d": ["dx_lev_bas", "dx_lev_adv", "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"]}
        for title in titles:
            tmp_title = title[1:]
            line = f"\n{tmp_title} "
            if title[0] == "d":
                line += "（DX） "
            line += str(etc[0])

            for tag in tags[title[0]]:
                try:
                    if float(data[tmp_title][tag]) == float(etc[0]):
                        dicts = {"lev_bas": "（绿）", "lev_adv": "（黄）", "lev_exp": "（红）", "lev_mas": "（紫）", "lev_remas": "（白）",
                                 "dx_lev_bas": "（绿）", "dx_lev_adv": "（黄）", "dx_lev_exp": "（红）", "dx_lev_mas": "（紫）", "dx_lev_remas": "（白）"}
                        line += f" {dicts[tag]} "
                except:
                    continue
            lines += line
        return "为您找到以下歌曲：" + lines

    lines = ""
    for title in titles:
        tmp_title = title[1:]
        line = f"\n{tmp_title}"
        if title[0] == "d":
            line += "（DX）"
        line += ": \n"
        tags = {"l": ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"],
                "d": ["dx_lev_bas", "dx_lev_adv", "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"]}
        for tag in tags[title[0]]:
            try:
                line += f"/{data[tmp_title][tag]}"
            except:
                pass
        lines += line
    if lines == "":
        return "抱歉，没有符合条件的歌曲"
    else:
        return "为您找到以下歌曲：" + lines


def select_song(args):
    # pass
    song_data_path = "/home/maimai/SCHelper/src/plugins/output.json"
    tags = ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"]
    answer = []
    songs = {}
    with open(song_data_path, "r", encoding="utf-8") as f:
        songs = json.loads(f.read())

    for song in songs.keys():
        flag1 = 0
        for tag in tags:
            try:
                if float(songs[song][tag]) == args[0]:
                    flag1 += 1
            except Exception as e:
                pass
        if flag1 >= 1:
            answer.append("l" + song)

    tags = ["dx_lev_bas", "dx_lev_adv",
            "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"]
    for song in songs.keys():
        flag1 = 0
        for tag in tags:
            try:
                if float(songs[song][tag]) == args[0]:
                    flag1 += 1
            except:
                pass
        if flag1 >= 1:
            answer.append("d" + song)
    return show_song(answer, songs, args[0])


def double_select_song(args):
    song_data_path = "/home/maimai/SCHelper/src/plugins/output.json"
    tags = ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"]
    answer = []
    songs = {}
    with open(song_data_path, "r", encoding="utf-8") as f:
        songs = json.loads(f.read())
    # 此处新增了一个情况，是输入两个数字的搜索方法
    for song in songs.keys():
        flag1 = 0
        flag2 = 0
        for tag in tags:
            try:
                if float(songs[song][tag]) == args[0]:
                    flag1 += 1
                if float(songs[song][tag]) == args[1]:
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
                if float(songs[song][tag]) == args[0]:
                    flag1 += 1
                if float(songs[song][tag]) == args[1]:
                    flag2 += 1
            except:
                pass
        if flag1 >= 1 and flag2 >= 1:
            answer.append("d" + song)
    return show_song(answer, songs)


def range_select_song(args):
    song_data_path = "/home/maimai/SCHelper/src/plugins/output.json"
    tags = ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"]
    answer = []
    songs = {}
    with open(song_data_path, "r", encoding="utf-8") as f:
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


def data_check(data):
    # 这里修改了一下，这次直接传进来的不包含'sc'，之前写的有点……
    """对数据进行检查和筛选"""
    if data[0] == "help":
        return help_sc()
    try:
        for i in range(len(data)):
            data[i] = float(data[i])
            if data[i] > 15.0 or data[i] < 1:
                return "输入的数据大小有误！"
    except:
        return "输入的数据有误！请使用\"sc help\"获得提示"

    if len(data) == 4:
        if data[0] > data[1] or data[2] > data[3]:
            return "是否按照顺序输入？"

    return data


def query_song(args):
    """通过参数对歌曲进行查询，根据args长度实现不同结果

    长度为1时，进行指定定数筛选

    长度为2时，进行指定定数双筛选

    长度为4时，进行范围筛选

    在使用时请自行设置json位置，修改内容为`song_data_path`
    """

    result = data_check(args)
    if type(result) == str:
        return result
    else:
        args = result

    if len(args) == 1:
        return select_song(args)
    if len(args) == 2:
        return double_select_song(args)
    if len(args) == 4:
        return range_select_song(args)


spell = on_command("sc", aliases=set(["拼机"]), priority=5)


@spell.handle()
async def spell_chicken(bot: Bot, event: Event):
    # 对收到的参数进行分割
    data = str(event.get_message()).split(" ")[1:]
    try:
        await bot.send(event=event, message=query_song(data))
    except Exception as e:
        #await bot.send(event=event, message=str(e))
        await bot.send(event=event, message="您输入的范围过大，由于QQ字数限制目前无法显示，请缩小查询范围")
        return
