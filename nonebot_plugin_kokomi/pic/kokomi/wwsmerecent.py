import requests
import json
import traceback
import time
from datetime import date, timedelta
import os
import sys
from PIL import ImageFont, Image, ImageDraw
# 数据响应模块


def pvprecent(account_id: int, server: str, info_date: int):
    try:
        sys.path.append(os.path.dirname(
            __file__).replace('pic/kokomi', 'function'))
        import tool
        today = date.today().strftime("%Y-%m-%d")
        beforeday = (date.today() + timedelta(days=-info_date)
                     ).strftime("%Y-%m-%d")
        recent_path = os.path.dirname(__file__).replace(
            'pic/kokomi', 'recent')+'/'+server+'/'+str(account_id) + '/date.json'
        today_path = recent_path.replace('user_qqid', str(
            account_id)).replace('date', today)
        beforeday_path = recent_path.replace('user_qqid', str(
            account_id)).replace('date', beforeday)

        if os.path.exists(today_path) == False:
            return('0x201', '数据丢失，请联系作者处理')
        if os.path.exists(beforeday_path) == False:
            return('0x202', '输入的时间过长，查询不到数据')
        today_data = open(today_path, "r", encoding="utf-8")
        todaydata = json.load(today_data)
        today_data.close()
        beforeday_data = open(beforeday_path, "r", encoding="utf-8")
        beforedaydata = json.load(beforeday_data)
        beforeday_data.close()

        if todaydata["meta"]["count"] == 0 or beforedaydata["meta"]["count"] == 0:
            return ('0x204', '没有数据请检查是否隐藏战绩')
        today_data = todaydata["data"][str(account_id)]
        beforeday_data = beforedaydata["data"][str(account_id)]
        today_len = len(today_data)
        beforeday_len = len(beforeday_data)

        y_coord = 455
        img = Image.open(os.path.dirname(__file__)+'/recent.png')
        draw = ImageDraw.Draw(img)
        font = tool.get_font(2, 27)
        font2 = tool.get_font(2, 40)
        font3 = tool.get_font(3, 40)

        all_battle = 0
        all_frag = 0
        all_damage_dealt = 0
        all_xp = 0
        all_pr = 0
        all_win = 0
        all_n_damage = 0
        all_n_frag = 0
        num = 0
        while num < today_len:
            i = 0
            new_battle = True
            while i < beforeday_len:
                today_ship_id = today_data[num]["ship_id"]
                before_ship_id = beforeday_data[i]["ship_id"]
                if today_ship_id == before_ship_id:
                    new_battle = False
                    break
                else:
                    i += 1
            if new_battle == True:
                battles = today_data[num]["pvp"]["battles"]
                if battles <= 0:
                    num += 1
                    continue
                all_battle += battles
                average_damage_dealt = int(
                    (today_data[num]["pvp"]["damage_dealt"])/battles)
                all_damage_dealt += today_data[num]["pvp"]["damage_dealt"]
                average_wins = round(
                    (today_data[num]["pvp"]["wins"])/battles*100, 2)
                all_win += today_data[num]["pvp"]["wins"]
                average_frag = round(
                    (today_data[num]["pvp"]["frags"])/battles, 2)
                all_frag += today_data[num]["pvp"]["frags"]
                average_xp = int((today_data[num]["pvp"]["xp"])/battles)
                all_xp += today_data[num]["pvp"]["xp"]
                if today_data[num]["pvp"]["main_battery"]["shots"] == 0:
                    average_hitrate = 0.0
                else:
                    average_hitrate = round((today_data[num]["pvp"]["main_battery"]["hits"])/(
                        today_data[num]["pvp"]["main_battery"]["shots"]), 2)

                ship_id = today_data[num]["ship_id"]
            else:
                battles = today_data[num]["pvp"]["battles"] - \
                    beforeday_data[i]["pvp"]["battles"]
                if today_data[num]["pvp"]["battles"] == 0 or battles <= 0:
                    num += 1
                    continue
                all_battle += battles
                average_damage_dealt = int(
                    (today_data[num]["pvp"]["damage_dealt"] - beforeday_data[i]["pvp"]["damage_dealt"])/battles)
                all_damage_dealt += today_data[num]["pvp"]["damage_dealt"] - \
                    beforeday_data[i]["pvp"]["damage_dealt"]
                average_wins = round(
                    (today_data[num]["pvp"]["wins"] - beforeday_data[i]["pvp"]["wins"])/battles*100, 2)
                all_win += today_data[num]["pvp"]["wins"] - \
                    beforeday_data[i]["pvp"]["wins"]
                average_frag = round(
                    (today_data[num]["pvp"]["frags"] - beforeday_data[i]["pvp"]["frags"])/battles, 2)
                all_frag += today_data[num]["pvp"]["frags"] - \
                    beforeday_data[i]["pvp"]["frags"]
                average_xp = int(
                    (today_data[num]["pvp"]["xp"] - beforeday_data[i]["pvp"]["xp"])/battles)
                all_xp += today_data[num]["pvp"]["xp"] - \
                    beforeday_data[i]["pvp"]["xp"]
                if (today_data[num]["pvp"]["main_battery"]["shots"]-beforeday_data[i]["pvp"]["main_battery"]["shots"]) == 0:
                    average_hitrate = 0.0
                else:
                    average_hitrate = round((today_data[num]["pvp"]["main_battery"]["hits"]-beforeday_data[i]["pvp"]["main_battery"]["hits"])/(
                        today_data[num]["pvp"]["main_battery"]["shots"]-beforeday_data[i]["pvp"]["main_battery"]["shots"])*100, 2)

                ship_id = today_data[num]["ship_id"]
            pr_value, n_damage, n_frag = tool.get_pvp_pr(
                average_damage_dealt, average_wins, average_frag, ship_id)
            damage_box = tool.get_damage_box(n_damage)
            frag_box = tool.get_frag_box(n_frag)
            all_n_damage += n_damage*battles
            all_n_frag += n_frag*battles
            all_pr += pr_value*battles
            num += 1
            PR = tool.get_pr_box(pr_value)[0]
            pr_box = tool.get_pr_box(pr_value)[1]
            shipinfo_path = tool.get_data_path('shipinfo')
            ship_info_data = open(shipinfo_path, "r", encoding='utf-8')
            shipinfodata = json.load(ship_info_data)
            ship_info_data.close()
            key = shipinfodata[str(ship_id)]['name']
            tier = shipinfodata[str(ship_id)]['tier']
            x_coord = 128-int(tool.get_x_coord(key, font))
            draw.text((x_coord+2, y_coord+2), key, (0, 0, 0), font=font)

            x_coord = 305-int(tool.get_x_coord(str(tier), font)/2)
            draw.text((x_coord+2, y_coord+2), str(tier), (0, 0, 0), font=font)

            x_coord = 390-int(tool.get_x_coord(str(battles), font))
            draw.text((x_coord+2, y_coord+2),
                      str(battles), (0, 0, 0), font=font)

            x_coord = 670-int(tool.get_x_coord(str(average_xp), font))
            draw.text((x_coord+2, y_coord+2),
                      str(average_xp), (0, 0, 0), font=font)
            average_hitrate = str(average_hitrate)+"%"
            x_coord = 1050-int(tool.get_x_coord(average_hitrate, font))
            draw.text((x_coord+2, y_coord+2), average_hitrate,
                      (0, 0, 0), font=font)
            outpr = PR+"("+str(int(pr_value))+")"
            x_coord = 520-int(tool.get_x_coord(outpr, font))
            draw.text((x_coord, y_coord), outpr, pr_box, font=font)

            win_box = tool.get_win_box(average_wins)
            out_wins = str(average_wins)+"%"
            x_coord = 762-int(tool.get_x_coord(out_wins, font))
            draw.text((x_coord, y_coord), out_wins, win_box, font=font)

            x_coord = 875 - \
                int(tool.get_x_coord(str(average_damage_dealt), font))
            draw.text((x_coord+1, y_coord+1), str(average_damage_dealt),
                      damage_box, font=font)

            x_coord = 960-int(tool.get_x_coord(str(average_frag), font))
            draw.text((x_coord+2, y_coord+2), str(average_frag),
                      frag_box, font=font)
            y_coord += 40

        if all_battle == 0:
            return('0x203', '该日期范围内没有数据')
        all_average_frag = round(all_frag/all_battle, 2)
        all_average_damage_dealt = int(all_damage_dealt/all_battle)
        all_average_xp = int(all_xp/all_battle)
        all_average_pr = int(all_pr/all_battle)
        all_average_win = round(all_win/all_battle*100, 2)
        all_average_n_damage = float(all_n_damage/all_battle)
        all_average_n_frag = float(all_n_frag/all_battle)
        all_damage_box = tool.get_damage_box(all_average_n_damage)
        all_frag_box = tool.get_frag_box(all_average_n_frag)
        account_name, clan_name = tool.get_user_name(account_id, server)

        x_coord = 318 - tool.get_x_coord(str(all_battle), font2)
        draw.text((x_coord+2, 230+2), str(all_battle), (0, 0, 0), font=font2)
        all_wins_box = tool.get_win_box(all_average_win)
        all_average_win = str(all_average_win) + "%"
        x_coord = 545 - tool.get_x_coord(all_average_win, font2)
        draw.text((x_coord+2, 230+2), all_average_win,
                  all_wins_box, font=font2)
        x_coord = 800 - \
            tool.get_x_coord(str(all_average_damage_dealt), font2)
        draw.text((x_coord+2, 230+2), str(all_average_damage_dealt),
                  all_damage_box, font=font2)
        x_coord = 438 - tool.get_x_coord(str(all_average_xp), font2)
        draw.text((x_coord+2, 315+2), str(all_average_xp),
                  (0, 0, 0), font=font2)
        x_coord = 668 - tool.get_x_coord(str(all_average_frag), font2)
        draw.text((x_coord+2, 315+2), str(all_average_frag),
                  all_frag_box, font=font2)
        all_PR = tool.get_pr_box(all_average_pr)[0]
        all_pr_box = tool.get_pr_box(all_average_pr)[1]
        a = ImageDraw.ImageDraw(img)
        a.rectangle(((104, 103), (1017, 167)), fill=all_pr_box, outline=None)
        out_pr = all_PR + "("+str(all_average_pr)+")"
        x_coord = 545-tool.get_x_coord(out_pr, font2)
        draw.text((x_coord, 107), out_pr, (255, 255, 255), font=font2)
        user_name = "["+str(clan_name)+"]"+str(account_name)
        x_coord = 560-tool.get_x_coord(user_name, font3)
        draw.text((x_coord, 20), user_name, (0, 0, 0), font=font3)
        x_coord = 545 - \
            tool.get_x_coord("CORAL(ASIA)©MaoYu", font)
        draw.text((x_coord, y_coord+45), "CORAL(ASIA)©MaoYu",
                  (0, 0, 0), font=font)
        img = img.crop((0, 0, 1120, (y_coord+90)))
        out_path = os.path.dirname(__file__)+'/temp/user.png'
        datetime = str(time.time())
        out_path = out_path.replace('user', datetime)
        if os.path.exists(out_path):
            os.remove(out_path)
        img.save(out_path)
        return ('success', out_path)
    except Exception as e:
        return ('error', str(e))


