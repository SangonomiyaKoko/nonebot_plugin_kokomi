from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import os
import sys
# 数据响应模块
wws_me = on_keyword({'wws me'})


@wws_me.handle()
async def xz(bot: Bot, event: Event, state: T_State):
    info_msg = str(event.get_message())
    user_qqid = event.get_user_id()
    if info_msg[0] != 'w':
        await wws_me.finish()
    if 'ship' in info_msg:
        await wws_me.finish()
    if 'recent' in info_msg:
        await wws_me.finish()
    if 'rank' in info_msg:
        await wws_me.finish()
    if 'info' in info_msg:
        await wws_me.finish()
    if info_msg == 'wws me':
        await wws_me.finish(Message('您没有输入参数，请发送wws help查询对应指令'))
    file_path = os.path.dirname(__file__).replace(
        'wwsmeall', '') + 'function'
    sys.path.append(file_path)
    import tool
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wws_me.finish(Message('您没有绑定账号，请发送wws [server] set [id]绑定'))
    pic_type_name = tool.get_pic_name(int(pic_type))
    if pic_type_name[0] != 'success':
        await wws_me.finish(Message(pic_type_name[1]))
    file_path = os.path.dirname(__file__).replace(
        'wwsmeall', '') + 'pic/'+pic_type_name[1]
    sys.path.append(file_path)
    import wwsmeall
    run_code, pic_path = wwsmeall.wws_me_all(account_id, info_msg, server)
    if run_code != 'success':
        await wws_me.finish(Message(pic_path))
    await wws_me.send(MessageSegment.image("file:///"+pic_path))
    os.remove(pic_path)
