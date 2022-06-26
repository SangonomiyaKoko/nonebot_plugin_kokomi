import os
import sqlite3
from PIL import ImageFont
import json
import requests


def get_data_path(file_name: str):
    shipdata_path = os.path.dirname(
        __file__).replace('function', '')+'shipdata/' + file_name + '.json'
    return shipdata_path


def get_recent_path(account_id: str, date: str, server: str):
    recentdata_path = os.path.dirname(
        __file__).replace('function', '')+'recent/'+server+'/'+account_id+'/'+date+'.json'
    return recentdata_path


def get_sqlit3_path():
    shipdata_path = os.path.dirname(__file__).replace(
        'function', '')+'shipdata/userid.db'
    return shipdata_path


def get_accid_path():
    shipdata_path = os.path.dirname(__file__).replace(
        'function', '')+'shipdata/accountid.db'
    return shipdata_path


def get_pic_name(pic_type: int):
    pic_type_dict = {
        1: 'kokomi'
    }
    if pic_type not in pic_type_dict:
        return ('error', '没有找到指定图片样式')
    return ('success', pic_type_dict[pic_type])


def get_account_id(user_qqid: str):
    conn = sqlite3.connect(get_sqlit3_path())
    c = conn.cursor()
    cursor = c.execute(
        "SELECT QQID,ACCID,TYPE,LANGUAGE,TIME,SERVER,EXTER1,EXTER2  from userid")
    account_id = 0
    row_list = list(cursor)
    conn.close()
    for row in row_list:
        userqqid = row[0]
        accountid = row[1]
        if userqqid == int(user_qqid):
            pic_type = row[2]
            server = row[5]
            return (accountid, server, pic_type)
    if account_id == 0:
        return (0, '0', '0')


def get_win_box(average_wins: float):
    if average_wins >= 70:
        color_box = (160, 13, 197)
    elif average_wins >= 65 and average_wins < 70:
        color_box = (208, 66, 243)
    elif average_wins >= 60 and average_wins < 65:
        color_box = (2, 201, 179)
    elif average_wins >= 56 and average_wins < 60:
        color_box = (49, 128, 0)
    elif average_wins >= 52 and average_wins < 56:
        color_box = (68, 179, 0)
    elif average_wins >= 49 and average_wins < 52:
        color_box = (255, 199, 31)
    elif average_wins >= 43 and average_wins < 49:
        color_box = (254, 121, 3)
    elif average_wins < 43:
        color_box = (254, 14, 0)
    return color_box


def get_damage_box(num: float):
    if num >= 1.5:
        color_box = (160, 13, 197)
    elif num >= 1.35 and num < 1.5:
        color_box = (208, 66, 243)
    elif num >= 1.2 and num < 1.35:
        color_box = (2, 201, 179)
    elif num >= 1.1 and num < 1.2:
        color_box = (49, 128, 0)
    elif num >= 1.0 and num < 1.1:
        color_box = (68, 179, 0)
    elif num >= 0.95 and num < 1.0:
        color_box = (255, 199, 31)
    elif num >= 0.8 and num < 0.95:
        color_box = (254, 121, 3)
    elif num < 0.8:
        color_box = (254, 14, 0)
    return color_box


def get_pr_box(pr: int):
    if pr == -1:
        PR = "水平未知"
        box = (96, 125, 139)
        diff = 0
    elif pr >= 0 and pr < 750:
        PR = "还需努力"
        box = (254, 14, 0)
        diff = int(750-pr)
    elif pr >= 750 and pr < 1100:
        PR = "低于平均"
        box = (230, 166, 48)
        diff = int(1100-pr)
    elif pr >= 1100 and pr < 1350:
        PR = "平均水平"
        box = (255, 199, 31)
        diff = int(1350-pr)
    elif pr >= 1350 and pr < 1550:
        PR = "好"
        box = (68, 179, 0)
        diff = int(1550-pr)
    elif pr >= 1550 and pr < 1750:
        PR = "很好"
        box = (49, 128, 0)
        diff = int(1750-pr)
    elif pr >= 1750 and pr < 2100:
        PR = "非常好"
        box = (2, 201, 179)
        diff = int(2100-pr)
    elif pr >= 2100 and pr < 2450:
        PR = "大佬平均"
        box = (208, 66, 243)
        diff = int(2450-pr)
    elif pr >= 2450:
        PR = "神佬平均"
        box = (160, 13, 197)
        diff = int(pr-2450)
    return (PR, box, diff)


def get_frag_box(num: float):
    if num >= 2:
        color_box = (160, 13, 197)
    elif num >= 1.5 and num < 2:
        color_box = (208, 66, 243)
    elif num >= 1.3 and num < 1.5:
        color_box = (2, 201, 179)
    elif num >= 1.0 and num < 1.3:
        color_box = (49, 128, 0)
    elif num >= 0.6 and num < 1.0:
        color_box = (68, 179, 0)
    elif num >= 0.3 and num < 0.6:
        color_box = (255, 199, 31)
    elif num >= 0.2 and num < 0.3:
        color_box = (254, 121, 3)
    elif num < 0.2:
        color_box = (254, 14, 0)
    return color_box


