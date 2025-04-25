import random
import time

class Pokemon:
    def __init__(self, name, type, health, level=0, status=""):
        self.name = name
        self.type = type
        self.health = health
        self.level = level
        self.status = status

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

def create_deck():
    return [
        Pokemon("皮卡丘", "電", 100, level=50),
        Pokemon("小火龍", "火", 100, level=50),
        Pokemon("傑尼龜", "水", 100, level=50),
        Pokemon("妙蛙種子", "草", 100, level=50),
        Pokemon("伊布", "一般", 100, level=50),
        Pokemon("胖丁", "妖精", 100, level=50),
        Pokemon("喵喵", "一般", 100, level=50),
        Pokemon("可達鴨", "水", 100, level=50),
        Pokemon("腕力", "格鬥", 100, level=50),
        Pokemon("小拳石", "岩石", 100, level=50),
    ]

def calculate_damage(attacker, defender):
    # 基礎傷害值（20~30 隨機）
    base_damage = random.randint(20, 30)
    
    # 屬性相剋表 (攻擊方 -> 防守方 -> 倍率)
    type_effectiveness = {
        "電": {"水": 2.0, "草": 0.5, "電": 0.5, "地": 0.0, "飛行": 2.0},
        "火": {"草": 2.0, "水": 0.5, "火": 0.5, "冰": 2.0, "蟲": 2.0},
        "水": {"火": 2.0, "草": 0.5, "水": 0.5, "地": 2.0, "岩石": 2.0},
        "草": {"水": 2.0, "火": 0.5, "草": 0.5, "地": 2.0, "毒": 0.5},
        "一般": {"岩石": 0.5, "幽靈": 0.0, "鋼": 0.5},
        "格鬥": {"一般": 2.0, "岩石": 2.0, "鋼": 2.0, "冰": 2.0, "幽靈": 0.0, "毒": 0.5, "飛行": 0.5, "超能力": 0.5, "蟲": 0.5},
        "岩石": {"火": 2.0, "冰": 2.0, "飛行": 2.0, "蟲": 2.0, "格鬥": 0.5, "地": 0.5, "鋼": 0.5},
        "妖精": {"格鬥": 2.0, "龍": 2.0, "黑暗": 2.0, "毒": 0.5, "鋼": 0.5, "火": 0.5}
    }
    
    # 獲取攻擊方和防守方的屬性
    attacker_type = attacker.type
    defender_type = defender.type
    
    # 計算屬性相剋加成
    effectiveness = 1.0
    if attacker_type in type_effectiveness:
        if defender_type in type_effectiveness[attacker_type]:
            effectiveness = type_effectiveness[attacker_type][defender_type]
    
    # 計算最終傷害值
    final_damage = int(base_damage * effectiveness)
    
    # 根據等級調整傷害值
    level_factor = 1.0 + (attacker.level / 100)
    final_damage = int(final_damage * level_factor)
    
    # 確保傷害至少為1
    if final_damage < 1 and effectiveness > 0:
        final_damage = 1
    
    return final_damage

def display_battle_status(turn, player_name, player_pokemon, ai_name, ai_pokemon, player_hand, ai_hand, battle_logs):
    print("--------------------------------------------------------------------------------")
    print(f"                                   回合 {turn}")
    print("--------------------------------------------------------------------------------")

    print(f"[{player_name}]")
    print(f"寶可夢: {player_pokemon.name}({player_pokemon.type})")
    print(f"生命值: {player_pokemon.health}%")
    print(f"剩餘寶可夢: {', '.join([f'{p.name}({p.type})' for p in player_hand])}")
    print("")
    print("VS")
    print("")
    print(f"[{ai_name}]")
    print(f"寶可夢: {ai_pokemon.name}({ai_pokemon.type})")
    print(f"生命值: {ai_pokemon.health}%")
    print(f"剩餘寶可夢: {', '.join([f'{p.name}({p.type})' for p in ai_hand])}")
    print("--------------------------------------------------------------------------------")
    # 輸出戰鬥過程（最多五行）
    for log in battle_logs[-7:]:
        print(log)
    for _ in range(7 - len(battle_logs[-7:])):
        print("")
    print("")
    print("")

def player_turn(player_pokemon, ai_pokemon, player_hand):
    action = input("選擇動作: (1) 攻擊 (2) 更換寶可夢？")
    log = ""
    if action == "1":
        # 判斷屬性相剋決定 miss 機率
        type_effectiveness = 1.0
        if hasattr(player_pokemon, 'type') and hasattr(ai_pokemon, 'type'):
            # 與 calculate_damage 裡一致
            type_chart = {
                "火": {"草": 2, "水": 0.5, "電": 1, "火": 0.5, "一般": 1},
                "水": {"火": 2, "草": 0.5, "電": 1, "水": 0.5, "一般": 1},
                "草": {"水": 2, "火": 0.5, "電": 1, "草": 0.5, "一般": 1},
                "電": {"水": 2, "草": 0.5, "火": 1, "電": 0.5, "一般": 1},
                "一般": {"火": 1, "水": 1, "草": 1, "電": 1, "一般": 1},
            }
            atk_type = player_pokemon.type
            def_type = ai_pokemon.type
            if atk_type in type_chart and def_type in type_chart[atk_type]:
                type_effectiveness = type_chart[atk_type][def_type]
        miss_rate = 0.3 if type_effectiveness < 1 else 0.1
        miss = random.random() < miss_rate
        attacker_str = f"玩家的{player_pokemon.name}"
        defender_str = f"AI的{ai_pokemon.name}"
        if miss:
            log = f"{defender_str} 躲過了攻擊！"
        else:
            # 暴擊機率 10%
            is_critical = random.random() < 0.1
            damage = calculate_damage(player_pokemon, ai_pokemon)
            if is_critical:
                log = f"\033[31m暴擊!\033[0m {attacker_str} 攻擊 {defender_str} 造成 {damage * 2} 點傷害!"
                damage *= 2
            else:
                log = f"{attacker_str} 攻擊 {defender_str} 造成 {damage} 點傷害!"
            ai_pokemon.take_damage(damage)
        print(log)
    elif action == "2" and len(player_hand) > 1:
        print("選擇要更換的寶可夢:")
        for i, pokemon in enumerate(player_hand):
            if pokemon != player_pokemon:
                print(f"{i + 1}. {pokemon.name} (屬性: {pokemon.type}, 生命值: {pokemon.health})")
        selected_index = int(input("輸入要更換的寶可夢編號: ")) - 1
        player_pokemon = player_hand[selected_index]
        log = f"玩家\033[34m更換\033[0m寶可夢為{player_pokemon.name}"
        print(log)
    else:
        log = "沒有其他寶可夢可以更換!"
        print(log)
    return player_pokemon, log

