from email.mime import application
from multiprocessing.sharedctypes import Value
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import requests
import json
import os
import sys
import sqlite3
# 数据响应模块
wws_set = on_keyword(
    {'wws asia set', 'wws eu set', 'wws ru set', 'wws na set'})


@wws_set.handle()
async def xz(bot: Bot, event: Event, state: T_State):
    try:
        user_qqid = event.get_user_id()
        error1 = ''
        sys.path.append(os.path.dirname(__file__).replace(
            'wwsset', '') + 'function')
        import tool

        info_message = str(event.get_message())
        nick_name = info_message.split()
        if info_message[0] != 'w':
            await wws_set.finish()
        if len(nick_name) != 4:
            await wws_set.finish(Message('输入的参数有误'))
        server = nick_name[1]
        if server not in {'asia', 'ru', 'eu', 'na'}:
            await wws_set.finish(Message('输入的服务器参数有误'))
        nick_name = nick_name[3]
        application_id = tool.get_application_id()
        url = 'https://api.worldofwarships.server/wows/account/list/?application_id=applicationid&search=name'
        url = url.replace('name', nick_name).replace(
            'server', server).replace('applicationid', application_id)
        api_data = requests.get(url=url)
        original_data = api_data.text
        processed_data = json.loads(original_data)
        if processed_data["status"] == "error":
            error_msg = "ERROR: "+processed_data["error"]["message"]
            await wws_set.finish(Message(error_msg))
        if processed_data["meta"]["count"] == 0:
            await wws_set.finish(Message(f"您输入的id {nick_name}不正确"))
        elif processed_data["meta"]["count"] == 1 or processed_data["data"][0]["nickname"] == nick_name:
            accountid = str(processed_data["data"][0]["account_id"])
        elif processed_data["data"][0]["nickname"].lower() == nick_name or processed_data["data"][0]["nickname"].upper() == nick_name:
            accountid = str(processed_data["data"][0]["account_id"])
        else:
            await wws_set.finish(Message(f"您输入的id {nick_name}不正确，请注意大小写"))

        conn = sqlite3.connect(tool.get_sqlit3_path())
        c = conn.cursor()
        cursor = c.execute(
            "SELECT QQID,ACCID,TYPE,LANGUAGE,TIME,SERVER,EXTER1,EXTER2  from userid")
        for row in cursor:
            if row[0] == int(user_qqid):
                old_accid = row[1]
                statements = "UPDATE userid set TIME = 0 where QQID=" + \
                    str(user_qqid)
                c.execute(statements)
                statements = "UPDATE userid set ACCID = " + \
                    str(accountid)+" where QQID="+str(user_qqid)
                c.execute(statements)
                statements = "UPDATE userid set SERVER = '" + \
                    str(server)+"' where QQID="+str(user_qqid)
                c.execute(statements)
                conn2 = sqlite3.connect(tool.get_accid_path())
                c2 = conn2.cursor()
                try:
                    c2.execute(
                        f"INSERT INTO accid (ACCID, TIME, SERVER) VALUES ({accountid},0,'{server}')")
                except:
                    continue
                conn2.commit()
                conn2.close()
                break
        if conn.total_changes == 3:
            conn.commit()
            conn.close()
            await wws_set.finish(Message(f"账号改绑成功\naccount_id: 从\n {old_accid} \n更改为->\n {accountid}"))
        else:
            statements = "INSERT INTO userid (QQID,ACCID,TYPE,LANGUAGE,TIME,SERVER,EXTER1,EXTER2) VALUES (" + str(
                user_qqid) + "," + str(accountid) + ", 1, 'cn', 0, '"+str(server)+"', '0', '0' )"
            c.execute(statements)
            conn.commit()
            conn.close()
            conn2 = sqlite3.connect(tool.get_accid_path())
            c2 = conn2.cursor()
            try:
                c2.execute(
                    f"INSERT INTO accid (ACCID, TIME, SERVER) VALUES ({accountid},0,{server})")
            except:
                print('已经存在该账号的recent数据')
            conn2.commit()
            conn2.close()
            await wws_set.finish(Message("账号绑定成功\n欢迎使用kokomibot\n发送wws help以查询指令集"))

    except Exception as e:
        error1 = error1 + str(e)
        if error1 != '':
            error1 = "发生错误,code:"+error1
            await wws_set.finish(Message(error1))
