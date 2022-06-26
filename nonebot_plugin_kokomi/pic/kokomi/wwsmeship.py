
import requests
import json
import time
import os
from PIL import ImageFont, Image, ImageDraw
import sys


def wws_me_ship(account_id: int, server: str, ship_name: str):
    # 导入所需字体
    sys.path.append(os.path.dirname(
        __file__).replace('pic/kokomi', 'function'))
    import tool
    font = tool.get_font(1, 60)
    if type(font) == str:
        return ('0x112', '加载字体数据失败')
    font5 = tool.get_font(1, 40)
    font2 = tool.get_font(1, 210)
    font3 = tool.get_font(3, 100)
    font4 = tool.get_font(2, 90)
    font6 = tool.get_font(2, 60)
    # 查询ship_id
    ship_id = tool.get_ship_id(ship_name=ship_name)
    if ship_id == -1:
        return ('0x102', '查询不到您输入的船名，发送 {添加船只别名 [别名] [标准名称]}可以为船只添加别名')
    # 导入服务器数据
    shipdata_path = tool.get_data_path('serverdata')
    ship_server_data = open(shipdata_path, "r", encoding="utf-8")
    userserverdata = json.load(ship_server_data)
    ship_server_data.close()
    # 服务器数据
    if str(ship_id) not in userserverdata["data"]:
        return ('0x103', '没有该船')
    if userserverdata["data"][str(ship_id)] == []:
        return ('0x104', '没有该船的服务器数据')
    server_wins = float(userserverdata["data"][str(ship_id)]["win_rate"])
    server_frags = float(
        userserverdata["data"][str(ship_id)]["average_frags"])
    server_damage_dealt = int(
        userserverdata["data"][str(ship_id)]["average_damage_dealt"])
    # 调用api,获取数据
    application_id = tool.get_application_id()
    url_example = 'http://api.worldofwarships.server/wows/ships/stats/?application_id=applicationid&ship_id=shipid&account_id=accountid'
    url = url_example.replace('applicationid', application_id).replace('shipid', str(
        ship_id)).replace('accountid', str(account_id)).replace('server', server)
    try:
        original_data = requests.get(url=url)
        processed_data = json.loads(original_data.text)
        original_data.close()
        # 单野
        solo_data = requests.get(url=url + '&extra=pvp_solo')
        solodata = json.loads(solo_data.text)
        solo_data.close()
        # 双排
        div2_data = requests.get(url=url + '&extra=pvp_div2')
        div2data = json.loads(div2_data.text)
        div2_data.close()
        # 三排
        div3_data = requests.get(url=url + '&extra=pvp_div3')
        div3data = json.loads(div3_data.text)
        div3_data.close()
    except:
        return ('0x105', '请求数据失败，请检查网络')
    # 判断是否成功获得数据
    if processed_data["status"] == "error":
        request_error_message = "请求数据失败，错误代码\nERROR: " + \
            processed_data["error"]["message"]
        return ('1x106', request_error_message)
    if processed_data["meta"]["count"] == 0:
        return('0x107', 'api数据接口没有返回数据，请检查是否隐藏战绩')
    if processed_data["data"][str(account_id)] == None:
        return ('0x108', '您在该船只上没有战斗数据')
    if processed_data["data"][str(account_id)][0]["battles"] == 0:
        return ('0x109', '您在该船只上没有战斗数据')
    # 提取数据
    try:
        pvp_data = processed_data["data"][str(account_id)][0]["pvp"]
        pvpsolo_data = solodata["data"][str(account_id)][0]["pvp_solo"]
        pvpdiv2_data = div2data["data"][str(account_id)][0]["pvp_div2"]
        pvpdiv3_data = div3data["data"][str(account_id)][0]["pvp_div3"]
    except:
        return ('0x110', '提取数据时发生错误')

    solo_battles = pvpsolo_data["battles"]
    if solo_battles == 0:
        solo_average_xp = 0
        solo_average_wins = 0
        solo_average_frags = 0
        solo_average_damage_dealt = 0
        solo_pr = -1
    else:
        solo_wins = pvpsolo_data["wins"]
        solo_damage_dealts = pvpsolo_data["damage_dealt"]
        solo_xp = pvpsolo_data["xp"]
        solo_frags = pvpsolo_data["frags"]
        solo_average_xp = int(solo_xp/solo_battles)
        solo_average_wins = round(solo_wins/solo_battles*100, 2)
        solo_average_frags = round(solo_frags/solo_battles, 2)
        solo_average_damage_dealt = int(solo_damage_dealts/solo_battles)
        solo_pr = tool.get_pvp_pr(
            solo_average_damage_dealt, solo_average_wins, solo_average_frags, ship_id)[0]

    div2_battles = pvpdiv2_data["battles"]
    if div2_battles == 0:
        div2_average_xp = 0
        div2_average_wins = 0
        div2_average_frags = 0
        div2_average_damage_dealt = 0
        div2_pr = -1
    else:
        div2_wins = pvpdiv2_data["wins"]
        div2_damage_dealts = pvpdiv2_data["damage_dealt"]
        div2_xp = pvpdiv2_data["xp"]
        div2_frags = pvpdiv2_data["frags"]
        div2_average_xp = int(div2_xp/div2_battles)
        div2_average_wins = round(div2_wins/div2_battles*100, 2)
        div2_average_frags = round(div2_frags/div2_battles, 2)
        div2_average_damage_dealt = int(div2_damage_dealts/div2_battles)
        div2_pr = tool.get_pvp_pr(div2_average_damage_dealt, div2_average_wins,
                                  div2_average_frags, ship_id)[0]

    div3_battles = pvpdiv3_data["battles"]
    if div3_battles == 0:
        div3_average_xp = 0
        div3_average_wins = 0
        div3_average_frags = 0
        div3_average_damage_dealt = 0
        div3_pr = -1
    else:
        div3_wins = pvpdiv3_data["wins"]
        div3_damage_dealts = pvpdiv3_data["damage_dealt"]
        div3_xp = pvpdiv3_data["xp"]
        div3_frags = pvpdiv3_data["frags"]
        div3_average_xp = int(div3_xp/div3_battles)
        div3_average_wins = round(div3_wins/div3_battles*100, 2)
        div3_average_frags = round(div3_frags/div3_battles, 2)
        div3_average_damage_dealt = int(div3_damage_dealts/div3_battles)
        div3_pr = tool.get_pvp_pr(div3_average_damage_dealt, div3_average_wins,
                                  div3_average_frags, ship_id)[0]
    # 场均数据
    xp = pvp_data["xp"]
    wins = pvp_data["wins"]
    battles = pvp_data["battles"]
    survived_battles = pvp_data["survived_battles"]
    frags = pvp_data["frags"]
    damage_scouting = pvp_data["damage_scouting"]
    art_agro = pvp_data["art_agro"]
    damage_dealt = pvp_data["damage_dealt"]
    planes_killed = pvp_data["planes_killed"]
    if battles == 0:
        return ('0x109', '您在该船只上没有战斗数据')
    # 主炮数据
    main_battery_data = processed_data["data"][str(
        account_id)][0]["pvp"]["main_battery"]

    main_battery_max_frags_battle = main_battery_data["max_frags_battle"]
    main_battery_hits = main_battery_data["hits"]
    main_battery_shots = main_battery_data["shots"]
    # 副炮数据
    second_battery_data = processed_data["data"][str(
        account_id)][0]["pvp"]["second_battery"]

    second_battery_max_frags_battle = second_battery_data["max_frags_battle"]
    # 鱼雷数据
    torpedoes_data = processed_data["data"][str(
        account_id)][0]["pvp"]["torpedoes"]

    torpedoes_max_frags_battle = torpedoes_data["max_frags_battle"]
    # 最高场均数据
    max_damage_scouting = pvp_data["max_damage_scouting"]
    max_xp = pvp_data["max_xp"]
    max_damage_dealt = pvp_data["max_damage_dealt"]
    max_ships_spotted = pvp_data["max_ships_spotted"]
    max_frags_battle = pvp_data["max_frags_battle"]
    max_planes_killed = pvp_data["max_planes_killed"]
    max_total_agro = pvp_data["max_total_agro"]
    # 其他数据
    last_battle_time = processed_data["data"][str(
        account_id)][0]["last_battle_time"]

    # 数据计算
    average_xp = int(xp/battles)
    average_wins = round(wins/battles*100, 2)
    average_survived_battles = round(survived_battles/battles*100, 2)
    average_kd = round(frags/battles, 2)
    average_frags = average_kd
    average_damage_scouting = int(damage_scouting/battles)
    average_art_agro = int(art_agro/battles)
    average_damage_dealt = int(damage_dealt/battles)
    average_planes_killed = round(planes_killed/battles, 2)

    if main_battery_shots == 0:
        average_main_battery_hits = 0.00
    else:
        average_main_battery_hits = round(
            main_battery_hits/main_battery_shots*100, 2)

    # 使用PIL进行生成图片
    # 1.场均数据
    img = Image.open(os.path.dirname(__file__)+'/wwsmeship.png')
    draw = ImageDraw.Draw(img)

    color_box = tool.get_win_box(average_wins)
    out_average_wins = str(average_wins)+"%"
    winscoord = 783-tool.get_x_coord(out_average_wins, font)*2
    draw.text((winscoord, 800), out_average_wins, color_box, font=font)

    color_box = tool.get_damage_box(
        average_damage_dealt/server_damage_dealt)
    out_damage_dealt = str(average_damage_dealt)
    damagecoord = 783-tool.get_x_coord(out_damage_dealt, font)*2
    draw.text((damagecoord, 925), out_damage_dealt,
              color_box, font=font)

    out_average_xp = str(average_xp)
    xpcoord = 783-tool.get_x_coord(out_average_xp, font)*2
    draw.text((xpcoord, 1300), out_average_xp, (255, 255, 255), font=font)

    out_average_planes_killed = str(average_planes_killed)
    planeskilledcoord = 783 - \
        tool.get_x_coord(out_average_planes_killed, font)*2
    draw.text((planeskilledcoord, 1175),
              out_average_planes_killed, (255, 255, 255), font=font)

    color_box = tool.get_frag_box(average_frags/server_frags)
    out_average_frags = str(average_frags)
    fragscoord = 783-tool.get_x_coord(out_average_frags, font)*2
    draw.text((fragscoord, 1050), out_average_frags,
              color_box, font=font)

    draw.text((1670, 800), str(battles),
              (255, 255, 255), font=font)

    draw.text((1670, 925), str(average_art_agro),
              (255, 255, 255), font=font)

    draw.text((1670, 1050), str(average_damage_scouting),
              (255, 255, 255), font=font)

    out_average_main_battery_hits = str(average_main_battery_hits) + "%"
    draw.text((1670, 1175), str(out_average_main_battery_hits),
              (255, 255, 255), font=font)

    out_average_survived_battles = str(average_survived_battles) + "%"
    draw.text((1670, 1300), str(out_average_survived_battles),
              (255, 255, 255), font=font)
    # 2.最高数据
    draw.text((650, 1495), str(max_damage_dealt),
              (255, 255, 255), font=font)

    draw.text((650, 1620), str(max_frags_battle),
              (255, 255, 255), font=font)

    draw.text((650, 1745), str(max_planes_killed),
              (255, 255, 255), font=font)

    draw.text((650, 1870), str(max_xp), (255, 255, 255), font=font)

    draw.text((650, 1995), str(max_ships_spotted),
              (255, 255, 255), font=font)

    draw.text((1670, 1495), str(max_damage_scouting),
              (255, 255, 255), font=font)

    draw.text((1670, 1620), str(max_total_agro),
              (255, 255, 255), font=font)

    draw.text((1670, 1745), str(main_battery_max_frags_battle),
              (255, 255, 255), font=font)

    draw.text((1670, 1870), str(second_battery_max_frags_battle),
              (255, 255, 255), font=font)

    draw.text((1670, 1995), str(torpedoes_max_frags_battle),
              (255, 255, 255), font=font)
    # 类别
    # 单野
    draw.text((375, 2295), str(solo_battles), (255, 255, 255), font=font5)

    solo_wins_box = tool.get_win_box(solo_average_wins)
    out_solo_wins = str(solo_average_wins) + '%'
    draw.text((375, 2370), out_solo_wins, solo_wins_box, font=font5)

    solo_damage_box = tool.get_damage_box(
        solo_average_damage_dealt/server_damage_dealt)
    draw.text((375, 2445), str(solo_average_damage_dealt),
              solo_damage_box, font=font5)

    solo_frage_box = tool.get_frag_box(solo_average_frags/server_frags)
    draw.text((375, 2520), str(solo_average_frags),
              solo_frage_box, font=font5)

    draw.text((375, 2595), str(solo_average_xp),
              (255, 255, 255), font=font5)

    person_rate = tool.get_pr_box(solo_pr)[0]
    pr_box = tool.get_pr_box(solo_pr)[1]
    pr_diff = tool.get_pr_box(solo_pr)[2]
    a = ImageDraw.ImageDraw(img)
    a.rectangle(((20, 2190), (704, 2250)), fill=pr_box, outline=None)
    person_rate = person_rate+"(+"+str(pr_diff)+")"
    person_rate_coord = 362-tool.get_x_coord(person_rate, font6)
    draw.text((person_rate_coord, 2177), person_rate, font=font6)
    # 双排
    draw.text((1100, 2295), str(div2_battles), (255, 255, 255), font=font5)

    div2_wins_box = tool.get_win_box(div2_average_wins)
    out_div2_wins = str(div2_average_wins) + '%'
    draw.text((1100, 2370), out_div2_wins, div2_wins_box, font=font5)

    div2_damage_box = tool.get_damage_box(
        div2_average_damage_dealt/server_damage_dealt)
    draw.text((1100, 2445), str(div2_average_damage_dealt),
              div2_damage_box, font=font5)

    div2_frage_box = tool.get_frag_box(div2_average_frags/server_frags)
    draw.text((1100, 2520), str(div2_average_frags),
              div2_frage_box, font=font5)

    draw.text((1100, 2595), str(div2_average_xp),
              (255, 255, 255), font=font5)

    person_rate, pr_box, pr_diff = tool.get_pr_box(div2_pr)
    a = ImageDraw.ImageDraw(img)
    a.rectangle(((746, 2190), (1430, 2250)), fill=pr_box, outline=None)
    person_rate = person_rate+"(+"+str(pr_diff)+")"
    person_rate_coord = 1088-tool.get_x_coord(person_rate, font6)
    draw.text((person_rate_coord, 2177), person_rate, font=font6)
    # 三排
    draw.text((1810, 2295), str(div3_battles), (255, 255, 255), font=font5)

    div3_wins_box = tool.get_win_box(div3_average_wins)
    out_solo_wins = str(div3_average_wins) + '%'
    draw.text((1810, 2370), out_solo_wins, div3_wins_box, font=font5)

    div3_damage_box = tool.get_damage_box(
        div3_average_damage_dealt/server_damage_dealt)
    draw.text((1810, 2445), str(div3_average_damage_dealt),
              div3_damage_box, font=font5)

    div3_frage_box = tool.get_frag_box(div3_average_frags/server_frags)
    draw.text((1810, 2520), str(div3_average_frags),
              div3_frage_box, font=font5)

    draw.text((1810, 2595), str(div3_average_xp),
              (255, 255, 255), font=font5)

    person_rate = tool.get_pr_box(div3_pr)[0]
    pr_box = tool.get_pr_box(div3_pr)[1]
    pr_diff = tool.get_pr_box(div3_pr)[2]
    a = ImageDraw.ImageDraw(img)
    a.rectangle(((1460, 2190), (2144, 2250)), fill=pr_box, outline=None)
    person_rate = person_rate+"(+"+str(pr_diff)+")"
    person_rate_coord = 1802-tool.get_x_coord(person_rate, font6)
    draw.text((person_rate_coord, 2177), person_rate, font=font6)
    # 3.差值计算
    # 3.1.胜率
    if average_wins-server_wins >= 0:
        differ_wins = "[+"+str(round(average_wins-server_wins, 2))+"%]"
        draw.text((800, 800), differ_wins, (114, 186, 63), font=font)
    else:
        differ_wins = "["+str(round(average_wins-server_wins, 2))+"%]"
        draw.text((800, 800), differ_wins, (234, 37, 36), font=font)
    # 3.2.场均
    if average_damage_dealt-server_damage_dealt >= 0:
        differ_damage_dealt = "[+" + \
            str(average_damage_dealt-server_damage_dealt)+"]"
        draw.text((800, 925), differ_damage_dealt,
                  (114, 186, 63), font=font)
    else:
        differ_damage_dealt = "[" + \
            str(average_damage_dealt-server_damage_dealt)+"]"
        draw.text((800, 925), differ_damage_dealt,
                  (234, 37, 36), font=font)
    # 3.5.kd
    if average_frags == -1:
        differ_kd = "[+"+str(server_frags)+"]"
        draw.text((800, 1050), differ_kd, (114, 186, 63), font=font)
    else:
        if average_kd-server_frags >= 0:
            differ_kd = "[+"+str(round(average_kd-server_frags, 2))+"]"
            draw.text((800, 1050), differ_kd, (114, 186, 63), font=font)
        else:
            differ_kd = "["+str(round(average_kd-server_frags, 2))+"]"
            draw.text((800, 1050), differ_kd, (234, 37, 36), font=font)
    # 4 其他
    timeArray = time.localtime(last_battle_time)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    draw.text((953, 530), otherStyleTime, (255, 255, 255), font=font)

    shipname_coord = 1080-tool.get_x_coord(ship_name, font2)
    draw.text((shipname_coord+10, 308), ship_name, (0, 0, 0), font=font2)
    draw.text((shipname_coord, 298), ship_name,
              (255, 255, 255), font=font2)
    account_name, clan_name = tool.get_user_name(
        account_id=account_id, server=server)
    if account_name == 'error':
        return ('0x111', clan_name)
    user_name = "["+str(clan_name)+"]"+str(account_name)
    user_name_coord = 1080-tool.get_x_coord(user_name, font3)
    draw.text((user_name_coord, 141), user_name,
              (255, 255, 255), font=font3)

    # pr计算
    if average_damage_dealt > server_damage_dealt*0.4:
        n_damage = (average_damage_dealt-server_damage_dealt *
                    0.4)/(server_damage_dealt*0.6)
    else:
        n_damage = 0
    if average_wins > server_wins*0.7:
        n_win_rate = (average_wins-server_wins*0.7) / \
            (server_wins*0.3)
    else:
        n_win_rate = 0
    if average_kd > server_frags*0.1:
        n_kd = (average_kd-server_frags*0.1)/(server_frags*0.9)
    else:
        n_kd = 0
    pr = 700*n_damage+300*n_kd+150*n_win_rate
    person_rate = tool.get_pr_box(pr)[0]
    pr_box = tool.get_pr_box(pr)[1]
    pr_diff = tool.get_pr_box(pr)[2]
    person_rate = person_rate+"(+"+str(pr_diff)+")"
    all_pr_box = ImageDraw.ImageDraw(img)
    all_pr_box.rectangle(((83, 633), (2076, 733)),
                         fill=pr_box, outline=None)
    person_rate_coord = 1080-tool.get_x_coord(person_rate, font4)
    draw.text((person_rate_coord, 623), person_rate, font=font4)

    out_path = os.path.dirname(__file__)+'/temp/user.png'
    datetime = str(time.time())
    out_path = out_path.replace('user', datetime)
    if os.path.exists(out_path):
        os.remove(out_path)
    img = img.resize((1100, 1400))
    img.save(out_path)
    return ('success', out_path)
