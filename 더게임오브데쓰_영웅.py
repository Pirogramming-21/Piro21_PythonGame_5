import random

def theGameofDeath(players):
    if not (2 <= len(players) <= 4):
        print("플레이어 수는 최소 2명에서 최대 4명이어야 합니다.")
        return

    # 각 플레이어가 지목할 사람 설정 (자신을 제외한 다른 플레이어)
    target_list = []
    for name in players:
        valid_targets = [p for p in players if p != name]
        target = random.choice(valid_targets)
        target_list.append(target)
    
    print("\n각 플레이어가 지목할 사람 설정 완료:")
    for idx, target in enumerate(target_list):
        print(f"{players[idx]} -> {target}")

    # 시작할 플레이어 선정
    current_player = random.choice(players)
    print(f"\n{current_player}님이 시작합니다.")

    # 라운드 진행
    if current_player == players[0]:  # 사용자가 시작자일 경우
        death_number = int(input(f"{current_player}의 차례입니다. 죽음의 번호를 입력하세요 (2-10): "))
        while death_number < 2 or death_number > 10:
            death_number = int(input("잘못된 입력입니다. 죽음의 번호를 2-10 사이로 입력하세요: "))
    else:
        death_number = random.randint(2, 10)
        print(f"{current_player}의 차례입니다. 죽음의 번호는 {death_number}입니다.")

    print(f"\n죽음의 숫자는 {death_number}입니다.\n")

    count = 1
    current_index = players.index(current_player)
    print(f"카운트 시작: {current_player}")

    while count <= death_number:
        next_player = target_list[current_index]
        print(f"카운트 {count}: {players[current_index]} -> {next_player}")
        current_index = players.index(next_player)
        count += 1

    eliminated_player = players[current_index]
    print(f"\nPlayer {eliminated_player} is eliminated.")
    return eliminated_player

# 게임 설정
player_names = input("플레이어 이름을 쉼표로 구분하여 입력하세요 (예: Alice,Bob,Charlie,David): ").split(',')

# 게임 시작
eliminated_player = theGameofDeath(player_names)
print(f"\n탈락한 플레이어: {eliminated_player}")