def get_plane_box(plane_kill: float):
    if plane_kill >= 7:
        color_box = (160, 13, 197)
    elif plane_kill >= 6 and plane_kill < 7:
        color_box = (208, 66, 243)
    elif plane_kill >= 5 and plane_kill < 6:
        color_box = (2, 201, 179)
    elif plane_kill >= 4 and plane_kill < 5:
        color_box = (49, 128, 0)
    elif plane_kill >= 3 and plane_kill < 4:
        color_box = (68, 179, 0)
    elif plane_kill >= 2 and plane_kill < 3:
        color_box = (255, 199, 31)
    elif plane_kill >= 1 and plane_kill < 2:
        color_box = (254, 121, 3)
    elif plane_kill < 1:
        color_box = (254, 14, 0)
    return color_box

def get_x_coord(in_str: str, font: ImageFont.FreeTypeFont):
    x = font.getsize(in_str)[0]
    out_coord = x/2
    return out_coord


def get_pvp_pr(average_damage_dealt: float, average_wins: float, average_kd: float, ship_id: int):
    shipdata_path = get_data_path('serverdata')
    ship_server_data = open(shipdata_path, "r", encoding="utf-8")
    userserverdata = json.load(ship_server_data)
    if userserverdata['data'][str(ship_id)] == []:
        return (-1, -1, -1)
    server_damage_dealt = userserverdata['data'][str(
        ship_id)]['average_damage_dealt']
    server_frags = userserverdata['data'][str(ship_id)]['average_frags']
    server_wins = userserverdata['data'][str(ship_id)]['win_rate']
    ship_server_data.close()
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
    return (pr, n_damage, n_kd)


def get_rank_pr(average_damage_dealt: float, average_wins: float, average_kd: float, ship_id: int):
    shipdata_path = get_data_path('serverdata')
    ship_server_data = open(shipdata_path, "r", encoding="utf-8")
    userserverdata = json.load(ship_server_data)
    if userserverdata['data'][str(ship_id)] == []:
        return (-1, -1, -1)
    server_damage_dealt = userserverdata['data'][str(
        ship_id)]['average_damage_dealt']
    server_frags = userserverdata['data'][str(ship_id)]['average_frags']
    server_wins = userserverdata['data'][str(ship_id)]['win_rate']
    ship_server_data.close()
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
    pr = 600*n_damage+350*n_kd+400*n_win_rate
    return (pr, n_damage, n_kd)


def get_ship_id(ship_name: str):
    shipid_path = get_data_path('shipid')
    ship_id_data = open(shipid_path, "r", encoding="utf-8")
    shipdata = json.load(ship_id_data)
    if ship_name not in shipdata:
        return -1
    else:
        return shipdata[ship_name]


def get_user_name(account_id: int, server: str):
    application_id = get_application_id()
    if len(application_id) != 32:
        return('error', '缺少application_id，请先配置application_id')
    clan_id_url = 'http://api.worldofwarships.server/wows/clans/accountinfo/?application_id=applicationid&account_id=accountid'
    clanid_url = clan_id_url.replace('applicationid', str(application_id)).replace(
        'accountid', str(account_id)).replace('server', server)
    try:
        clan_id_original_data = requests.get(url=clanid_url)
    except:
        return('error', '请求数据失败，请检查网络')
    clan_id_processed_data = json.loads(clan_id_original_data.text)
    clan_id_original_data.close()
    if clan_id_processed_data["data"][str(account_id)] != None:
        clan_id = clan_id_processed_data["data"][str(account_id)]["clan_id"]
        account_name = clan_id_processed_data["data"][str(
            account_id)]["account_name"]
        if clan_id == None:
            clan_name = ""
        elif clan_id == "":
            clan_name = ""
        else:
            clan_name_url = 'http://api.worldofwarships.server/wows/clans/info/?application_id=applicationid&clan_id=clanid'
            clanname_url = clan_name_url.replace('clanid', str(clan_id)).replace(
                'applicationid', str(application_id)).replace('server', server)
            try:
                clan_name_original_data = requests.get(url=clanname_url)
            except:
                return('error', '请求数据失败，请检查网络')
            clan_name_processed_data = json.loads(clan_name_original_data.text)
            clan_name_original_data.close()
            if clan_name_processed_data["status"] == "error":
                clan_name = ""
            else:
                clan_name = clan_name_processed_data["data"][str(
                    clan_id)]["tag"]
    else:
        account_name_url = 'https://api.worldofwarships.server/wows/account/info/?application_id=applicationid&account_id=accountid'
        account_name_url = account_name_url.replace('accountid', str(account_id)).replace(
            'applicationid', str(application_id)).replace('server', server)
        try:
            clan_id_original_data = requests.get(url=account_name_url)
        except:
            return ('error', '请求数据失败，请检查网络')
        clan_id_processed_data = json.loads(clan_id_original_data.text)
        clan_id_original_data.close()
        account_name = clan_id_processed_data["data"][str(
            account_id)]["nickname"]
        clan_name = ''

    return (account_name, clan_name)


def get_application_id():
    user_config_data = json.load(open(os.path.dirname(
        __file__)+'/config.json', "r", encoding="utf-8"))
    application_id = user_config_data['application_id']
    return application_id


def get_font(font_num: int, font_size: int):
    if font_num == 1:
        font_path = '/usr/share/fonts/NZBZ.ttf'
    elif font_num == 2:
        font_path = '/usr/share/fonts/STZHONGS.TTF'
    else:
        font_path = '/usr/share/fonts/ARLRDBD.TTF'
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        return 'error'
    return font
