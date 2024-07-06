import time
import random

def print_intro():
    intro_text = """
    ***********************************************
    *                                             *
    *             Welcome to the                  *
    *             ULTIMATE DRINKING GAME          *
    *                                             *
    ***********************************************
    *                                             *
    *    Get ready for an unforgettable night!    *
    *                                             *
    ***********************************************
    """

    for line in intro_text.split("\n"):
        print(line)
        time.sleep(0.2)

def start_game():
    print("Starting the game... Enjoy responsibly!")

def get_alcohol_tolerance():
    while True:
        print("소주 기준 당신의 주량은?")
        print("1. 소주 반병(2잔)")
        print("2. 소주 반병에서 한병(4잔)")
        print("3. 소주 한병에서 한병 반(6잔)")
        print("4. 소주 한병 반에서 두병(8잔)")
        print("5. 소주 두병이상(10잔)")
        print("\n당신의 치사량(주량)은 얼마만큼인가요? (1~5 중에 선택하시오)")
        
        choice = input("선택 (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        else:
            print("잘못된 입력입니다. 1에서 5 사이의 숫자를 선택해주세요.")

def invite_players():
    all_players = []
    names = ["은서", "하연", "연서", "예진", "헌도"]
    
    # 메인 플레이어 추가
    name = input("오늘 거하게 취해볼 사람은?: ")
    tolerance = get_alcohol_tolerance()
    all_players.append([name, tolerance, 0, tolerance * 2])  # 이름, 주량, 현재 마신 잔 수, 남은 잔 수
    print(f"\n{name}님의 주량은 레벨 {tolerance}입니다!")
    
    # 상대 플레이어 추가
    while True:
        try:
            num_opponents = int(input("몇 명의 상대를 초대하시겠습니까? (최대 3명): "))
            if 1 <= num_opponents <= 3:
                break
            else:
                print("1에서 3 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("올바른 숫자를 입력해주세요.")
    
    for _ in range(num_opponents):
        name = random.choice(names)
        names.remove(name)
        tolerance = random.randint(1, 5)
        all_players.append([name, tolerance, 0, tolerance * 2])
    
    return all_players

def print_player_status(player):
    name, tolerance, glasses_drunk, glasses_left = player
    print(f"\n{name}의 상태:")
    print(f"주량: 레벨 {tolerance} ({tolerance * 2}잔)")
    print(f"현재까지 마신 잔 수: {glasses_drunk}")
    print(f"치사량까지 남은 잔 수: {glasses_left}")

def print_game_list():
    games = [
        "369게임",
        "숫자맞추기",
        "이순신",
        "베스킨라빈스 31"
    ]
    print("\n게임 리스트:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game}")
    return games

def select_first_player(players):
    return random.choice(players)

def play_game(game, players, selector):
    print(f"\n{game} 게임을 시작합니다!")
    if game == "369게임":
        loser = play_369(players)
    elif game == "숫자맞추기":
        loser = play_number_guess(players, selector)
    elif game == "이순신":
        loser, coins = play_lee_soon_shin(players)
        update_player_status(loser, coins)
        print(f"{loser[0]}님이 {coins}잔 마셨습니다!")
    elif game == "베스킨라빈스 31":
        loser = play_baskin_robbins(players)
    print(f"{game} 게임이 끝났습니다!")
    print(f"패자: {loser[0]}")
    return loser

def play_baskin_robbins(players):
    current_number = 0
    
    while current_number < 31:
        for player in players:
            if player[0] == players[0][0]:  # 사용자 차례
                while True:
                    try:
                        count = int(input("1에서 3 사이의 숫자를 입력하세요: "))
                        if 1 <= count <= 3:
                            break
                        else:
                            print("1에서 3 사이의 숫자만 입력할 수 있습니다.")
                    except ValueError:
                        print("올바른 숫자를 입력해주세요.")
            else:  # 참여자 차례
                count = random.randint(1, 3)
                print(f"{player[0]}의 선택: {count}")
            
            for i in range(count):
                current_number += 1
                print(f"{current_number}", end=" ")
                if current_number >= 31:
                    print(f"\n{player[0]}이(가) 31을 불렀습니다!")
                    return player
            print()

def play_369(players):
    current_number = 1
    while True:
        for player in players:
            if player[0] == players[0][0]:  # 사용자 차례
                user_input = input(f"{current_number}에 해당하는 값을 입력하세요 (숫자 또는 '짝'): ")
                if '3' in str(current_number) or '6' in str(current_number) or '9' in str(current_number):
                    if user_input != '짝':
                        print("틀렸습니다! '짝'을 입력해야 합니다.")
                        return player
                elif user_input != str(current_number):
                    print(f"틀렸습니다! {current_number}를 입력해야 합니다.")
                    return player
            else:  # 참여자 차례
                if '3' in str(current_number) or '6' in str(current_number) or '9' in str(current_number):
                    if random.random() < 0.5:  # 50% 확률로 실수
                        print(f"{player[0]}가 실수했습니다!")
                        return player
                    else:
                        print(f"{player[0]}: 짝")
                else:
                    print(f"{player[0]}: {current_number}")
            
            current_number += 1
            if current_number > 50:  # 게임 종료 조건
                return random.choice(players)

def play_number_guess(players, selector):
    target_number = random.randint(1, 20)
    print(f"1부터 20 사이의 숫자가 정해졌습니다.")
    
    playing_players = [p for p in players if p[0] != selector[0]]
    
    while True:
        for player in playing_players:
            if player[0] == players[0][0]:  # 사용자 차례
                while True:
                    try:
                        guess = int(input("1부터 20 사이의 숫자를 맞춰보세요: "))
                        if 1 <= guess <= 20:
                            break
                        else:
                            print("1부터 20 사이의 숫자를 입력해주세요.")
                    except ValueError:
                        print("올바른 숫자를 입력해주세요.")
            else:  # 참여자 차례
                guess = random.randint(1, 20)
                print(f"{player[0]}의 추측: {guess}")
            
            if guess == target_number:
                return player
            elif guess < target_number:
                print("업!")
            else:
                print("다운!")

def play_lee_soon_shin(players):
    coins = 0
    current_player_index = 0
    
    while True:
        current_player = players[current_player_index]
        
        if current_player[0] == players[0][0]:  # 사용자 차례
            choice = input(f"현재 {coins}잔입니다. 동전을 던지시겠습니까? (y/n): ").lower()
            if choice == 'y':
                coins += 1
            elif choice == 'n':
                current_player_index = (current_player_index + 1) % len(players)
                continue
        else:  # 참여자 차례
            if random.random() < 0.5:
                coins += 1
                print(f"{current_player[0]}가 동전을 던집니다. 현재 {coins}잔입니다.")
            else:
                print(f"{current_player[0]}가 동전을 던지지 않습니다.")
                current_player_index = (current_player_index + 1) % len(players)
                continue
        
        if random.random() < 0.5:  # 앞면
            print("앞면이 나왔습니다!")
            return current_player, coins
        else:  # 뒷면
            print("뒷면이 나왔습니다.")
            current_player_index = (current_player_index + 1) % len(players)

def update_player_status(player, drinks):
    player[2] += drinks  # glasses_drunk 증가
    player[3] -= drinks  # glasses_left 감소
    print_player_status(player)

def main():
    print_intro()
    
    while True:
        user_input = input("Do you want to start the game? (y/n): ").strip().lower()
        if user_input == 'y':
            start_game()
            break
        elif user_input == 'n':
            print("Exiting the game. Have a great day!")
            return
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
    
    try:
        all_players = invite_players()
    except ValueError:
        print("잘못된 입력입니다. 프로그램을 다시 실행해주세요.")
        return
    
    print("\n참가자 목록:")
    for player in all_players:
        print(f"{player[0]} (주량 레벨: {player[1]})")
    
    for player in all_players:
        print_player_status(player)
    
    games = print_game_list()

    game_round = 1
    while all(player[3] > 0 for player in all_players):
        print(f"\n===== 라운드 {game_round} =====")
        
        first_player = select_first_player(all_players)
        print(f"\n{first_player[0]}님이 게임을 선택합니다.")
        
        if first_player[0] == all_players[0][0]:  # 사용자인 경우
            while True:
                try:
                    game_choice = int(input("게임 번호를 선택하세요: "))
                    if 1 <= game_choice <= len(games):
                        selected_game = games[game_choice - 1]
                        break
                    else:
                        print("올바른 게임 번호를 선택해주세요.")
                except ValueError:
                    print("숫자를 입력해주세요.")
        else:
            selected_game = random.choice(games)
        
        print(f"\n{first_player[0]}님이 {selected_game}을(를) 선택했습니다.")
        
        loser = play_game(selected_game, all_players, first_player)
        update_player_status(loser, 1)  # 패자는 1잔을 마심
        
        if loser[3] <= 0:
            print(f"\n{loser[0]}님이 치사량에 도달했습니다!")
            break
        
        game_round += 1
    
    print("\n게임이 종료되었습니다!")
    print("최종 결과:")
    for player in all_players:
        print_player_status(player)

if __name__ == "__main__":
    main()