def ai_turn(ai_pokemon, player_pokemon, ai_hand):
    action = random.choice(["attack", "switch"])
    log = ""
    new_ai_pokemon = ai_pokemon
    if action == "attack":
        # 判斷屬性相剋決定 miss 機率
        type_effectiveness = 1.0
        if hasattr(ai_pokemon, 'type') and hasattr(player_pokemon, 'type'):
            type_chart = {
                "火": {"草": 2, "水": 0.5, "電": 1, "火": 0.5, "一般": 1},
                "水": {"火": 2, "草": 0.5, "電": 1, "水": 0.5, "一般": 1},
                "草": {"水": 2, "火": 0.5, "電": 1, "草": 0.5, "一般": 1},
                "電": {"水": 2, "草": 0.5, "火": 1, "電": 0.5, "一般": 1},
                "一般": {"火": 1, "水": 1, "草": 1, "電": 1, "一般": 1},
            }
            atk_type = ai_pokemon.type
            def_type = player_pokemon.type
            if atk_type in type_chart and def_type in type_chart[atk_type]:
                type_effectiveness = type_chart[atk_type][def_type]
        miss_rate = 0.3 if type_effectiveness < 1 else 0.1
        miss = random.random() < miss_rate
        attacker_str = f"AI的{ai_pokemon.name}"
        defender_str = f"玩家的{player_pokemon.name}"
        if miss:
            log = f"{defender_str} 躲過了攻擊！"
        else:
            # 暴擊機率 10%
            is_critical = random.random() < 0.1
            damage = calculate_damage(ai_pokemon, player_pokemon)
            if is_critical:
                log = f"\033[31m暴擊!\033[0m {attacker_str} 攻擊 {defender_str} 造成 {damage * 2} 點傷害!"
                damage *= 2
            else:
                log = f"{attacker_str} 攻擊 {defender_str} 造成 {damage} 點傷害!"
            player_pokemon.take_damage(damage)
        print(log)
    elif action == "switch":
        # 從 ai_hand 選擇不是當前 ai_pokemon 的寶可夢
        candidates = [p for p in ai_hand if p != ai_pokemon]
        if candidates:
            new_ai_pokemon = random.choice(candidates)
            log = f"AI\033[34m更換\033[0m寶可夢為{new_ai_pokemon.name}"
        else:
            log = f"AI沒有其他寶可夢可以更換!"
        print(log)
    return log, new_ai_pokemon

def game_loop():
    player_deck = create_deck()
    ai_deck = create_deck()
    player_hand = random.sample(player_deck, 3)
    ai_hand = random.sample(ai_deck, 3)
    player_pokemon = player_hand[0]
    ai_pokemon = ai_hand[0]
    turn = 1
    battle_logs = []
    player_name = "Player"
    ai_name = "AI"

    while player_hand and ai_hand:
        display_battle_status(turn, player_name, player_pokemon, ai_name, ai_pokemon, player_hand, ai_hand, battle_logs)
        player_pokemon, log = player_turn(player_pokemon, ai_pokemon, player_hand)
        battle_logs.append(log)
        # 立即顯示玩家行動結果
        display_battle_status(turn, player_name, player_pokemon, ai_name, ai_pokemon, player_hand, ai_hand, battle_logs)
        time.sleep(2)
        if not ai_pokemon.is_alive():
            log = f"AI的{ai_pokemon.name} 被擊敗了!"
            print(log)
            battle_logs.append(log)
            ai_hand.remove(ai_pokemon)
            if ai_hand:
                ai_pokemon = ai_hand[0]
            else:
                log = "AI 沒有寶可夢了! 你獲勝!"
                print(log)
                battle_logs.append(log)
                break

        if ai_pokemon.is_alive():
            log, new_ai_pokemon = ai_turn(ai_pokemon, player_pokemon, ai_hand)
            if new_ai_pokemon != ai_pokemon:
                ai_pokemon = new_ai_pokemon
            battle_logs.append(log)
            # 顯示AI行動結果
            display_battle_status(turn, player_name, player_pokemon, ai_name, ai_pokemon, player_hand, ai_hand, battle_logs)
            if not player_pokemon.is_alive():
                log = f"玩家的{player_pokemon.name} 被擊敗了!"
                print(log)
                battle_logs.append(log)
                player_hand.remove(player_pokemon)
                if player_hand:
                    player_pokemon = player_hand[0]
                else:
                    log = "你沒有寶可夢了! 你輸了!"
                    print(log)
                    battle_logs.append(log)
                    break

        turn += 1
if __name__ == "__main__":
    game_loop() 