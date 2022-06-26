
import requests
import json
import time
import traceback
from datetime import date, timedelta
import os
from PIL import ImageFont, Image, ImageDraw
import sys
import collections
# 数据响应模块


def wws_me_all(account_id: int, info_msg: str, server: str):
    try:
        info_list = info_msg.replace('wws me ', '').upper().split()
        info_len = len(info_list)
        info_tier = 'all'
        info_type = 'all'
        info_nation = 'all'
        tier_dict = {
            'T11': 11,
            'T10': 10,
            'T9': 9,
            'T8': 8,
            'T7': 7,
            'T6': 6,
            'T5': 5,
            'T4': 4,
            'T3': 3,
            'T2': 2,
            'T1': 1,
            '11': 11,
            '10': 10,
            '9': 9,
            '8': 8,
            '7': 7,
            '6': 6,
            '5': 5,
            '4': 4,
            '3': 3,
            '2': 2,
            '1': 1,
            'XI': 11,
            'X': 10,
            'IX': 9,
            'VIII': 8,
            'VII': 7,
            'VI': 6,
            'V': 5,
            'IV': 4,
            'III': 3,
            'II': 2,
            'I': 1
        }
        type_dict = {
            'CV': 'AirCarrier',
            'BB': 'Battleship',
            'CA': 'Cruiser',
            'DD': 'Destroyer',
            '航母': 'AirCarrier',
            '战列': 'Battleship',
            '巡洋': 'Cruiser',
            '驱逐': 'Destroyer'
        }
        nation_dict = {
            'USA': 'usa',
            'M': 'usa',
            '美国': 'usa',
            '美系': 'usa',
            'M系': 'usa',
            'JAPAN': 'japan',
            'R': 'japan',
            '日本': 'japan',
            'R系': 'japan',
            '日系': 'japan',
            'EUROPE': 'europe',
            'E': 'europe',
            '欧洲': 'europe',
            'E系': 'europe',
            'FRANCE': 'france',
            'F': 'france',
            'F系': 'france',
            '法国': 'france',
            'GERMANY': 'germany',
            'D': 'germany',
            'D系': 'germany',
            '德国': 'germany',
            'UK': 'uk',
            'Y': 'uk',
            'Y系': 'uk',
            '英国': 'uk',
            'PANASIA': 'pan_asia',
            'C': 'pan_asia',
            'C系': 'pan_asia',
            '泛亚': 'pan_asia',
            'USSR': 'ussr',
            'S': 'ussr',
            'S系': 'ussr',
            '苏联': 'ussr',
            'ITALY': 'italy',
            'I': 'italy',
            'I系': 'italy',
            '意大利': 'italy',
            'NETHERLANDS': 'netherlands',
            'HL': 'netherlands',
            'HL系': 'netherlands',
            '荷兰': 'netherlands',
            'PANAMERICA': 'pan_america',
            'FM': 'pan_america',
            'FM系': 'pan_america',
            '泛美': 'pan_america',
            'COMMONWEALTH': 'commonwealth',
            'CW': 'commonwealth',
            'CW系': 'commonwealth',
            '泛英': 'commonwealth',
            '英联邦': 'commonwealth',
            'SPAIN': 'spain',
            'X': 'spain',
            'X系': 'spain',
            '西班牙': 'spain'
        }
        if info_len > 3 or info_len < 1:
            return('0x401', '参数数量有误')
        i = 0
        while i < info_len:
            if info_list[i] in tier_dict:
                if info_tier != 'all':
                    return('0x402', '您输入了重复类型的参数')
                info_tier = tier_dict[info_list[i]]
            elif info_list[i] in type_dict:
                if info_type != 'all':
                    return('0x402', '您输入了重复类型的参数')
                info_type = type_dict[info_list[i]]
            elif info_list[i] in nation_dict:
                if info_nation != 'all':
                    return('0x402', '您输入了重复类型的参数')
                info_nation = nation_dict[info_list[i]]
            else:
                return('0x401', '参数数量有误')
            i += 1
        #account_id = 2034370595
        sys.path.append(os.path.dirname(
            __file__).replace('pic/kokomi', 'function'))
        import tool
        application_id = tool.get_application_id()
        url = 'https://api.worldofwarships.server/wows/ships/stats/?application_id=applicationid&account_id=accountid&language=zh-cn&extra=typeextra'
        url = url.replace('accountid', str(account_id)
                          ).replace('typeextra', 'rank_solo').replace('applicationid', application_id).replace('server', server)

        try:
            ship_info_data = open(tool.get_data_path(
                'shipinfo'), "r", encoding='utf-8')
            shipinfodata = json.load(ship_info_data)
            ship_info_data.close()
        except:
            return('0x301', '导入本地数据文件出现错误')
        try:
            rank_data = requests.get(url=url)
        except:
            return('0x403', '请求数据失败，请检查网络')
        rankdata = json.loads(rank_data.text)
        rank_data.close()

        pvp_all_data = rankdata["data"][str(account_id)]
        clcnum = len(pvp_all_data)
        pvp_all_battles = 0
        pvp_all_damage = 0
        pvp_all_wins = 0
        pvp_all_frags = 0
        pvp_all_pr = 0
        pvp_all_n_damage = 0
        pvp_all_n_frage = 0
        i = 0

        shipdata_dict = tree()
        rank_dict = tree()

        img = Image.open(os.path.dirname(__file__)+'/me.png')
        draw = ImageDraw.Draw(img)
        font = tool.get_font(2, 27)
        font1 = tool.get_font(2, 40)
        font2 = tool.get_font(2, 33)
        font3 = tool.get_font(3, 40)
        y_coord = 340

        while i < clcnum:
            ship_id = pvp_all_data[i]["ship_id"]
            if str(ship_id) not in shipinfodata:
                i += 1
                continue
            tier = shipinfodata[str(ship_id)]['tier']
            shiptype = shipinfodata[str(ship_id)]['type']
            nation = shipinfodata[str(ship_id)]['nation']
            shipname = shipinfodata[str(ship_id)]['name']
            if info_type == 'all' or shiptype == info_type:
                if info_tier == 'all' or tier == info_tier:
                    if info_nation == 'all' or nation == info_nation:
                        # 提取pvp数据
                        pvp_battles = pvp_all_data[i]['pvp']['battles']
                        pvp_wins = pvp_all_data[i]['pvp']['wins']
                        pvp_damage = pvp_all_data[i]['pvp']['damage_dealt']
                        pvp_frags = pvp_all_data[i]['pvp']['frags']
                        pvp_xp = pvp_all_data[i]['pvp']['xp']
                        pvp_planes = pvp_all_data[i]['pvp']['planes_killed']

                        if pvp_battles != 0:
                            pvp_average_damage = pvp_damage/pvp_battles
                            pvp_average_wins = pvp_wins/pvp_battles*100
                            pvp_average_frags = pvp_frags/pvp_battles
                            pvppr, pvp_n_damage, pvp_n_frag = tool.get_pvp_pr(
                                pvp_average_damage, pvp_average_wins, pvp_average_frags, ship_id)
                            if pvppr == -1:
                                i += 1
                                continue
                            PR, box, diff = tool.get_pr_box(pvppr)

                            pvp_all_battles += pvp_battles
                            pvp_all_damage += pvp_damage
                            pvp_all_wins += pvp_wins
                            pvp_all_frags += pvp_frags
                            pvp_all_pr += pvppr*pvp_battles
                            pvp_all_n_damage += pvp_n_damage*pvp_battles
                            pvp_all_n_frage += pvp_n_frag*pvp_battles

                            shipdata_dict[shipname]['pr'] = PR + \
                                '(+'+str(diff)+')'
                            shipdata_dict[shipname]['box'] = box
                            shipdata_dict[shipname]['tier'] = str(tier)
                            shipdata_dict[shipname]['battle'] = str(
                                pvp_battles)
                            shipdata_dict[shipname]['outwin'] = str(
                                round(pvp_average_wins, 2)) + '%'
                            shipdata_dict[shipname]['win'] = round(
                                pvp_average_wins, 2)
                            shipdata_dict[shipname]['damage'] = str(
                                int(pvp_average_damage))
                            shipdata_dict[shipname]['n_damage'] = pvp_n_damage
                            shipdata_dict[shipname]['frag'] = str(
                                round(pvp_average_frags, 2))
                            shipdata_dict[shipname]['n_frag'] = pvp_n_frag
                            rank_dict[shipname] = pvppr
                        else:
                            PR, box, diff = tool.get_pr_box(-1)
                            shipdata_dict[shipname]['pr'] = PR + \
                                '(+'+str(diff)+')'
                            shipdata_dict[shipname]['box'] = box
                            shipdata_dict[shipname]['tier'] = str(tier)
                            shipdata_dict[shipname]['battle'] = '0'
                            shipdata_dict[shipname]['outwin'] = '0.0%'
                            shipdata_dict[shipname]['win'] = 0
                            shipdata_dict[shipname]['damage'] = '0'
                            shipdata_dict[shipname]['n_damage'] = 0
                            shipdata_dict[shipname]['frag'] = '0'
                            shipdata_dict[shipname]['n_frag'] = 0
                            rank_dict[shipname] = 0

            i += 1
        rankdict = sorted(rank_dict.items(), key=lambda x: x[1], reverse=True)
        shiprank_len = len(rankdict)
        if shiprank_len == 0:
            return ('0x404', '没有筛选到数据，请检查筛选条件')
        i = 0
        while i < shiprank_len:
            shipname = rankdict[i][0]
            x_coord = 135-int(tool.get_x_coord(shipname, font))
            draw.text((x_coord+2, y_coord+2),
                      shipname, (0, 0, 0), font=font)

            box = shipdata_dict[shipname]['box']
            out_pr = shipdata_dict[shipname]['pr']
            x_coord = 360-int(tool.get_x_coord(out_pr, font))
            draw.text((x_coord+2, y_coord+2),
                      out_pr, box, font=font)

            tier = shipdata_dict[shipname]['tier']
            x_coord = 516-int(tool.get_x_coord(tier, font))
            draw.text((x_coord+2, y_coord+2), tier, (0, 0, 0), font=font)

            pvp_battles = shipdata_dict[shipname]['battle']
            x_coord = 627-int(tool.get_x_coord(pvp_battles, font))
            draw.text((x_coord+2, y_coord+2),
                      pvp_battles, (0, 0, 0), font=font)

            out_wins = shipdata_dict[shipname]['outwin']
            x_coord = 742-int(tool.get_x_coord(out_wins, font))
            color_box = tool.get_win_box(shipdata_dict[shipname]['win'])
            draw.text((x_coord+2, y_coord+2), out_wins, color_box, font=font)

            pvp_average_damage = shipdata_dict[shipname]['damage']
            x_coord = 860 - int(tool.get_x_coord(pvp_average_damage, font))
            color_box = tool.get_damage_box(
                shipdata_dict[shipname]['n_damage'])
            draw.text((x_coord+2, y_coord+2),
                      str(int(pvp_average_damage)), color_box, font=font)

            pvp_average_frags = shipdata_dict[shipname]['frag']
            x_coord = 975 - int(tool.get_x_coord(pvp_average_frags, font))
            color_box = tool.get_frag_box(shipdata_dict[shipname]['n_frag'])
            draw.text((x_coord+2, y_coord+2),
                      pvp_average_frags, color_box, font=font)
            y_coord += 40
            i += 1
        x_coord = 565 - \
            tool.get_x_coord(
                f'筛选条件：等级：{info_tier} 船只：{info_type} 国家：{info_nation}', font2)
        draw.text((x_coord, 130),
                  f'筛选条件：等级：{info_tier} 船只：{info_type} 国家：{info_nation}', (0, 0, 0), font=font2)
        pvp_all_average_win = round(pvp_all_wins/pvp_all_battles*100, 2)
        pvp_all_average_damage = str(int(pvp_all_damage/pvp_all_battles))
        pvp_all_average_frag = str(round(pvp_all_frags/pvp_all_battles, 2))
        pvp_all_n_damage = pvp_all_n_damage/pvp_all_battles
        pvp_all_n_frag = pvp_all_n_frage/pvp_all_battles
        x_coord = 180-int(tool.get_x_coord(str(pvp_all_battles), font1))
        draw.text((x_coord+2, 210),
                  str(pvp_all_battles), (0, 0, 0), font=font1)
        out_win = str(pvp_all_average_win)+'%'
        color_box = tool.get_win_box(pvp_all_average_win)
        x_coord = 405-int(tool.get_x_coord(out_win, font1))
        draw.text((x_coord+2, 210), out_win, color_box, font=font1)
        color_box = tool.get_damage_box(pvp_all_n_damage)
        x_coord = 635-int(tool.get_x_coord(pvp_all_average_damage, font1))
        draw.text((x_coord+2, 210), pvp_all_average_damage,
                  color_box, font=font1)
        color_box = tool.get_frag_box(pvp_all_n_frag)
        x_coord = 892-int(tool.get_x_coord(pvp_all_average_frag, font1))
        draw.text((x_coord+2, 210), pvp_all_average_frag,
                  color_box, font=font1)

        pvp_all_average_pr = pvp_all_pr/pvp_all_battles
        PR, color_box, diff_pr = tool.get_pr_box(pvp_all_average_pr)
        all_pr_box = ImageDraw.ImageDraw(img)
        all_pr_box.rectangle(((105, 74), (1023, 124)),
                             fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        x_coord = 565 - tool.get_x_coord(out_pr, font1)
        draw.text((x_coord, 72), out_pr, (255, 255, 255), font=font1)
        clan_id_url = 'http://api.worldofwarships.asia/wows/clans/accountinfo/?application_id=aaaa630bfc681dfdbc13c3327eac2e85&account_id=accountid'
        clanid_url = clan_id_url.replace('accountid', str(account_id))
        clan_id_original_data = requests.get(url=clanid_url, verify=False)
        clan_id_processed_data = json.loads(clan_id_original_data.text)
        clan_id_original_data.close()
        clan_id = clan_id_processed_data["data"][str(account_id)]["clan_id"]
        account_name = clan_id_processed_data["data"][str(
            account_id)]["account_name"]
        if clan_id == None:
            clan_name = ""
        elif clan_id == "":
            clan_name = ""
        else:
            clan_name_url = 'http://api.worldofwarships.asia/wows/clans/info/?application_id=aaaa630bfc681dfdbc13c3327eac2e85&clan_id=clanid'
            clanname_url = clan_name_url.replace('clanid', str(clan_id))
            clan_name_original_data = requests.get(url=clanname_url)
            # 数据处理
            clan_name_processed_data = json.loads(clan_name_original_data.text)
            clan_name_original_data.close()
            if clan_name_processed_data["status"] == "error":
                clan_name = ""
            else:
                clan_name = clan_name_processed_data["data"][str(
                    clan_id)]["tag"]
        user_name = "["+str(clan_name)+"]"+str(account_name)
        x_coord = 565 - tool.get_x_coord(user_name, font3)
        draw.text((x_coord, 10), user_name, (0, 0, 0), font=font3)
        x_coord = 565 - \
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


def tree():
    return collections.defaultdict(tree)
