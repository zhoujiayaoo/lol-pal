import sqlite3
import time
import json
import win32api
import win32con

from configUtils import conf


# 显示弹框
def  show_message_box(pal_list, me_team):
    print("我的队伍：", me_team)
    box_str = ""
    for item in pal_list:
        this_game = item['this_game']
        before_game = item['before_game']
        player_team = "敌方"
        if str(item['this_game'][3]) == str(me_team):
            player_team = "己方"
        box_str_item = "[{}]【{}】（{}）是[ {} ]场前[{}]【{}】，{}次相遇\n".format(player_team, this_game[1], this_game[2], item['how_long'],
                                                               before_game['team'], before_game['player_hero'], before_game['frequency'])
        # print(box_str_item)
        box_str = box_str + box_str_item
    # print(pal_list)
    win32api.MessageBox(None, box_str, "遇见熟人", win32con.MB_SYSTEMMODAL)


# 保存游戏数据
def insert_game_info(json_str):
    conn = sqlite3.connect('resources/db.db')
    cursor = conn.cursor()
    words_result_num = json.loads(json_str)['words_result_num']
    if words_result_num < 20:
        print("检测数据异常，请勿胡乱操作!")
        return
    json_obj = json.loads(json_str)['words_result']
    # manyData可以是二维列表、元组或者迭代器
    data = (str(time.time()),)
    cursor.execute('INSERT INTO game (game_time) VALUES (?)', data)
    conn.commit()
    game_id = cursor.lastrowid
    pal_list = []
    my_team = ""
    for i in range(10):
        player_name = json_obj[i + 10]['words']
        pal_info = query_pal(player_name)
        team = "blue"
        if i + 10 >= 15:
            team = "red"
        data = (game_id, json_obj[i]['words'], player_name, team, pal_info['player_type'],)
        if pal_info['player_type'] == "ME":
            my_team = team
        if pal_info['player_type'] == "PAL":
            pal_item = {'this_game': data, 'before_game': pal_info, 'how_long': game_id - pal_info['game_id']}
            pal_list.append(pal_item)
        cursor.execute('INSERT INTO player (game_id, hero, player_name, team, player_type) VALUES (?,?,?,?,?)', data)
        conn.commit()
    conn.close()
    if len(pal_list) > 0:
        # 如果有熟人则弹窗显示
        show_message_box(pal_list, my_team)
    else:
        win32api.MessageBox(None, "没有熟人", "没有熟人", win32con.MB_SYSTEMMODAL)

# 查询是否是熟人
def query_pal(player_name):
    conn = sqlite3.connect('resources/db.db')
    cursor = conn.cursor()
    data = (player_name, "PASSER", "PAL",)
    cursor.execute('SELECT * FROM player where player_name = ? AND (player_type = ? OR player_type = ?) '
                   'ORDER BY player_id DESC', data)
    values = cursor.fetchall()
    player_type = "PASSER"
    if len(values) > 0:
        player_type = "PAL"
        player_item = values[0]
        data = (player_item[1], 'ME', )
        cursor.execute('''
            SELECT team FROM player as p
            LEFT JOIN game as g ON p.game_id = g.game_id
            WHERE p.game_id = ? AND p.player_type = ?
        ''', data)
        team_values = cursor.fetchall()
        my_team = team_values[0][0]
        # print("me_team: ", my_team)
        team = "敌方"
        if my_team == player_item[4]:
            team = "已方"
        return_data = {'player_type': player_type, 'player_hero': player_item[2], 'team': team,
                       'frequency': len(values), 'game_id': player_item[1]}
    else:
        ME = str(conf.get("me", "me"))
        if player_name == ME:
            player_type = "ME"
        if player_name == "DFLMG" or player_name == "我太孤单12":
            player_type = "MY_FRIEND"
        return_data = {'player_type': player_type}
    return return_data


if __name__ == '__main__':
    # query_pal("社会你啊建哥")
    insert_game_info(
        '''{"words_result":[{"words":"SSW辛吉德"},{"words":"暗黑女武神黛安娜"},{"words":"大发明家"},{"words":"奥术大师吉格斯"},{"words":"最后一只恐龙纳尔"},{"words":"冰川巨兽墨菲特"},{"words":"社会名流乐芙兰"},{"words":"创世之神赫卡里姆"},{"words":"腥红之月派克"},{"words":"蓝焰梦魔魔腾"},{"words":"DFLMG"},{"words":"Flora剪影"},{"words":"长剑起舞"},{"words":"浮暮幽影丶汐"},{"words":"墨竹Merry"},{"words":"被子忘盖人被伦"},{"words":"深沉阿灿"},{"words":"时光偷走的回忆"},{"words":"1656360177"},{"words":"ROSE成风"}],"words_result_num":20,"log_id":1617176471289637428}''')
    # box_str = "[队友]【麦林炮手-大叔你好】是上1把游戏[队友]【皎月女神】\n[队友]【麦林炮手-大叔你好】是上1把游戏[队友]【皎月女神】\n[队友]【麦林炮手-大叔你好】是上1把游戏[队友]【皎月女神】\n[队友]【麦林炮手-大叔你好】是上1把游戏[队友]【皎月女神】"
    # win32api.MessageBox(0, box_str, "检测到熟人", win32con.MB_OK)
