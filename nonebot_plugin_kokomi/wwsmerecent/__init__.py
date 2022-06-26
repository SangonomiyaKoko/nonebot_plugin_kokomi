
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import time
import os
from PIL import ImageFont, Image, ImageDraw
import sys
# 数据响应模块
pvp_recent = on_keyword({'wws me recent'})


@pvp_recent.handle()
async def xz(bot: Bot, event: Event, state: T_State):
    info_message = str(event.get_message())
    user_qqid = event.get_user_id()
    if info_message[0] != 'w':
        await pvp_recent.finish()
    if info_message == 'wws me recent':
        info_date = 1
    else:
        if info_message.replace('wws me recent', '') == info_message:
            info_date = info_message.replace('wws me recent', '')
        else:
            info_date = info_message.replace('wws me recent ', '')
        if info_date.isdigit() != True:
            await pvp_recent.finish(Message('输入的参数有问题'))
        info_date = int(info_date)
    if info_date <= 0 or info_date > 365:
        await pvp_recent.finish(Message('输入的参数有问题'))
    file_path = os.path.dirname(__file__).replace(
        'wwsmerecent', '') + 'function'
    sys.path.append(file_path)
    import tool
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await pvp_recent.finish(Message('您没有绑定账号，请发送wws [server] set [id]绑定'))
    pic_type_name = tool.get_pic_name(int(pic_type))
    if pic_type_name[0] != 'success':
        await pvp_recent.finish(Message(pic_type_name[1]))
    file_path = os.path.dirname(__file__).replace(
        'wwsmerecent', '') + 'pic/'+pic_type_name[1]
    sys.path.append(file_path)
    import wwsmerecent

    run_code, pic_path = wwsmerecent.pvprecent(account_id, server, info_date)
    if run_code != 'success':
        await pvp_recent.finish(Message(pic_path))
    await pvp_recent.send(MessageSegment.image("file:///"+pic_path))
    os.remove(pic_path)


rank_recent = on_keyword({'wws me rank recent'})


@rank_recent.handle()
async def xz(bot: Bot, event: Event, state: T_State):
    info_message = str(event.get_message())
    user_qqid = event.get_user_id()
    if user_qqid != '3197206779':
        await rank_recent.finish(Message('更新维护中，暂时无法查询，具体更新内容及更新时间请查看qq空间的更新公告'))
    if info_message[0] != 'w':
        await rank_recent.finish()
    if info_message == 'wws me rank recent':
        info_date = 1
    else:
        if info_message.replace('wws me rank recent', '') == info_message:
            info_date = info_message.replace('wws me rank recent', '')
        else:
            info_date = info_message.replace('wws me rank recent ', '')
        if info_date.isdigit() != True:
            await rank_recent.finish(Message('输入的参数有问题'))
        info_date = int(info_date)
    if info_date <= 0 or info_date > 365:
        await rank_recent.finish(Message('输入的参数有问题'))
    file_path = os.path.dirname(__file__).replace(
        'wwsmerecent', '') + 'function'
    sys.path.append(file_path)
    import tool
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await rank_recent.finish(Message('您没有绑定账号，请发送wws [server] set [id]绑定'))
    pic_type_name = tool.get_pic_name(int(pic_type))
    if pic_type_name[0] != 'success':
        await rank_recent.finish(Message(pic_type_name[1]))
    file_path = os.path.dirname(__file__).replace(
        'wwsmerecent', '') + 'pic/'+pic_type_name[1]
    sys.path.append(file_path)
    import wwsmerecent
    run_code, pic_path = wwsmerecent.rankrecent(account_id, server, info_date)
    if run_code != 'success':
        await rank_recent.finish(Message(pic_path))
    await rank_recent.send(MessageSegment.image("file:///"+pic_path))
    os.remove(pic_path)
