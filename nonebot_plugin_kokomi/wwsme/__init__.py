from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import os
import sys
wws_me = on_keyword({'wws me info'})


@wws_me.handle()
async def xz(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    info_message = str(event.get_message())
    if info_message[0] != 'w':
        await wws_me.finish()
    file_path = os.path.dirname(__file__).replace(
        'wwsme', '') + 'function'
    sys.path.append(file_path)
    import tool
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wws_me.finish(Message('您没有绑定账号，请发送wws [server] set [id]绑定'))
    pic_type_name = tool.get_pic_name(int(pic_type))
    if pic_type_name[0] != 'success':
        await wws_me.finish(Message(pic_type_name[1]))
    file_path = os.path.dirname(__file__).replace(
        'wwsme', '') + 'pic/'+pic_type_name[1]
    sys.path.append(file_path)
    import wwsme
    run_code, pic_path = wwsme.wws_me(account_id, server)
    if run_code != 'success':
        await wws_me.finish(Message(pic_path))
    await wws_me.send(MessageSegment.image("file:///"+pic_path))
    os.remove(pic_path)
