import threading
import time
import random

def play_007_game(players):
    print("\n공공칠빵 게임을 시작합니다!")
    print("시작자가 손가락으로 자신의 앞에 007가방을 그립니다.")
    
    current_player = random.choice(players)
    print(f"{current_player[0]}님이 시작합니다.")
    
    sequence = ["공", "공", "칠", "빵"]
    seq_index = 0

    def timer_expired():
        nonlocal timer_expired_flag
        timer_expired_flag = True

    while True:
        if current_player[0] == players[0][0]:  # 사용자 차례
            while True:
                user_input = input(f"{sequence[seq_index]}을(를) 말하고 다음 플레이어를 지목하세요 (예: 공 이름): ").split()
                if len(user_input) != 2 or user_input[0] != sequence[seq_index]:
                    print(f"올바른 형식으로 입력해주세요. '{sequence[seq_index]} 플레이어이름' 형식으로 입력하세요.")
                    continue
                next_player_name = user_input[1]
                next_player = next((p for p in players if p[0] == next_player_name), None)
                if next_player:
                    break
                else:
                    print("올바른 플레이어 이름을 입력해주세요.")
        else:  # AI 플레이어 차례
            print(f"{current_player[0]}: {sequence[seq_index]}")
            time.sleep(1)
            next_player = random.choice([p for p in players if p != current_player])
        
        print(f"{current_player[0]}님이 {next_player[0]}님을 지목했습니다.")
        
        if seq_index == 3:  # "빵" 다음 차례
            left_player = players[(players.index(next_player) - 1) % len(players)]
            right_player = players[(players.index(next_player) + 1) % len(players)]
            
            timer_expired_flag = False
            timer = threading.Timer(3.0, timer_expired)
            timer.start()

            if left_player[0] == players[0][0] or right_player[0] == players[0][0]:
                user_input = input("3초 안에 '으악'을 외치고 손을 들어야 합니다. 준비되셨나요? (y 입력): ")
                if user_input.lower() != 'y' or timer_expired_flag:
                    timer.cancel()
                    print("시간 초과 또는 잘못된 입력!")
                    return next_player
            else:
                time.sleep(random.uniform(0.5, 2.5))  # AI 반응 시간
                if random.random() < 0.3 or timer_expired_flag:  # 30% 확률로 AI가 실수 또는 시간 초과
                    timer.cancel()
                    print(f"{left_player[0]} 또는 {right_player[0]}가 제 시간에 반응하지 못했습니다!")
                    return random.choice([left_player, right_player])
            
            timer.cancel()
            print(f"{left_player[0]}와 {right_player[0]}: 으악!")

        seq_index = (seq_index + 1) % 4
        current_player = next_player

    return current_player