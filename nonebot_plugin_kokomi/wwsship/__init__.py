from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import os
import sys
# 数据响应模块
wws_ship = on_keyword({'wws me ship'})


@wws_ship.handle()
async def xz(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    info_message = str(event.get_message())
    if info_message[0] != 'w':
        await wws_ship.finish()
    if '.rank' in info_message:
        await wws_ship.finish()
    if info_message.replace('wws me ship', '') == info_message:
        ship_name = info_message.replace('wws me ship', '')
    else:
        ship_name = info_message.replace('wws me ship ', '')
    file_path = os.path.dirname(__file__).replace(
        'wwsship', '') + 'function'
    sys.path.append(file_path)
    import tool
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wws_ship.finish(Message('您没有绑定账号，请发送wws [server] set [id]绑定'))
    pic_type_name = tool.get_pic_name(int(pic_type))
    if pic_type_name[0] != 'success':
        await wws_ship.finish(Message(pic_type_name[1]))
    file_path = os.path.dirname(__file__).replace(
        'wwsship', '') + 'pic/'+pic_type_name[1]
    sys.path.append(file_path)
    import wwsmeship
    run_code, pic_path = wwsmeship.wws_me_ship(account_id, server, ship_name)
    if run_code != 'success':
        await wws_ship.finish(Message(pic_path))
    await wws_ship.send(MessageSegment.image("file:///"+pic_path))
    os.remove(pic_path)