def rankrecent(account_id: int, server: str, info_date: int):
    try:
        sys.path.append(os.path.dirname(
            __file__).replace('pic/kokomi', 'function'))
        import tool
        today = date.today().strftime("%Y-%m-%d")
        beforeday = (date.today() + timedelta(days=-info_date)
                     ).strftime("%Y-%m-%d")
        recent_path = os.path.dirname(__file__).replace(
            'pic/kokomi', 'recent')+'/'+server+'/'+str(account_id) + '/date.json'
        today_path = recent_path.replace('user_qqid', str(
            account_id)).replace('date', today)
        beforeday_path = recent_path.replace('user_qqid', str(
            account_id)).replace('date', beforeday)

        if os.path.exists(today_path) == False:
            return('0x201', '数据丢失，请联系作者处理')
        if os.path.exists(beforeday_path) == False:
            return('0x202', '输入的时间过长，查询不到数据')
        today_data = open(today_path, "r", encoding="utf-8")
        todaydata = json.load(today_data)
        today_data.close()
        beforeday_data = open(beforeday_path, "r", encoding="utf-8")
        beforedaydata = json.load(beforeday_data)
        beforeday_data.close()

        if todaydata["meta"]["count"] == 0 or beforedaydata["meta"]["count"] == 0:
            return ('0x204', '没有数据请检查是否隐藏战绩')
        today_data = todaydata["data"][str(account_id)]
        beforeday_data = beforedaydata["data"][str(account_id)]
        today_len = len(today_data)
        beforeday_len = len(beforeday_data)

        y_coord = 455
        img = Image.open(os.path.dirname(__file__)+'/rankrecent.png')
        draw = ImageDraw.Draw(img)
        font = tool.get_font(2, 27)
        font2 = tool.get_font(2, 40)
        font3 = tool.get_font(3, 40)

        all_battle = 0
        all_frag = 0
        all_damage_dealt = 0
        all_xp = 0
        all_pr = 0
        all_win = 0
        all_n_damage = 0
        all_n_frag = 0
        num = 0
        while num < today_len:
            i = 0
            new_battle = True
            while i < beforeday_len:
                today_ship_id = today_data[num]["ship_id"]
                before_ship_id = beforeday_data[i]["ship_id"]
                if today_ship_id == before_ship_id:
                    new_battle = False
                    break
                else:
                    i += 1
            if new_battle == True:
                battles = today_data[num]["rank_solo"]["battles"]
                if battles <= 0:
                    num += 1
                    continue
                all_battle += battles
                average_damage_dealt = int(
                    (today_data[num]["rank_solo"]["damage_dealt"])/battles)
                all_damage_dealt += today_data[num]["rank_solo"]["damage_dealt"]
                average_wins = round(
                    (today_data[num]["rank_solo"]["wins"])/battles*100, 2)
                all_win += today_data[num]["rank_solo"]["wins"]
                average_frag = round(
                    (today_data[num]["rank_solo"]["frags"])/battles, 2)
                all_frag += today_data[num]["rank_solo"]["frags"]
                average_xp = int((today_data[num]["rank_solo"]["xp"])/battles)
                all_xp += today_data[num]["rank_solo"]["xp"]
                if today_data[num]["rank_solo"]["main_battery"]["shots"] == 0:
                    average_hitrate = 0.0
                else:
                    average_hitrate = round((today_data[num]["rank_solo"]["main_battery"]["hits"])/(
                        today_data[num]["rank_solo"]["main_battery"]["shots"]), 2)

                ship_id = today_data[num]["ship_id"]
            else:
                battles = today_data[num]["rank_solo"]["battles"] - \
                    beforeday_data[i]["rank_solo"]["battles"]
                if today_data[num]["rank_solo"]["battles"] == 0 or battles <= 0:
                    num += 1
                    continue
                all_battle += battles
                average_damage_dealt = int(
                    (today_data[num]["rank_solo"]["damage_dealt"] - beforeday_data[i]["rank_solo"]["damage_dealt"])/battles)
                all_damage_dealt += today_data[num]["rank_solo"]["damage_dealt"] - \
                    beforeday_data[i]["rank_solo"]["damage_dealt"]
                average_wins = round(
                    (today_data[num]["rank_solo"]["wins"] - beforeday_data[i]["rank_solo"]["wins"])/battles*100, 2)
                all_win += today_data[num]["rank_solo"]["wins"] - \
                    beforeday_data[i]["rank_solo"]["wins"]
                average_frag = round(
                    (today_data[num]["rank_solo"]["frags"] - beforeday_data[i]["rank_solo"]["frags"])/battles, 2)
                all_frag += today_data[num]["rank_solo"]["frags"] - \
                    beforeday_data[i]["rank_solo"]["frags"]
                average_xp = int(
                    (today_data[num]["rank_solo"]["xp"] - beforeday_data[i]["rank_solo"]["xp"])/battles)
                all_xp += today_data[num]["rank_solo"]["xp"] - \
                    beforeday_data[i]["rank_solo"]["xp"]
                if (today_data[num]["rank_solo"]["main_battery"]["shots"]-beforeday_data[i]["rank_solo"]["main_battery"]["shots"]) == 0:
                    average_hitrate = 0.0
                else:
                    average_hitrate = round((today_data[num]["rank_solo"]["main_battery"]["hits"]-beforeday_data[i]["rank_solo"]["main_battery"]["hits"])/(
                        today_data[num]["rank_solo"]["main_battery"]["shots"]-beforeday_data[i]["rank_solo"]["main_battery"]["shots"])*100, 2)

                ship_id = today_data[num]["ship_id"]

            pr_value, n_damage, n_frag = tool.get_rank_pr(
                average_damage_dealt, average_wins, average_frag, ship_id)
            damage_box = tool.get_damage_box(n_damage)
            frag_box = tool.get_frag_box(n_frag)
            all_n_damage += n_damage*battles
            all_n_frag += n_frag*battles
            all_pr += pr_value*battles
            num += 1
            PR = tool.get_pr_box(pr_value)[0]
            pr_box = tool.get_pr_box(pr_value)[1]
            shipinfo_path = tool.get_data_path('shipinfo')
            ship_info_data = open(shipinfo_path, "r", encoding='utf-8')
            shipinfodata = json.load(ship_info_data)
            ship_info_data.close()
            key = shipinfodata[str(ship_id)]['name']
            tier = shipinfodata[str(ship_id)]['tier']
            x_coord = 128-int(tool.get_x_coord(key, font))
            draw.text((x_coord+2, y_coord+2), key, (0, 0, 0), font=font)

            x_coord = 305-int(tool.get_x_coord(str(tier), font)/2)
            draw.text((x_coord+2, y_coord+2), str(tier), (0, 0, 0), font=font)

            x_coord = 390-int(tool.get_x_coord(str(battles), font))
            draw.text((x_coord+2, y_coord+2),
                      str(battles), (0, 0, 0), font=font)

            x_coord = 670-int(tool.get_x_coord(str(average_xp), font))
            draw.text((x_coord+2, y_coord+2),
                      str(average_xp), (0, 0, 0), font=font)
            average_hitrate = str(average_hitrate)+"%"
            x_coord = 1050-int(tool.get_x_coord(average_hitrate, font))
            draw.text((x_coord+2, y_coord+2), average_hitrate,
                      (0, 0, 0), font=font)
            outpr = PR+"("+str(int(pr_value))+")"
            x_coord = 520-int(tool.get_x_coord(outpr, font))
            draw.text((x_coord, y_coord), outpr, pr_box, font=font)

            win_box = tool.get_win_box(average_wins)
            out_wins = str(average_wins)+"%"
            x_coord = 762-int(tool.get_x_coord(out_wins, font))
            draw.text((x_coord, y_coord), out_wins, win_box, font=font)

            x_coord = 875 - \
                int(tool.get_x_coord(str(average_damage_dealt), font))
            draw.text((x_coord+1, y_coord+1), str(average_damage_dealt),
                      damage_box, font=font)

            x_coord = 960-int(tool.get_x_coord(str(average_frag), font))
            draw.text((x_coord+2, y_coord+2), str(average_frag),
                      frag_box, font=font)
            y_coord += 40

        if all_battle == 0:
            return('0x203', '该日期范围内没有数据')
        all_average_frag = round(all_frag/all_battle, 2)
        all_average_damage_dealt = int(all_damage_dealt/all_battle)
        all_average_xp = int(all_xp/all_battle)
        all_average_pr = int(all_pr/all_battle)
        all_average_win = round(all_win/all_battle*100, 2)
        all_average_n_damage = float(all_n_damage/all_battle)
        all_average_n_frag = float(all_n_frag/all_battle)
        all_damage_box = tool.get_damage_box(all_average_n_damage)
        all_frag_box = tool.get_frag_box(all_average_n_frag)
        account_name, clan_name = tool.get_user_name(account_id, server)

        x_coord = 318 - tool.get_x_coord(str(all_battle), font2)
        draw.text((x_coord+2, 230+2), str(all_battle), (0, 0, 0), font=font2)
        all_wins_box = tool.get_win_box(all_average_win)
        all_average_win = str(all_average_win) + "%"
        x_coord = 545 - tool.get_x_coord(all_average_win, font2)
        draw.text((x_coord+2, 230+2), all_average_win,
                  all_wins_box, font=font2)
        x_coord = 800 - \
            tool.get_x_coord(str(all_average_damage_dealt), font2)
        draw.text((x_coord+2, 230+2), str(all_average_damage_dealt),
                  all_damage_box, font=font2)
        x_coord = 438 - tool.get_x_coord(str(all_average_xp), font2)
        draw.text((x_coord+2, 315+2), str(all_average_xp),
                  (0, 0, 0), font=font2)
        x_coord = 668 - tool.get_x_coord(str(all_average_frag), font2)
        draw.text((x_coord+2, 315+2), str(all_average_frag),
                  all_frag_box, font=font2)
        all_PR = tool.get_pr_box(all_average_pr)[0]
        all_pr_box = tool.get_pr_box(all_average_pr)[1]
        a = ImageDraw.ImageDraw(img)
        a.rectangle(((104, 103), (1017, 167)), fill=all_pr_box, outline=None)
        out_pr = all_PR + "("+str(all_average_pr)+")"
        x_coord = 545-tool.get_x_coord(out_pr, font2)
        draw.text((x_coord, 107), out_pr, (255, 255, 255), font=font2)
        user_name = "["+str(clan_name)+"]"+str(account_name)
        x_coord = 560-tool.get_x_coord(user_name, font3)
        draw.text((x_coord, 20), user_name, (0, 0, 0), font=font3)
        x_coord = 545 - \
            tool.get_x_coord("CORAL(ASIA)©MaoYu", font)
        draw.text((x_coord, y_coord+45), "CORAL(ASIA)©MaoYu",
                  (0, 0, 0), font=font)
        img = img.crop((0, 0, 1120, (y_coord+90)))
        out_path = os.path.dirname(__file__)+'/temp/user.png'
        datetime = str(time.time())
        out_path = out_path.replace('user', datetime)
        if os.path.exists(out_path):
            os.remove(out_path)
        img.save(out_path)
        return ('success', out_path)
    except Exception as e:
        return ('error', str(e))
