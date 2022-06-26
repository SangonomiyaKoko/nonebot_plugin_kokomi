
from turtle import color
import requests
import json
import time
import os
import sys
from PIL import ImageFont, Image, ImageDraw

# 数据响应模块


def wws_me(account_id: int, server: str):
    sys.path.append(os.path.dirname(
        __file__).replace('pic\\kokomi', 'function'))
    import tool
    #account_id = 2034370595
    application_id = tool.get_application_id()
    url = 'https://api.worldofwarships.server/wows/ships/stats/?application_id=applicationid&account_id=accountid&language=zh-cn&extra=typeextra'
    url1 = url.replace('accountid', str(account_id)
                       ).replace('typeextra', 'pvp_solo').replace('applicationid', application_id).replace('server', server)
    url2 = url.replace('accountid', str(account_id)
                       ).replace('typeextra', 'pvp_div2').replace('applicationid', application_id).replace('server', server)
    url3 = url.replace('accountid', str(account_id)
                       ).replace('typeextra', 'pvp_div3').replace('applicationid', application_id).replace('server', server)
    url4 = url.replace('accountid', str(account_id)
                       ).replace('typeextra', 'rank_solo').replace('applicationid', application_id).replace('server', server)
    achieve_url = 'https://api.worldofwarships.server/wows/account/achievements/?application_id=aaaa630bfc681dfdbc13c3327eac2e85&account_id=accountid'
    url5 = achieve_url.replace('accountid', str(
        account_id)).replace('server', server)
    # 导入json数据文件
    try:
        ship_info_data = open(tool.get_data_path(
            'shipinfo'), "r", encoding='utf-8')
        shipinfodata = json.load(ship_info_data)
        ship_info_data.close()
    except:
        return('0x301', '导入本地数据文件出现错误')

    # pvp总数据
    try:
        rank_data = requests.get(url=url4)
        rankdata = json.loads(rank_data.text)
        rank_data.close()
        if rankdata["meta"]["count"] == 0:
            return('0x302', 'api数据接口没有返回数据，请检查是否隐藏战绩')

        pvp_all_data = rankdata["data"][str(account_id)]
        clcnum = len(pvp_all_data)
        pvp_all_battles = 0
        pvp_all_value_battles = 0
        pvp_all_damage = 0
        pvp_all_wins = 0
        pvp_all_frags = 0
        pvp_all_planes = 0
        pvp_all_xp = 0
        pvp_all_pr = 0
        pvp_all_n_damage = 0
        pvp_all_n_frage = 0
        i = 0

        # rank总数据
        rank_all_battles = 0
        rank_all_damage = 0
        rank_all_wins = 0
        rank_all_frags = 0
        rank_all_planes = 0
        rank_all_xp = 0
        rank_all_pr = 0
        rank_all_n_damage = 0
        rank_all_n_frage = 0

        # solo数据
        solo_data = requests.get(url=url1)
        solodata = json.loads(solo_data.text)
        solo_data.close()
        solo_all_data = solodata["data"][str(account_id)]
        solo_clcnum = len(pvp_all_data)

        solo_all_battles = 0
        solo_all_value_battles = 0
        solo_all_damage = 0
        solo_all_wins = 0
        solo_all_frags = 0
        solo_all_planes = 0
        solo_all_xp = 0
        solo_all_pr = 0
        solo_all_n_damage = 0
        solo_all_n_frage = 0
        j = 0

        # div2数据
        div2_data = requests.get(url=url2)
        div2data = json.loads(div2_data.text)
        div2_data.close()
        div2_all_data = div2data["data"][str(account_id)]
        div2_clcnum = len(div2_all_data)

        div2_all_battles = 0
        div2_all_value_battles = 0
        div2_all_damage = 0
        div2_all_wins = 0
        div2_all_frags = 0
        div2_all_planes = 0
        div2_all_xp = 0
        div2_all_pr = 0
        div2_all_n_damage = 0
        div2_all_n_frage = 0
        k = 0

        # div3数据

        div3_data = requests.get(url=url3)
        div3data = json.loads(div3_data.text)
        div3_data.close()
        div3_all_data = div3data["data"][str(account_id)]
        div3_clcnum = len(div3_all_data)

        div3_all_battles = 0
        div3_all_value_battles = 0
        div3_all_damage = 0
        div3_all_wins = 0
        div3_all_frags = 0
        div3_all_planes = 0
        div3_all_xp = 0
        div3_all_pr = 0
        div3_all_n_damage = 0
        div3_all_n_frage = 0
        l = 0
        # 最高数据记录
        pvp_damage_rank = {}
        pvp_frag_rank = {}
        pvp_plane_rank = {}
        pvp_agro_rank = {}
        pvp_spotted_rank = {}
        pvp_xp_rank = {}
        pvp_scouting_rank = {}
        # pvp总数据记录
        pvp_all_type_dict = {
            'AirCarrier': {
                'all_battles': 0,
                'all_damage': 0,
                'all_value_battles': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            'Battleship': {
                'all_battles': 0,
                'all_damage': 0,
                'all_value_battles': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            'Cruiser': {
                'all_battles': 0,
                'all_damage': 0,
                'all_value_battles': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            'Destroyer': {
                'all_battles': 0,
                'all_damage': 0,
                'all_value_battles': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            }
        }
        rank_all_type_dict = {
            'AirCarrier': {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            'Battleship': {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            'Cruiser': {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            'Destroyer': {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            }
        }
        # rank总数据记录
        pvp_all_tier_dict = {
            1: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            2: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            3: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            4: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            5: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            6: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            7: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            8: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            9: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            10: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            },
            11: {
                'all_battles': 0,
                'all_damage': 0,
                'all_wins': 0,
                'all_frags': 0,
                'all_planes': 0,
                'all_xp': 0,
                'all_pr': 0,
                'all_n_damage': 0,
                'all_n_frag': 0
            }
        }
        # 成就数据记录
        achievement_dict = {
            'PCH016_FirstBlood': 0,
            'PCH004_Dreadnought': 0,
            'PCH011_InstantKill': 0,
            'PCH003_MainCaliber': 0,
            'PCH006_Withering': 0,
            'PCH023_Warrior': 0,
            'PCH010_Retribution': 0,
            'PCH017_Fireproof': 0,
            'PCH012_Arsonist': 0,
            'PCH020_ATBACaliber': 0,
            'PCH001_DoubleKill': 0,
            'PCH174_AirDefenseExpert': 0,
            'PCH019_Detonated': 0,
            'PCH013_Liquidator': 0,
            'PCH014_Headbutt': 0,
            'PCH002_OneSoldierInTheField': 0,
            'PCH018_Unsinkable': 0,

            'PCH161_CLAN_LEAGUE_4': 0,
            'PCH160_CLAN_LEAGUE_3': 0,
            'PCH159_CLAN_LEAGUE_2': 0,
            'PCH158_CLAN_LEAGUE_1': 0,

            'PCH276_JollyRogerBronze': 0,
            'PCH277_JollyRogerSilver': 0,
            'PCH232_JollyRoger': 0
        }
        achieve_data = requests.get(url=url5)
        achievedata = json.loads(achieve_data.text)
        achieve_data.close()
    except:
        return('0x303', '请求数据发生错误，请检查网络')
    achieve_all_data = achievedata["data"][str(account_id)]["battle"]
    m = 0
    while i < clcnum:
        ship_id = pvp_all_data[i]["ship_id"]
        if str(ship_id) not in shipinfodata:
            i += 1
            continue
        tier = shipinfodata[str(ship_id)]['tier']
        shiptype = shipinfodata[str(ship_id)]['type']
        # 提取pvp数据
        pvp_battles = pvp_all_data[i]['pvp']['battles']
        pvp_wins = pvp_all_data[i]['pvp']['wins']
        pvp_damage = pvp_all_data[i]['pvp']['damage_dealt']
        pvp_frags = pvp_all_data[i]['pvp']['frags']
        pvp_xp = pvp_all_data[i]['pvp']['xp']
        pvp_planes = pvp_all_data[i]['pvp']['planes_killed']

        max_pvp_damage = pvp_all_data[i]['pvp']['max_damage_dealt']
        max_pvp_frag = pvp_all_data[i]['pvp']['max_frags_battle']
        max_pvp_plane = pvp_all_data[i]['pvp']['max_planes_killed']
        max_pvp_agro = pvp_all_data[i]['pvp']['max_total_agro']
        max_pvp_spotted = pvp_all_data[i]['pvp']['max_ships_spotted']
        max_pvp_xp = pvp_all_data[i]['pvp']['max_xp']
        max_pvp_scouting = pvp_all_data[i]['pvp']['max_damage_scouting']
        # 提取rank数据
        rank_battles = pvp_all_data[i]['rank_solo']['battles']
        rank_wins = pvp_all_data[i]['rank_solo']['wins']
        rank_damage = pvp_all_data[i]['rank_solo']['damage_dealt']
        rank_frags = pvp_all_data[i]['rank_solo']['frags']
        rank_xp = pvp_all_data[i]['rank_solo']['xp']
        rank_planes = pvp_all_data[i]['rank_solo']['planes_killed']
        if tier <= 4:
            # pvp数据录入
            if pvp_battles != 0 and shiptype in pvp_all_type_dict:
                pvp_all_tier_dict[tier]['all_battles'] += pvp_battles
                pvp_all_tier_dict[tier]['all_damage'] += pvp_damage
                pvp_all_tier_dict[tier]['all_wins'] += pvp_wins
                pvp_all_tier_dict[tier]['all_frags'] += pvp_frags
                pvp_all_tier_dict[tier]['all_planes'] += pvp_planes
                pvp_all_tier_dict[tier]['all_xp'] += pvp_xp

                pvp_all_battles += pvp_battles
                pvp_all_damage += pvp_damage
                pvp_all_wins += pvp_wins
                pvp_all_frags += pvp_frags
                pvp_all_planes += pvp_planes
                pvp_all_xp += pvp_xp

                pvp_damage_rank[ship_id] = max_pvp_damage
                pvp_frag_rank[ship_id] = max_pvp_frag
                pvp_plane_rank[ship_id] = max_pvp_plane
                pvp_agro_rank[ship_id] = max_pvp_agro
                pvp_spotted_rank[ship_id] = max_pvp_spotted
                pvp_xp_rank[ship_id] = max_pvp_xp
                pvp_scouting_rank[ship_id] = max_pvp_scouting

                pvp_all_type_dict[shiptype]['all_battles'] += pvp_battles
                pvp_all_type_dict[shiptype]['all_damage'] += pvp_damage
                pvp_all_type_dict[shiptype]['all_wins'] += pvp_wins
                pvp_all_type_dict[shiptype]['all_frags'] += pvp_frags
                pvp_all_type_dict[shiptype]['all_planes'] += pvp_planes
                pvp_all_type_dict[shiptype]['all_xp'] += pvp_xp
        else:
            if pvp_battles != 0 and shiptype in pvp_all_type_dict:

                # pvp_pr数据录入
                pvp_average_damage = pvp_damage/pvp_battles
                pvp_average_wins = pvp_wins/pvp_battles*100
                pvp_aversge_frags = pvp_frags/pvp_battles
                pvppr, pvp_n_damage, pvp_n_frag = tool.get_pvp_pr(
                    pvp_average_damage, pvp_average_wins, pvp_aversge_frags, ship_id)
                if pvppr == -1:
                    i += 1
                    continue
                pvp_all_tier_dict[tier]['all_pr'] += pvppr*pvp_battles

                pvp_all_battles += pvp_battles
                pvp_all_value_battles += pvp_battles
                pvp_all_damage += pvp_damage
                pvp_all_wins += pvp_wins
                pvp_all_frags += pvp_frags
                pvp_all_planes += pvp_planes
                pvp_all_xp += pvp_xp
                pvp_all_pr += pvppr*pvp_battles
                pvp_all_n_damage += pvp_n_damage*pvp_battles
                pvp_all_n_frage += pvp_n_frag*pvp_battles

                pvp_all_tier_dict[tier]['all_battles'] += pvp_battles
                pvp_all_tier_dict[tier]['all_damage'] += pvp_damage
                pvp_all_tier_dict[tier]['all_wins'] += pvp_wins
                pvp_all_tier_dict[tier]['all_frags'] += pvp_frags
                pvp_all_tier_dict[tier]['all_planes'] += pvp_planes
                pvp_all_tier_dict[tier]['all_xp'] += pvp_xp
                pvp_all_tier_dict[tier]['all_n_damage'] += pvp_n_damage*pvp_battles
                pvp_all_tier_dict[tier]['all_n_frag'] += pvp_n_frag*pvp_battles

                pvp_damage_rank[ship_id] = max_pvp_damage
                pvp_frag_rank[ship_id] = max_pvp_frag
                pvp_plane_rank[ship_id] = max_pvp_plane
                pvp_agro_rank[ship_id] = max_pvp_agro
                pvp_spotted_rank[ship_id] = max_pvp_spotted
                pvp_xp_rank[ship_id] = max_pvp_xp
                pvp_scouting_rank[ship_id] = max_pvp_scouting

                pvp_all_type_dict[shiptype]['all_battles'] += pvp_battles
                pvp_all_type_dict[shiptype]['all_value_battles'] += pvp_battles
                pvp_all_type_dict[shiptype]['all_damage'] += pvp_damage
                pvp_all_type_dict[shiptype]['all_wins'] += pvp_wins
                pvp_all_type_dict[shiptype]['all_frags'] += pvp_frags
                pvp_all_type_dict[shiptype]['all_planes'] += pvp_planes
                pvp_all_type_dict[shiptype]['all_xp'] += pvp_xp
                pvp_all_type_dict[shiptype]['all_pr'] += pvppr*pvp_battles
                pvp_all_type_dict[shiptype]['all_n_damage'] += pvp_n_damage*pvp_battles
                pvp_all_type_dict[shiptype]['all_n_frag'] += pvp_n_frag*pvp_battles

            if rank_battles != 0 and shiptype in rank_all_type_dict:
                rank_average_damage = rank_damage/rank_battles
                rank_average_wins = rank_wins/rank_battles*100
                rank_aversge_frags = rank_frags/rank_battles
                rankpr, rank_n_damage, rank_n_frag = tool.get_rank_pr(rank_average_damage, rank_average_wins,
                                                                      rank_aversge_frags, ship_id)
                if rankpr == -1:
                    i += 1
                    continue
                rank_all_type_dict[shiptype]['all_battles'] += rank_battles
                rank_all_type_dict[shiptype]['all_damage'] += rank_damage
                rank_all_type_dict[shiptype]['all_wins'] += rank_wins
                rank_all_type_dict[shiptype]['all_frags'] += rank_frags
                rank_all_type_dict[shiptype]['all_planes'] += rank_planes
                rank_all_type_dict[shiptype]['all_xp'] += rank_xp
                rank_all_type_dict[shiptype]['all_pr'] += rankpr * \
                    rank_battles
                rank_all_type_dict[shiptype]['all_n_damage'] += rank_n_damage*rank_battles
                rank_all_type_dict[shiptype]['all_n_frag'] += rank_n_frag*rank_battles

                rank_all_battles += rank_battles
                rank_all_damage += rank_damage
                rank_all_wins += rank_wins
                rank_all_frags += rank_frags
                rank_all_planes += rank_planes
                rank_all_xp += rank_xp
                rank_all_pr += rankpr*rank_battles
                rank_all_n_damage += rank_n_damage*rank_battles
                rank_all_n_frage += rank_n_frag*rank_battles
        i += 1
    while j < solo_clcnum:
        ship_id = solo_all_data[j]["ship_id"]
        # 提取pvp数据
        if str(ship_id) not in shipinfodata:
            j += 1
            continue
        tier = shipinfodata[str(ship_id)]['tier']
        solo_battles = solo_all_data[j]['pvp_solo']['battles']
        solo_wins = solo_all_data[j]['pvp_solo']['wins']
        solo_damage = solo_all_data[j]['pvp_solo']['damage_dealt']
        solo_frags = solo_all_data[j]['pvp_solo']['frags']
        solo_xp = solo_all_data[j]['pvp_solo']['xp']
        solo_planes = solo_all_data[j]['pvp_solo']['planes_killed']
        if solo_battles != 0 and tier > 4:
            solo_average_damage = solo_damage/solo_battles
            solo_average_wins = solo_wins/solo_battles*100
            solo_aversge_frags = solo_frags/solo_battles
            solopr, solo_n_damage, solo_n_frag = tool.get_pvp_pr(
                solo_average_damage, solo_average_wins, solo_aversge_frags, ship_id)
            if solopr == -1:
                j += 1
                continue
            solo_all_battles += solo_battles
            solo_all_value_battles += solo_battles
            solo_all_damage += solo_damage
            solo_all_wins += solo_wins
            solo_all_frags += solo_frags
            solo_all_planes += solo_planes
            solo_all_xp += solo_xp
            solo_all_pr += solopr*solo_battles
            solo_all_n_damage += solo_n_damage*solo_battles
            solo_all_n_frage += solo_n_frag*solo_battles
        elif solo_battles != 0 and tier <= 4:
            solo_all_battles += solo_battles
            solo_all_damage += solo_damage
            solo_all_wins += solo_wins
            solo_all_frags += solo_frags
            solo_all_planes += solo_planes
            solo_all_xp += solo_xp
        j += 1
    while k < div2_clcnum:
        ship_id = div2_all_data[k]["ship_id"]
        if str(ship_id) not in shipinfodata:
            k += 1
            continue
        tier = shipinfodata[str(ship_id)]['tier']
        div2_battles = div2_all_data[k]['pvp_div2']['battles']
        div2_wins = div2_all_data[k]['pvp_div2']['wins']
        div2_damage = div2_all_data[k]['pvp_div2']['damage_dealt']
        div2_frags = div2_all_data[k]['pvp_div2']['frags']
        div2_xp = div2_all_data[k]['pvp_div2']['xp']
        div2_planes = div2_all_data[k]['pvp_div2']['planes_killed']
        if div2_battles != 0 and tier > 4:
            div2_average_damage = div2_damage/div2_battles
            div2_average_wins = div2_wins/div2_battles*100
            div2_aversge_frags = div2_frags/div2_battles
            div2pr, div2_n_damage, div2_n_frag = tool.get_pvp_pr(
                div2_average_damage, div2_average_wins, div2_aversge_frags, ship_id)
            if div2pr == -1:
                k += 1
                continue
            div2_all_battles += div2_battles
            div2_all_value_battles += div2_battles
            div2_all_damage += div2_damage
            div2_all_wins += div2_wins
            div2_all_frags += div2_frags
            div2_all_planes += div2_planes
            div2_all_xp += div2_xp
            div2_all_pr += div2pr*div2_battles
            div2_all_n_damage += div2_n_damage*div2_battles
            div2_all_n_frage += div2_n_frag*div2_battles
        elif div2_battles != 0 and tier <= 4:
            div2_all_battles += div2_battles
            div2_all_damage += div2_damage
            div2_all_wins += div2_wins
            div2_all_frags += div2_frags
            div2_all_planes += div2_planes
            div2_all_xp += div2_xp
        k += 1
    while l < div3_clcnum:
        ship_id = div3_all_data[l]["ship_id"]
        if str(ship_id) not in shipinfodata:
            l += 1
            continue
        # 提取pvp数据
        tier = shipinfodata[str(ship_id)]['tier']
        # 提取pvp数据
        div3_battles = div3_all_data[l]['pvp_div3']['battles']
        div3_wins = div3_all_data[l]['pvp_div3']['wins']
        div3_damage = div3_all_data[l]['pvp_div3']['damage_dealt']
        div3_frags = div3_all_data[l]['pvp_div3']['frags']
        div3_xp = div3_all_data[l]['pvp_div3']['xp']
        div3_planes = div3_all_data[l]['pvp_div3']['planes_killed']
        if div3_battles != 0 and tier > 4:
            div3_average_damage = div3_damage/div3_battles
            div3_average_wins = div3_wins/div3_battles*100
            div3_aversge_frags = div3_frags/div3_battles
            div3pr, div3_n_damage, div3_n_frag = tool.get_pvp_pr(
                div3_average_damage, div3_average_wins, div3_aversge_frags, ship_id)
            if div3pr == -1:
                l += 1
                continue
            div3_all_battles += div3_battles
            div3_all_value_battles += div3_battles
            div3_all_damage += div3_damage
            div3_all_wins += div3_wins
            div3_all_frags += div3_frags
            div3_all_planes += div3_planes
            div3_all_xp += div3_xp
            div3_all_pr += div3pr*div3_battles
            div3_all_n_damage += div3_n_damage*div3_battles
            div3_all_n_frage += div3_n_frag*div3_battles
        elif div3_battles != 0 and tier <= 4:
            div3_all_battles += div3_battles
            div3_all_damage += div3_damage
            div3_all_wins += div3_wins
            div3_all_frags += div3_frags
            div3_all_planes += div3_planes
            div3_all_xp += div3_xp
        l += 1
    for key, value in achievement_dict.items():
        if key not in achieve_all_data:
            continue
        else:
            achievement_dict[key] = achieve_all_data[key]
    account_name, clan_name = tool.get_user_name(account_id, server)
    user_name = "["+str(clan_name)+"]"+str(account_name)
    time_url = 'https://api.worldofwarships.server/wows/account/info/?application_id=applicationid&account_id=accountid'
    time_url = time_url.replace('accountid', str(account_id)).replace(
        'applicationid', application_id).replace('server', server)
    time_data = requests.get(url=time_url)
    timedata = json.loads(time_data.text)
    time_data.close()
    last_battle_time = timedata['data'][str(
        account_id)]["last_battle_time"]
    create_time = timedata['data'][str(account_id)]["created_at"]

    #     =================PILLOW==================
    img = Image.open(os.path.dirname(__file__)+'\\wwsme.png')
    draw = ImageDraw.Draw(img)
    font = tool.get_font(1, 95)
    font2 = tool.get_font(1, 70)
    font3 = tool.get_font(1, 80)
    font4 = tool.get_font(1, 45)
    font5 = tool.get_font(1, 55)
    font6 = tool.get_font(3, 55)
    font7 = tool.get_font(2, 55)
    font8 = tool.get_font(1, 120)
    # 用户信息
    xcoord = 950-tool.get_x_coord(user_name, font)
    draw.text((xcoord, 57), user_name, (255, 255, 255), font=font)
    user_accountid = server.upper()+'  --'+str(account_id)
    draw.text((1235, 175), user_accountid, (255, 255, 255), font=font4)
    lastbattletime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(last_battle_time))
    draw.text((2465, 40), lastbattletime, (255, 255, 255), font=font2)
    createtime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(create_time))
    draw.text((4500, 2533), createtime, (255, 255, 255), font=font3)

    diff_day = str(int((time.time() - create_time)/86400))
    draw.text((5008, 2660), diff_day, (255, 240, 0), font=font8)
    # PVP数据总览
    if pvp_all_battles != 0 and pvp_all_value_battles != 0:
        xcoord = 371-tool.get_x_coord(str(pvp_all_battles), font2)
        draw.text((xcoord, 667), str(pvp_all_battles),
                  (255, 255, 255), font=font2)

        out_wins = str(round(pvp_all_wins/pvp_all_battles*100, 2)) + '%'
        xcoord = 942-tool.get_x_coord(out_wins, font2)
        color_box = tool.get_win_box(pvp_all_wins/pvp_all_battles*100)
        draw.text((xcoord, 667), out_wins, color_box, font=font2)

        xcoord = 1573 - \
            tool.get_x_coord(
                str(int(pvp_all_damage/pvp_all_battles)), font2)
        color_box = tool.get_damage_box(
            pvp_all_n_damage/pvp_all_value_battles)
        draw.text((xcoord, 667), str(int(pvp_all_damage/pvp_all_battles)),
                  color_box, font=font2)

        xcoord = 371 - \
            tool.get_x_coord(
                str(round(pvp_all_frags/pvp_all_battles, 2)), font2)
        color_box = tool.get_frag_box(
            pvp_all_n_frage/pvp_all_value_battles)
        draw.text((xcoord, 876), str(
            round(pvp_all_frags/pvp_all_battles, 2)), color_box, font=font2)

        xcoord = 942 - \
            tool.get_x_coord(str(int(pvp_all_xp/pvp_all_battles)), font2)
        draw.text((xcoord, 876), str(int(pvp_all_xp/pvp_all_battles)),
                  (255, 255, 255), font=font2)

        xcoord = 1573 - \
            tool.get_x_coord(
                str(round(pvp_all_planes/pvp_all_battles, 2)), font2)
        color_box = tool.get_plane_box(pvp_all_planes/pvp_all_battles)
        draw.text((xcoord, 876), str(round(pvp_all_planes/pvp_all_battles, 2)),
                  color_box, font=font2)

        PR, color_box, diff_pr = tool.get_pr_box(
            pvp_all_pr/pvp_all_value_battles)
        pvp_all_pr_box = ImageDraw.ImageDraw(img)
        pvp_all_pr_box.rectangle(((56, 415), (1865, 516)),
                                 fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 950 - tool.get_x_coord(out_pr, font3)
        draw.text((xcoord, 434), out_pr, (255, 255, 255), font=font3)
    elif pvp_all_battles != 0 and pvp_all_value_battles == 0:
        xcoord = 371-tool.get_x_coord(str(pvp_all_battles), font2)
        draw.text((xcoord, 667), str(pvp_all_battles),
                  (255, 255, 255), font=font2)

        out_wins = str(round(pvp_all_wins/pvp_all_battles*100, 2)) + '%'
        xcoord = 942-tool.get_x_coord(out_wins, font2)
        color_box = tool.get_win_box(pvp_all_wins/pvp_all_battles*100)
        draw.text((xcoord, 667), out_wins, color_box, font=font2)

        xcoord = 1573 - \
            tool.get_x_coord(
                str(int(pvp_all_damage/pvp_all_battles)), font2)
        color_box = tool.get_damage_box(0)
        draw.text((xcoord, 667), str(int(pvp_all_damage/pvp_all_battles)),
                  color_box, font=font2)

        xcoord = 371 - \
            tool.get_x_coord(
                str(round(pvp_all_frags/pvp_all_battles, 2)), font2)
        color_box = tool.get_frag_box(0)
        draw.text((xcoord, 876), str(
            round(pvp_all_frags/pvp_all_battles, 2)), color_box, font=font2)

        xcoord = 942 - \
            tool.get_x_coord(str(int(pvp_all_xp/pvp_all_battles)), font2)
        draw.text((xcoord, 876), str(int(pvp_all_xp/pvp_all_battles)),
                  (255, 255, 255), font=font2)

        xcoord = 1573 - \
            tool.get_x_coord(
                str(round(pvp_all_planes/pvp_all_battles, 2)), font2)
        color_box = tool.get_plane_box(pvp_all_planes/pvp_all_battles)
        draw.text((xcoord, 876), str(round(pvp_all_planes/pvp_all_battles, 2)),
                  color_box, font=font2)

        PR, color_box, diff_pr = tool.get_pr_box(0)
        pvp_all_pr_box = ImageDraw.ImageDraw(img)
        pvp_all_pr_box.rectangle(((56, 415), (1865, 516)),
                                 fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 950 - tool.get_x_coord(out_pr, font3)
        draw.text((xcoord, 434), out_pr, (255, 255, 255), font=font3)
    else:
        xcoord = 371-tool.get_x_coord('0', font2)
        draw.text((xcoord, 667), '0', (255, 255, 255), font=font2)

        out_wins = '0.0' + '%'
        xcoord = 942-tool.get_x_coord(out_wins, font2)
        draw.text((xcoord, 667), out_wins, (255, 255, 255), font=font2)

        xcoord = 1573-tool.get_x_coord('0', font2)
        draw.text((xcoord, 667), '0', (255, 255, 255), font=font2)

        xcoord = 371-tool.get_x_coord('0', font2)
        draw.text((xcoord, 876), '0', (255, 255, 255), font=font2)

        xcoord = 942-tool.get_x_coord('0', font2)
        draw.text((xcoord, 876), '0', (255, 255, 255), font=font2)

        xcoord = 1573-tool.get_x_coord('0', font2)
        draw.text((xcoord, 876), '0', (255, 255, 255), font=font2)

        PR, color_box, diff_pr = tool.get_pr_box(-1)
        pvp_all_pr_box = ImageDraw.ImageDraw(img)
        pvp_all_pr_box.rectangle(((56, 415), (1865, 516)),
                                 fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 950 - tool.get_x_coord(out_pr, font3)
        draw.text((xcoord, 434), out_pr, (255, 255, 255), font=font3)
    # RANK数据总览
    if rank_all_battles != 0:
        xcoord = 371-tool.get_x_coord(str(rank_all_battles), font2)
        draw.text((xcoord, 1425), str(rank_all_battles),
                  (255, 255, 255), font=font2)

        out_wins = str(round(rank_all_wins/rank_all_battles*100, 2)) + '%'
        xcoord = 942-tool.get_x_coord(out_wins, font2)
        color_box = tool.get_win_box(rank_all_wins/rank_all_battles*100)
        draw.text((xcoord, 1425), out_wins, color_box, font=font2)

        xcoord = 1573 - \
            tool.get_x_coord(
                str(int(rank_all_damage/rank_all_battles)), font2)
        color_box = tool.get_damage_box(rank_all_n_damage/rank_all_battles)
        draw.text((xcoord, 1425), str(int(rank_all_damage/rank_all_battles)),
                  color_box, font=font2)

        xcoord = 371 - \
            tool.get_x_coord(
                str(round(rank_all_frags/rank_all_battles, 2)), font2)
        color_box = tool.get_frag_box(rank_all_n_frage/rank_all_battles)
        draw.text((xcoord, 1628), str(
            round(rank_all_frags/rank_all_battles, 2)), color_box, font=font2)

        xcoord = 942 - \
            tool.get_x_coord(str(int(rank_all_xp/rank_all_battles)), font2)
        draw.text((xcoord, 1628), str(int(rank_all_xp/rank_all_battles)),
                  (255, 255, 255), font=font2)

        xcoord = 1573 - \
            tool.get_x_coord(
                str(round(rank_all_planes/rank_all_battles, 2)), font2)
        color_box = tool.get_plane_box(rank_all_planes/rank_all_battles)
        draw.text((xcoord, 1628), str(round(rank_all_planes/rank_all_battles, 2)),
                  color_box, font=font2)

        PR, color_box, diff_pr = tool.get_pr_box(
            rank_all_pr/rank_all_battles)
        rank_all_pr_box = ImageDraw.ImageDraw(img)
        rank_all_pr_box.rectangle(((56, 1162), (1865, 1263)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 950 - tool.get_x_coord(out_pr, font3)
        draw.text((xcoord, 1181), out_pr, (255, 255, 255), font=font3)
    else:
        xcoord = 371-tool.get_x_coord('0', font2)
        draw.text((xcoord, 1425), '0',
                  (255, 255, 255), font=font2)

        out_wins = '0.0' + '%'
        xcoord = 942-tool.get_x_coord(out_wins, font2)
        draw.text((xcoord, 1425), out_wins, (255, 255, 255), font=font2)

        xcoord = 1573-tool.get_x_coord('0', font2)
        draw.text((xcoord, 1425), '0',
                  (255, 255, 255), font=font2)

        xcoord = 371-tool.get_x_coord('0', font2)
        draw.text((xcoord, 1628), '0', (255, 255, 255), font=font2)

        xcoord = 942-tool.get_x_coord('0', font2)
        draw.text((xcoord, 1628), '0',
                  (255, 255, 255), font=font2)

        xcoord = 1573 - \
            tool.get_x_coord('0', font2)
        draw.text((xcoord, 1628), '0',
                  (255, 255, 255), font=font2)

        PR, color_box, diff_pr = tool.get_pr_box(-1)
        rank_all_pr_box = ImageDraw.ImageDraw(img)
        rank_all_pr_box.rectangle(((56, 1162), (1865, 1263)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 950 - tool.get_x_coord(out_pr, font3)
        draw.text((xcoord, 1181), out_pr, (255, 255, 255), font=font3)

    # PVP单野数据
    if solo_all_battles != 0 and solo_all_value_battles != 0:
        xcoord = 204-tool.get_x_coord(str(solo_all_battles), font4)
        draw.text((xcoord, 2022), str(solo_all_battles),
                  (255, 255, 255), font=font4)

        out_wins = str(round(solo_all_wins/solo_all_battles*100, 2)) + '%'
        xcoord = 469-tool.get_x_coord(out_wins, font4)
        color_box = tool.get_win_box(solo_all_wins/solo_all_battles*100)
        draw.text((xcoord, 2022), out_wins, color_box, font=font4)

        xcoord = 459 - \
            tool.get_x_coord(
                str(int(solo_all_damage/solo_all_battles)), font4)
        color_box = tool.get_damage_box(
            solo_all_n_damage/solo_all_value_battles)
        draw.text((xcoord, 2150), str(int(solo_all_damage/solo_all_battles)),
                  color_box, font=font4)

        xcoord = 204 - \
            tool.get_x_coord(
                str(round(solo_all_frags/solo_all_battles, 2)), font4)
        color_box = tool.get_frag_box(
            solo_all_n_frage/solo_all_value_battles)
        draw.text((xcoord, 2150), str(
            round(solo_all_frags/solo_all_battles, 2)), color_box, font=font4)

        xcoord = 449 - \
            tool.get_x_coord(str(int(solo_all_xp/solo_all_battles)), font4)
        draw.text((xcoord, 2281), str(int(solo_all_xp/solo_all_battles)),
                  (255, 255, 255), font=font4)

        xcoord = 204 - \
            tool.get_x_coord(
                str(round(solo_all_planes/solo_all_battles, 2)), font4)
        color_box = tool.get_plane_box(solo_all_planes/solo_all_battles)
        draw.text((xcoord, 2281), str(round(solo_all_planes/solo_all_battles, 2)),
                  color_box, font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(
            solo_all_pr/solo_all_value_battles)
        solo_all_pr_box = ImageDraw.ImageDraw(img)
        solo_all_pr_box.rectangle(((41, 1873), (611, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 316 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    elif solo_all_battles != 0 and solo_all_value_battles == 0:
        xcoord = 204-tool.get_x_coord(str(solo_all_battles), font4)
        draw.text((xcoord, 2022), str(solo_all_battles),
                  (255, 255, 255), font=font4)

        out_wins = str(round(solo_all_wins/solo_all_battles*100, 2)) + '%'
        xcoord = 469-tool.get_x_coord(out_wins, font4)
        color_box = tool.get_win_box(solo_all_wins/solo_all_battles*100)
        draw.text((xcoord, 2022), out_wins, color_box, font=font4)

        xcoord = 459 - \
            tool.get_x_coord(
                str(int(solo_all_damage/solo_all_battles)), font4)
        color_box = tool.get_damage_box(0)
        draw.text((xcoord, 2150), str(int(solo_all_damage/solo_all_battles)),
                  color_box, font=font4)

        xcoord = 204 - \
            tool.get_x_coord(
                str(round(solo_all_frags/solo_all_battles, 2)), font4)
        color_box = tool.get_frag_box(0)
        draw.text((xcoord, 2150), str(
            round(solo_all_frags/solo_all_battles, 2)), color_box, font=font4)

        xcoord = 449 - \
            tool.get_x_coord(str(int(solo_all_xp/solo_all_battles)), font4)
        draw.text((xcoord, 2281), str(int(solo_all_xp/solo_all_battles)),
                  (255, 255, 255), font=font4)

        xcoord = 204 - \
            tool.get_x_coord(
                str(round(solo_all_planes/solo_all_battles, 2)), font4)
        color_box = tool.get_plane_box(solo_all_planes/solo_all_battles)
        draw.text((xcoord, 2281), str(round(solo_all_planes/solo_all_battles, 2)),
                  color_box, font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(0)
        solo_all_pr_box = ImageDraw.ImageDraw(img)
        solo_all_pr_box.rectangle(((41, 1873), (611, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 316 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    else:
        xcoord = 204-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2022), '0', (255, 255, 255), font=font4)

        out_wins = '0.0' + '%'
        xcoord = 469-tool.get_x_coord(out_wins, font4)
        draw.text((xcoord, 2022), out_wins, (255, 255, 255), font=font4)

        xcoord = 459-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2150), '0',
                  (255, 255, 255), font=font4)

        xcoord = 204-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2150), '0', (255, 255, 255), font=font4)

        xcoord = 449-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2281), '0',
                  (255, 255, 255), font=font4)

        xcoord = 204-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2281), '0',
                  (255, 255, 255), font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(-1)
        solo_all_pr_box = ImageDraw.ImageDraw(img)
        solo_all_pr_box.rectangle(((41, 1873), (611, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 316 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)

    # PVP双排
    if div2_all_battles != 0 and div2_all_value_battles != 0:
        xcoord = 817-tool.get_x_coord(str(div2_all_battles), font4)
        draw.text((xcoord, 2022), str(div2_all_battles),
                  (255, 255, 255), font=font4)

        out_wins = str(round(div2_all_wins/div2_all_battles*100, 2)) + '%'
        xcoord = 1082-tool.get_x_coord(out_wins, font4)
        color_box = tool.get_win_box(div2_all_wins/div2_all_battles*100)
        draw.text((xcoord, 2022), out_wins, color_box, font=font4)

        xcoord = 1072 - \
            tool.get_x_coord(
                str(int(div2_all_damage/div2_all_battles)), font4)
        color_box = tool.get_damage_box(
            div2_all_n_damage/div2_all_value_battles)
        draw.text((xcoord, 2150), str(int(div2_all_damage/div2_all_battles)),
                  color_box, font=font4)

        xcoord = 817 - \
            tool.get_x_coord(
                str(round(div2_all_frags/div2_all_battles, 2)), font4)
        color_box = tool.get_frag_box(
            div2_all_n_frage/div2_all_value_battles)
        draw.text((xcoord, 2150), str(
            round(div2_all_frags/div2_all_battles, 2)), color_box, font=font4)

        xcoord = 1062 - \
            tool.get_x_coord(str(int(div2_all_xp/div2_all_battles)), font4)
        draw.text((xcoord, 2281), str(int(div2_all_xp/div2_all_battles)),
                  (255, 255, 255), font=font4)

        xcoord = 817 - \
            tool.get_x_coord(
                str(round(div2_all_planes/div2_all_battles, 2)), font4)
        color_box = tool.get_plane_box(div2_all_planes/div2_all_battles)
        draw.text((xcoord, 2281), str(round(div2_all_planes/div2_all_battles, 2)),
                  color_box, font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(
            div2_all_pr/div2_all_value_battles)
        div2_all_pr_box = ImageDraw.ImageDraw(img)
        div2_all_pr_box.rectangle(((663, 1873), (1233, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 929 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    elif div2_all_battles != 0 and div2_all_value_battles == 0:
        xcoord = 817-tool.get_x_coord(str(div2_all_battles), font4)
        draw.text((xcoord, 2022), str(div2_all_battles),
                  (255, 255, 255), font=font4)

        out_wins = str(round(div2_all_wins/div2_all_battles*100, 2)) + '%'
        xcoord = 1082-tool.get_x_coord(out_wins, font4)
        color_box = tool.get_win_box(div2_all_wins/div2_all_battles*100)
        draw.text((xcoord, 2022), out_wins, color_box, font=font4)

        xcoord = 1072 - \
            tool.get_x_coord(
                str(int(div2_all_damage/div2_all_battles)), font4)
        color_box = tool.get_damage_box(0)
        draw.text((xcoord, 2150), str(int(div2_all_damage/div2_all_battles)),
                  color_box, font=font4)

        xcoord = 817 - \
            tool.get_x_coord(
                str(round(div2_all_frags/div2_all_battles, 2)), font4)
        color_box = tool.get_frag_box(0)
        draw.text((xcoord, 2150), str(
            round(div2_all_frags/div2_all_battles, 2)), color_box, font=font4)

        xcoord = 1062 - \
            tool.get_x_coord(str(int(div2_all_xp/div2_all_battles)), font4)
        draw.text((xcoord, 2281), str(int(div2_all_xp/div2_all_battles)),
                  (255, 255, 255), font=font4)

        xcoord = 817 - \
            tool.get_x_coord(
                str(round(div2_all_planes/div2_all_battles, 2)), font4)
        color_box = tool.get_plane_box(div2_all_planes/div2_all_battles)
        draw.text((xcoord, 2281), str(round(div2_all_planes/div2_all_battles, 2)),
                  color_box, font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(0)
        div2_all_pr_box = ImageDraw.ImageDraw(img)
        div2_all_pr_box.rectangle(((663, 1873), (1233, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 929 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    else:
        xcoord = 817-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2022), '0', (255, 255, 255), font=font4)

        out_wins = '0.0' + '%'
        xcoord = 1082-tool.get_x_coord(out_wins, font4)
        draw.text((xcoord, 2022), out_wins, (255, 255, 255), font=font4)

        xcoord = 1072-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2150), '0',
                  (255, 255, 255), font=font4)

        xcoord = 817-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2150), '0', (255, 255, 255), font=font4)

        xcoord = 1062-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2281), '0',
                  (255, 255, 255), font=font4)

        xcoord = 817-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2281), '0',
                  (255, 255, 255), font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(-1)
        div2_all_pr_box = ImageDraw.ImageDraw(img)
        div2_all_pr_box.rectangle(((663, 1873), (1233, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 929 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)

    # PVP三排
    if div3_all_battles != 0 and div3_all_value_battles != 0:
        xcoord = 1430-tool.get_x_coord(str(div3_all_battles), font4)
        draw.text((xcoord, 2022), str(div3_all_battles),
                  (255, 255, 255), font=font4)

        out_wins = str(round(div3_all_wins/div3_all_battles*100, 2)) + '%'
        xcoord = 1695-tool.get_x_coord(out_wins, font4)
        color_box = tool.get_win_box(div3_all_wins/div3_all_battles*100)
        draw.text((xcoord, 2022), out_wins, color_box, font=font4)

        xcoord = 1695 - \
            tool.get_x_coord(
                str(int(div3_all_damage/div3_all_battles)), font4)
        color_box = tool.get_damage_box(
            div3_all_n_damage/div3_all_value_battles)
        draw.text((xcoord, 2150), str(int(div3_all_damage/div3_all_battles)),
                  color_box, font=font4)

        xcoord = 1430 - \
            tool.get_x_coord(
                str(round(div3_all_frags/div3_all_battles, 2)), font4)
        color_box = tool.get_frag_box(
            div3_all_n_frage/div3_all_value_battles)
        draw.text((xcoord, 2150), str(
            round(div3_all_frags/div3_all_battles, 2)), color_box, font=font4)

        xcoord = 1675 - \
            tool.get_x_coord(str(int(div3_all_xp/div3_all_battles)), font4)
        draw.text((xcoord, 2281), str(int(div3_all_xp/div3_all_battles)),
                  (255, 255, 255), font=font4)

        xcoord = 1430 - \
            tool.get_x_coord(
                str(round(div3_all_planes/div3_all_battles, 2)), font4)
        color_box = tool.get_plane_box(div3_all_planes/div3_all_battles)
        draw.text((xcoord, 2281), str(round(div3_all_planes/div3_all_battles, 2)),
                  color_box, font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(
            div3_all_pr/div3_all_value_battles)
        div3_all_pr_box = ImageDraw.ImageDraw(img)
        div3_all_pr_box.rectangle(((1279, 1873), (1849, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 1546 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    elif div3_all_battles != 0 and div3_all_value_battles == 0:
        xcoord = 1430-tool.get_x_coord(str(div3_all_battles), font4)
        draw.text((xcoord, 2022), str(div3_all_battles),
                  (255, 255, 255), font=font4)

        out_wins = str(round(div3_all_wins/div3_all_battles*100, 2)) + '%'
        xcoord = 1695-tool.get_x_coord(out_wins, font4)
        color_box = tool.get_win_box(div3_all_wins/div3_all_battles*100)
        draw.text((xcoord, 2022), out_wins, color_box, font=font4)

        xcoord = 1695 - \
            tool.get_x_coord(
                str(int(div3_all_damage/div3_all_battles)), font4)
        color_box = tool.get_damage_box(0)
        draw.text((xcoord, 2150), str(int(div3_all_damage/div3_all_battles)),
                  color_box, font=font4)

        xcoord = 1430 - \
            tool.get_x_coord(
                str(round(div3_all_frags/div3_all_battles, 2)), font4)
        color_box = tool.get_frag_box(0)
        draw.text((xcoord, 2150), str(
            round(div3_all_frags/div3_all_battles, 2)), color_box, font=font4)

        xcoord = 1675 - \
            tool.get_x_coord(str(int(div3_all_xp/div3_all_battles)), font4)
        draw.text((xcoord, 2281), str(int(div3_all_xp/div3_all_battles)),
                  (255, 255, 255), font=font4)

        xcoord = 1430 - \
            tool.get_x_coord(
                str(round(div3_all_planes/div3_all_battles, 2)), font4)
        color_box = tool.get_plane_box(div3_all_planes/div3_all_battles)
        draw.text((xcoord, 2281), str(round(div3_all_planes/div3_all_battles, 2)),
                  color_box, font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(0)
        div3_all_pr_box = ImageDraw.ImageDraw(img)
        div3_all_pr_box.rectangle(((1279, 1873), (1849, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 1546 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    else:
        xcoord = 1430-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2022), '0', (255, 255, 255), font=font4)

        out_wins = '0.0' + '%'
        xcoord = 1695-tool.get_x_coord(out_wins, font4)
        draw.text((xcoord, 2022), out_wins, (255, 255, 255), font=font4)

        xcoord = 1695-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2150), '0',
                  (255, 255, 255), font=font4)

        xcoord = 1430-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2150), '0', (255, 255, 255), font=font4)

        xcoord = 1675-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2281), '0',
                  (255, 255, 255), font=font4)

        xcoord = 1430-tool.get_x_coord('0', font4)
        draw.text((xcoord, 2281), '0',
                  (255, 255, 255), font=font4)

        PR, color_box, diff_pr = tool.get_pr_box(-1)
        div3_all_pr_box = ImageDraw.ImageDraw(img)
        div3_all_pr_box.rectangle(((1279, 1873), (1849, 1941)),
                                  fill=color_box, outline=None)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 1546 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1887), out_pr, (255, 255, 255), font=font4)
    # PVP type数据
    type_dict = ('AirCarrier', 'Battleship', 'Cruiser', 'Destroyer')
    type_num = 0
    while type_num < 4:
        pvp_type_battles = pvp_all_type_dict[type_dict[type_num]
                                             ]['all_battles']
        if pvp_type_battles == 0:
            xcoord = 2414-tool.get_x_coord('0', font5)
            draw.text((xcoord, 358+92*type_num), '0',
                      (255, 255, 255), font=font5)
            PR, color_box, diff_pr = tool.get_pr_box(-1)
            out_pr = PR + '(+' + str(diff_pr) + ')'
            xcoord = 2720 - tool.get_x_coord(out_pr, font4)
            draw.text((xcoord, 358+92*type_num),
                      out_pr, color_box, font=font4)

            out_wins = '0.0' + '%'
            xcoord = 3020-tool.get_x_coord(out_wins, font5)
            draw.text((xcoord, 358+92*type_num),
                      out_wins, color_box, font=font5)

            xcoord = 3270-tool.get_x_coord('0', font5)
            draw.text((xcoord, 358+92*type_num), '0',
                      color_box, font=font5)

            xcoord = 3495 - tool.get_x_coord('0', font5)
            draw.text((xcoord, 358+92*type_num), '0',
                      color_box, font=font5)

            xcoord = 3691 - tool.get_x_coord('0', font5)
            draw.text((xcoord, 358+92*type_num), '0',
                      (255, 255, 255), font=font5)
            type_num += 1
            continue

        pvp_type_damage = pvp_all_type_dict[type_dict[type_num]
                                            ]['all_damage']
        pvp_type_value_battles = pvp_all_type_dict[type_dict[type_num]
                                                   ]['all_value_battles']
        pvp_type_wins = pvp_all_type_dict[type_dict[type_num]]['all_wins']
        pvp_type_frags = pvp_all_type_dict[type_dict[type_num]]['all_frags']
        pvp_type_planes = pvp_all_type_dict[type_dict[type_num]
                                            ]['all_planes']
        pvp_type_pr = pvp_all_type_dict[type_dict[type_num]]['all_pr']
        pvp_type_n_damage = pvp_all_type_dict[type_dict[type_num]
                                              ]['all_n_damage']
        pvp_type_n_frag = pvp_all_type_dict[type_dict[type_num]
                                            ]['all_n_frag']

        xcoord = 2414-tool.get_x_coord(str(pvp_type_battles), font5)
        draw.text((xcoord, 358+92*type_num), str(pvp_type_battles),
                  (255, 255, 255), font=font5)

        if pvp_type_value_battles != 0:
            PR, color_box, diff_pr = tool.get_pr_box(
                pvp_type_pr/pvp_type_value_battles)
            out_pr = PR + '(+' + str(diff_pr) + ')'
            xcoord = 2720 - tool.get_x_coord(out_pr, font4)
            draw.text((xcoord, 358+92*type_num),
                      out_pr, color_box, font=font4)
            out_wins = str(
                round(pvp_type_wins/pvp_type_battles*100, 2)) + '%'
            xcoord = 3020-tool.get_x_coord(out_wins, font5)
            color_box = tool.get_win_box(
                pvp_type_wins/pvp_type_battles*100)
            draw.text((xcoord, 358+92*type_num),
                      out_wins, color_box, font=font5)

            xcoord = 3270 - \
                tool.get_x_coord(
                    str(int(pvp_type_damage/pvp_type_battles)), font5)
            color_box = tool.get_damage_box(
                pvp_type_n_damage/pvp_type_value_battles)
            draw.text((xcoord, 358+92*type_num), str(int(pvp_type_damage/pvp_type_battles)),
                      color_box, font=font5)

            xcoord = 3495 - \
                tool.get_x_coord(
                    str(round(pvp_type_frags/pvp_type_battles, 2)), font5)
            color_box = tool.get_frag_box(
                pvp_type_n_frag/pvp_type_value_battles)
            draw.text((xcoord, 358+92*type_num), str(round(pvp_type_frags/pvp_type_battles, 2)),
                      color_box, font=font5)

            xcoord = 3691 - \
                tool.get_x_coord(
                    str(round(pvp_type_planes/pvp_type_battles, 2)), font5)
            color_box = tool.get_plane_box(
                pvp_type_planes/pvp_type_battles)
            draw.text((xcoord, 358+92*type_num), str(round(pvp_type_planes/pvp_type_battles, 2)),
                      color_box, font=font5)
        else:
            PR, color_box, diff_pr = tool.get_pr_box(0)
            out_pr = PR + '(+' + str(diff_pr) + ')'
            xcoord = 2720 - tool.get_x_coord(out_pr, font4)
            draw.text((xcoord, 358+92*type_num),
                      out_pr, color_box, font=font4)
            out_wins = str(
                round(pvp_type_wins/pvp_type_battles*100, 2)) + '%'
            xcoord = 3020-tool.get_x_coord(out_wins, font5)
            color_box = tool.get_win_box(
                pvp_type_wins/pvp_type_battles*100)
            draw.text((xcoord, 358+92*type_num),
                      out_wins, color_box, font=font5)

            xcoord = 3270 - \
                tool.get_x_coord(
                    str(int(pvp_type_damage/pvp_type_battles)), font5)
            color_box = tool.get_damage_box(0)
            draw.text((xcoord, 358+92*type_num), str(int(pvp_type_damage/pvp_type_battles)),
                      color_box, font=font5)

            xcoord = 3495 - \
                tool.get_x_coord(
                    str(round(pvp_type_frags/pvp_type_battles, 2)), font5)
            color_box = tool.get_frag_box(0)
            draw.text((xcoord, 358+92*type_num), str(round(pvp_type_frags/pvp_type_battles, 2)),
                      color_box, font=font5)

            xcoord = 3691 - \
                tool.get_x_coord(
                    str(round(pvp_type_planes/pvp_type_battles, 2)), font5)
            color_box = tool.get_plane_box(
                pvp_type_planes/pvp_type_battles)
            draw.text((xcoord, 358+92*type_num), str(round(pvp_type_planes/pvp_type_battles, 2)),
                      color_box, font=font5)

        type_num += 1

    # RANK type数据
    type_dict = ('AirCarrier', 'Battleship', 'Cruiser', 'Destroyer')
    type_num = 0
    while type_num < 4:
        pvp_type_battles = rank_all_type_dict[type_dict[type_num]
                                              ]['all_battles']
        if pvp_type_battles == 0:
            xcoord = 2414-tool.get_x_coord('0', font5)
            draw.text((xcoord, 986+92*type_num), '0',
                      (255, 255, 255), font=font5)
            PR, color_box, diff_pr = tool.get_pr_box(-1)
            out_pr = PR + '(+' + str(diff_pr) + ')'
            xcoord = 2720 - tool.get_x_coord(out_pr, font4)
            draw.text((xcoord, 986+92*type_num), out_pr,
                      (255, 255, 255), font=font4)

            out_wins = '0.0' + '%'
            xcoord = 3020-tool.get_x_coord(out_wins, font5)
            draw.text((xcoord, 986+92*type_num), out_wins,
                      (255, 255, 255), font=font5)

            xcoord = 3270-tool.get_x_coord('0', font5)
            draw.text((xcoord, 986+92*type_num), '0',
                      (255, 255, 255), font=font5)

            xcoord = 3495 - tool.get_x_coord('0', font5)
            draw.text((xcoord, 986+92*type_num), '0',
                      (255, 255, 255), font=font5)

            xcoord = 3691 - tool.get_x_coord('0', font5)
            draw.text((xcoord, 986+92*type_num), '0',
                      (255, 255, 255), font=font5)
            type_num += 1
            continue

        pvp_type_damage = rank_all_type_dict[type_dict[type_num]
                                             ]['all_damage']
        pvp_type_wins = rank_all_type_dict[type_dict[type_num]]['all_wins']
        pvp_type_frags = rank_all_type_dict[type_dict[type_num]]['all_frags']
        pvp_type_planes = rank_all_type_dict[type_dict[type_num]
                                             ]['all_planes']
        pvp_type_pr = rank_all_type_dict[type_dict[type_num]]['all_pr']
        pvp_type_n_damage = rank_all_type_dict[type_dict[type_num]
                                               ]['all_n_damage']
        pvp_type_n_frag = rank_all_type_dict[type_dict[type_num]
                                             ]['all_n_frag']

        xcoord = 2414-tool.get_x_coord(str(pvp_type_battles), font5)
        draw.text((xcoord, 986+92*type_num), str(pvp_type_battles),
                  (255, 255, 255), font=font5)

        PR, color_box, diff_pr = tool.get_pr_box(
            pvp_type_pr/pvp_type_battles)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 2720 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 986+92*type_num), out_pr, color_box, font=font4)

        out_wins = str(round(pvp_type_wins/pvp_type_battles*100, 2)) + '%'
        xcoord = 3020-tool.get_x_coord(out_wins, font5)
        color_box = tool.get_win_box(pvp_type_wins/pvp_type_battles*100)
        draw.text((xcoord, 986+92*type_num),
                  out_wins, color_box, font=font5)

        xcoord = 3270 - \
            tool.get_x_coord(
                str(int(pvp_type_damage/pvp_type_battles)), font5)
        color_box = tool.get_damage_box(pvp_type_n_damage/pvp_type_battles)
        draw.text((xcoord, 986+92*type_num), str(int(pvp_type_damage/pvp_type_battles)),
                  color_box, font=font5)

        xcoord = 3495 - \
            tool.get_x_coord(
                str(round(pvp_type_frags/pvp_type_battles, 2)), font5)
        color_box = tool.get_frag_box(pvp_type_n_frag/pvp_type_battles)
        draw.text((xcoord, 986+92*type_num), str(round(pvp_type_frags/pvp_type_battles, 2)),
                  color_box, font=font5)

        xcoord = 3691 - \
            tool.get_x_coord(
                str(round(pvp_type_planes/pvp_type_battles, 2)), font5)
        color_box = tool.get_plane_box(pvp_type_planes/pvp_type_battles)
        draw.text((xcoord, 986+92*type_num), str(round(pvp_type_planes/pvp_type_battles, 2)),
                  color_box, font=font5)

        type_num += 1

    pvp_tier = 5
    while pvp_tier < 12:
        pvp_type_battles = pvp_all_tier_dict[pvp_tier]['all_battles']
        if pvp_type_battles == 0:
            xcoord = 2414-tool.get_x_coord('0', font5)
            draw.text((xcoord, 1610+107*(pvp_tier-5)),
                      '0', (255, 255, 255), font=font5)
            PR, color_box, diff_pr = tool.get_pr_box(-1)
            out_pr = PR + '(+' + str(diff_pr) + ')'
            xcoord = 2720 - tool.get_x_coord(out_pr, font4)
            draw.text((xcoord, 1610+107*(pvp_tier-5)),
                      out_pr, (255, 255, 255), font=font4)

            out_wins = '0.0' + '%'
            xcoord = 3020-tool.get_x_coord(out_wins, font5)
            draw.text((xcoord, 1610+107*(pvp_tier-5)),
                      out_wins, (255, 255, 255), font=font5)

            xcoord = 3270-tool.get_x_coord('0', font5)
            draw.text((xcoord, 1610+107*(pvp_tier-5)), '0',
                      (255, 255, 255), font=font5)

            xcoord = 3495 - tool.get_x_coord('0', font5)
            draw.text((xcoord, 1610+107*(pvp_tier-5)), '0',
                      (255, 255, 255), font=font5)

            xcoord = 3691 - tool.get_x_coord('0', font5)
            draw.text((xcoord, 1610+107*(pvp_tier-5)), '0',
                      (255, 255, 255), font=font5)
            pvp_tier += 1
            continue

        pvp_type_damage = pvp_all_tier_dict[pvp_tier]['all_damage']
        pvp_type_wins = pvp_all_tier_dict[pvp_tier]['all_wins']
        pvp_type_frags = pvp_all_tier_dict[pvp_tier]['all_frags']
        pvp_type_planes = pvp_all_tier_dict[pvp_tier]['all_planes']
        pvp_type_pr = pvp_all_tier_dict[pvp_tier]['all_pr']
        pvp_type_n_damage = pvp_all_tier_dict[pvp_tier]['all_n_damage']
        pvp_type_n_frag = pvp_all_tier_dict[pvp_tier]['all_n_frag']

        xcoord = 2414-tool.get_x_coord(str(pvp_type_battles), font5)
        draw.text((xcoord, 1610+107*(pvp_tier-5)), str(pvp_type_battles),
                  (255, 255, 255), font=font5)

        PR, color_box, diff_pr = tool.get_pr_box(
            pvp_type_pr/pvp_type_battles)
        out_pr = PR + '(+' + str(diff_pr) + ')'
        xcoord = 2720 - tool.get_x_coord(out_pr, font4)
        draw.text((xcoord, 1610+107*(pvp_tier-5)),
                  out_pr, color_box, font=font4)

        out_wins = str(round(pvp_type_wins/pvp_type_battles*100, 2)) + '%'
        xcoord = 3020-tool.get_x_coord(out_wins, font5)
        color_box = tool.get_win_box(pvp_type_wins/pvp_type_battles*100)
        draw.text((xcoord, 1610+107*(pvp_tier-5)),
                  out_wins, color_box, font=font5)

        xcoord = 3270 - \
            tool.get_x_coord(
                str(int(pvp_type_damage/pvp_type_battles)), font5)
        color_box = tool.get_damage_box(pvp_type_n_damage/pvp_type_battles)
        draw.text((xcoord, 1610+107*(pvp_tier-5)), str(int(pvp_type_damage/pvp_type_battles)),
                  color_box, font=font5)

        xcoord = 3495 - \
            tool.get_x_coord(
                str(round(pvp_type_frags/pvp_type_battles, 2)), font5)
        color_box = tool.get_frag_box(pvp_type_n_frag/pvp_type_battles)
        draw.text((xcoord, 1610+107*(pvp_tier-5)), str(round(pvp_type_frags/pvp_type_battles, 2)),
                  color_box, font=font5)

        xcoord = 3691 - \
            tool.get_x_coord(
                str(round(pvp_type_planes/pvp_type_battles, 2)), font5)
        color_box = tool.get_plane_box(pvp_type_planes/pvp_type_battles)
        draw.text((xcoord, 1610+107*(pvp_tier-5)), str(round(pvp_type_planes/pvp_type_battles, 2)),
                  color_box, font=font5)

        pvp_tier += 1
    # 成就数据
    cw_achieve_dict = {
        'PCH158_CLAN_LEAGUE_1': 0,
        'PCH159_CLAN_LEAGUE_2': 0,
        'PCH160_CLAN_LEAGUE_3': 0,
        'PCH161_CLAN_LEAGUE_4': 0
    }
    cw_achieve_dict['PCH161_CLAN_LEAGUE_4'] = achievement_dict['PCH161_CLAN_LEAGUE_4'],
    del(achievement_dict['PCH161_CLAN_LEAGUE_4'])
    cw_achieve_dict['PCH160_CLAN_LEAGUE_3'] = achievement_dict['PCH160_CLAN_LEAGUE_3'],
    del(achievement_dict['PCH160_CLAN_LEAGUE_3'])
    cw_achieve_dict['PCH159_CLAN_LEAGUE_2'] = achievement_dict['PCH159_CLAN_LEAGUE_2'],
    del(achievement_dict['PCH159_CLAN_LEAGUE_2'])
    cw_achieve_dict['PCH158_CLAN_LEAGUE_1'] = achievement_dict['PCH158_CLAN_LEAGUE_1'],
    del(achievement_dict['PCH158_CLAN_LEAGUE_1'])
    rank_achieve_dict = {
        'PCH232_JollyRoger': 0,
        'PCH277_JollyRogerSilver': 0,
        'PCH276_JollyRogerBronze': 0
    }
    rank_achieve_dict['PCH276_JollyRogerBronze'] = achievement_dict['PCH276_JollyRogerBronze']
    del(achievement_dict['PCH276_JollyRogerBronze'])
    rank_achieve_dict['PCH277_JollyRogerSilver'] = achievement_dict['PCH277_JollyRogerSilver']
    del(achievement_dict['PCH277_JollyRogerSilver'])
    rank_achieve_dict['PCH232_JollyRoger'] = achievement_dict['PCH232_JollyRoger']
    del(achievement_dict['PCH232_JollyRoger'])
    battle_achieve_dict = sorted(
        achievement_dict.items(), key=lambda x: x[1], reverse=True)
    achieve_num = 0
    battle_achieve_len = len(battle_achieve_dict)
    while True:
        if achieve_num >= battle_achieve_len:
            break
        achieve_name = battle_achieve_dict[achieve_num][0]
        achieve_number = battle_achieve_dict[achieve_num][1]
        if achieve_number == 0:
            break
        pic_path = os.path.dirname(
            __file__)+'\\achievement_pic\\picname.png'
        pic_path = pic_path.replace('picname', achieve_name)
        achieve_img = Image.open(pic_path)
        ycoord = int(achieve_num/5)
        xcoord = int(achieve_num % 5)
        img.paste(achieve_img, (3895+340*xcoord, 306+300*ycoord))
        xcoord = 4015+340*xcoord - \
            tool.get_x_coord(str(achieve_number), font6)
        draw.text((xcoord, 546+300*ycoord), str(achieve_number),
                  (255, 255, 255), font=font6)
        achieve_num += 1
    cw_num = 0
    for key, value in cw_achieve_dict.items():
        if int(value[0]) == 0:
            continue
        pic_path = os.path.dirname(
            __file__)+'\\achievement_pic\\picname.png'
        pic_path = pic_path.replace('picname', key)
        achieve_img = Image.open(pic_path)
        img.paste(achieve_img, (3895+340*cw_num, 2075))
        xcoord = 4015+340*cw_num - \
            tool.get_x_coord(str(int(value[0])), font6)
        draw.text((xcoord, 2295), str(
            int(value[0])), (255, 255, 255), font=font6)
        cw_num += 1
    rank_num = 0
    for key, value in rank_achieve_dict.items():
        if int(value) == 0:
            continue
        pic_path = os.path.dirname(
            __file__)+'\\achievement_pic\\picname.png'
        pic_path = pic_path.replace('picname', key)
        achieve_img = Image.open(pic_path)
        img.paste(achieve_img, (3895+340*rank_num, 1639))
        xcoord = 4015+340*rank_num - \
            tool.get_x_coord(str(int(value)), font6)
        draw.text((xcoord, 1879), str(int(value)),
                  (255, 255, 255), font=font6)
        rank_num += 1
    # 最高记录
    max_record_num = 0
    while max_record_num < 7:
        if max_record_num == 0:
            pvp_rank_dict = sorted(pvp_damage_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        elif max_record_num == 1:
            pvp_rank_dict = sorted(pvp_frag_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        elif max_record_num == 2:
            pvp_rank_dict = sorted(pvp_plane_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        elif max_record_num == 3:
            pvp_rank_dict = sorted(pvp_xp_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        elif max_record_num == 4:
            pvp_rank_dict = sorted(pvp_agro_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        elif max_record_num == 5:
            pvp_rank_dict = sorted(pvp_scouting_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        elif max_record_num == 6:
            pvp_rank_dict = sorted(pvp_spotted_rank.items(),
                                   key=lambda x: x[1], reverse=True)
        rank_num = 0
        while rank_num < 5:
            if rank_num == 0:
                color_box = (255, 240, 0)
            elif rank_num == 1:
                color_box = (208, 255, 254)
            elif rank_num == 2:
                color_box = (186, 110, 64)
            elif rank_num == 3:
                color_box = (255, 255, 255)
            elif rank_num == 4:
                color_box = (255, 255, 255)
            shipid = pvp_rank_dict[rank_num][0]
            max_record = pvp_rank_dict[rank_num][1]
            xcoord = 558+523*max_record_num - \
                tool.get_x_coord(str(max_record), font3)
            ship_name = shipinfodata[str(shipid)]['name']
            ship_tier = shipinfodata[str(shipid)]['tier']
            draw.text((xcoord, 2557+180*rank_num),
                      str(max_record), color_box, font=font3)
            out_ship_name = 'T'+str(ship_tier)+' '+ship_name
            xcoord = 558+523*max_record_num - \
                tool.get_x_coord(out_ship_name, font7)
            draw.text((xcoord, 2640+180*rank_num),
                      out_ship_name, (255, 255, 255), font=font7)
            rank_num += 1
        max_record_num += 1
    datetime = str(time.time())
    image = img.resize((2820, 1791))
    out_path = os.path.dirname(__file__)+'\\temp\\user.png'
    out_path = out_path.replace('user', datetime)
    image.save(out_path)
    return ('success', out_path)


print(wws_me(60853417, 'ru'))
