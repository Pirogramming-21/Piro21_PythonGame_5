import threading
import time
import random

from pyfiglet import Figlet
import random

def print_intro():

    f = Figlet(font='block', width=400)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')
    time.sleep(0.7)
    print(f.renderText('! ALCOHOL GAME !'))
    time.sleep(0.7) 
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print("")
    print('                             안주🍗먹을 시간⏱️이 없어요~❌❌ 마시면서 배우는 술게임 🍻🍺😵‍💫')
    print("")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')


##-게임 세팅 ----------------------------------------------------------------------


def start_game():
    f = Figlet(font='straight', width=400,)
    print(f.renderText("Starting the game... Enjoy responsibly!\n"))

def invite_players():
    all_players = []
    names = ["의진", "지현", "영웅", "다예", "태연"]
    
def get_alcohol_tolerance():
    while True:
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~🍺 소주 기준 당신의 주량은? 🍺~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('                                          🍺 1. 소주 반병 (2잔)')
        print('                                          🍺 2. 소주 반병에서 한병 (4잔)')
        print('                                          🍺 3. 소주 한병에서 한병 반 (6잔)')
        print('                                          🍺 4. 소주 한병 반에서 두병 (8잔)')
        print('                                          🍺 5. 소주 두병 이상 (10잔)')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        choice = input("당신의 치사량(주량)은 얼마만큼인가요? (1~5를 선택해주세요): ").strip()
        
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        else:
            print("잘못된 입력입니다. 1에서 5 사이의 숫자를 선택해주세요.")

def invite_players():
    all_players = []
    names = ["의진", "지현", "영웅", "다예", "태연"]
    
    # 메인 플레이어 추가
    name = input("오늘 거하게 취해볼 당신의 이름은?: ")
    if name in names:
        names.remove(name)
    tolerance = get_alcohol_tolerance()
    all_players.append([name, tolerance, 0, tolerance * 2])  # 이름, 주량, 현재 마신 잔 수, 남은 잔 수
    print(f"{name}님의 주량은 레벨 {tolerance}입니다!")
    
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

##-게임 상태 출력----------------------------------------------------------------

def print_player_status(player):
    name, tolerance, glasses_drunk, glasses_left = player
    glasses_drunk_emoji = '🍺' * glasses_drunk  # 마신 잔 수를 이모티콘으로 변환
    glasses_left_emoji = '🍺' * glasses_left  # 남은 잔 수를 이모티콘으로 변환
    
    print(f"\n{name}의 상태:")
    print(f"주량: 레벨 {tolerance} ({tolerance * 2}잔)")
    print(f"현재까지 마신 잔 수: {glasses_drunk_emoji} ({glasses_drunk}잔)")
    print(f"치사량까지 남은 잔 수: {glasses_left_emoji} ({glasses_left}잔)")

##-게임 시작 & 종료-------------------------------------------------------------------

def print_game_list():
    games = [
        "369게임",
        "지하철 게임",
        "공공칠빵 게임",
        "더게임오브데쓰",
        "만두게임"
    ]
    print("\n게임 리스트:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game}")
    return games

def select_first_player(players):
    return random.choice(players)

def play_game(game, players, selector):
    print(f"\n{game} 을 시작합니다!\n")
    if game == "369게임":
        loser = play_369(players)
    elif game == "지하철 게임":
        loser = play_subway_game(players, selector)
    elif game == "공공칠빵 게임":
        loser = play_007_game(players)
    elif game == "더게임오브데쓰":
        loser = theGameofDeath(players,selector)
    elif game == "만두게임":
        loser = play_mando_game(players)

    print(f"\n{game} 이 끝났습니다!")
    print(f"\n🚨 패자: {loser[0]}")
    return loser

##-게임 1. 369 ---------------------------------------------------------------------

def play_369(players):
    current_number = 1
    
    def timer_expired():
        nonlocal timer_expired_flag
        timer_expired_flag = True

    def get_correct_answer(number):
        if number in [33, 66, 99]:
            return '짝짝'
        elif '3' in str(number) or '6' in str(number) or '9' in str(number):
            return '짝'
        else:
            return str(number)

    while True:
        for player in players:
            print(f"\n{player[0]}의 차례입니다. (현재 숫자: {current_number})")
            
            timer_expired_flag = False
            timer = threading.Timer(5.0, timer_expired)
            timer.start()

            correct_answer = get_correct_answer(current_number)

            if player[0] == players[0][0]:  # 사용자 차례
                user_input = input(f"{current_number}에 해당하는 값을 입력하세요 (숫자, '짝' 또는 '짝짝') (제한 시간 5초): ")
            else:  # AI 플레이어 차례
                time.sleep(random.uniform(1, 3))  # AI가 생각하는 시간
                if random.random() < 0.7:  # 70% 확률로 정답
                    user_input = correct_answer
                else:  # 30% 확률로 오답
                    wrong_answers = ['짝', '짝짝', str(current_number)]
                    wrong_answers.remove(correct_answer)
                    user_input = random.choice(wrong_answers)
                print(f"{player[0]}의 선택: {user_input}")

            timer.cancel()

            if timer_expired_flag:
                print("시간 초과!")
                return player

            if user_input != correct_answer:
                print(f"틀렸습니다! 정답은 '{correct_answer}'입니다.")
                return player
            
            current_number += 1
            if current_number > 50:  # 게임 종료 조건
                return random.choice(players)
            
##-게임 2. 지하철 게임 ---------------------------------------------------------------------
          
def play_subway_game(players, selector):
    subway_lines = {
        '1호선': ['인천', '동인천', '도원', '제물포', '도화', '주안', '간석', '동암', '백운', '부평', '부개', '송내', '중동', '부천', '소사', '역곡', '온수', '오류동', '개봉', '구일', '구로', '신도림', '영등포', '신길', '대방', '노량진', '용산', '남영', '서울역', 
                '시청', '종각', '종로3가', '종로5가', '동대문', '동묘앞', '신설동', '제기동', '청량리', '회기', '외대앞', '신이문', '석계', '광운대', '월계', '녹천', '창동', '방학', '도봉', '도봉산', '망월사', '회룡', '의정부', '가능', '녹양', '양주', 
                '덕계', '덕정', '지행', '동두천중앙', '보산', '동두천', '소요산', '가산디지털단지', '독산', '금천구청', '석수', '관악', '안양', '명학', '금정', '군포', '당정', '의왕', '성균관대', '화서', '수원', '세류', '병점', '서동탄', '세마', '오산대', 
                '오산', '진위', '송탄', '서정리', '지제', '평택', '성환', '직산', '두정', '천안', '봉명', '쌍용', '아산', '탕정', '배방', '온양온천', '신창'],
        '2호선': ['시청', '을지로입구', '을지로3가', '을지로4가', '동대문역사문화공원', '신당', '상왕십리', '왕십리', '한양대', '뚝섬', '성수', '건대입구', '구의', '강변', '잠실나루', '잠실', '잠실새내', '종합운동장', '삼성', '선릉', '역삼', '강남', 
                '교대', '서초', '방배', '사당', '낙성대', '서울대입구', '봉천', '신림', '신대방', '구로디지털단지', '대림', '신도림', '문래', '영등포구청', '당산', '합정', '홍대입구', '신촌', '이대', '아현', '충정로', '까치산', '신정네거리', '양천구청', '도림천'],
        '3호선': ['대화', '주엽', '정발산', '마두', '백석', '대곡', '화정', '원당', '원흥', '삼송', '지축', '구파발', '연신내', '불광', '녹번', '홍제', '무악재', '독립문', '경복궁', '안국', '종로3가', '을지로3가', '충무로', '동대입구', '약수', '금호', '옥수', '압구정', 
                '신사', '잠원', '고속터미널', '교대', '남부터미널', '양재', '매봉', '도곡', '대치', '학여울', '대청', '일원', '수서', '가락시장', '경찰병원', '오금'],
        '4호선': ['당고개', '상계', '노원', '창동', '쌍문', '수유', '미아', '미아사거리', '길음', '성신여대입구', '한성대입구', '혜화', '동대문', '동대문역사문화공원', '충무로', '명동', '회현', '서울역', '숙대입구', '삼각지', '신용산', '이촌', '동작', '총신대입구', 
                '사당', '남태령', '선바위', '경마공원', '대공원', '과천', '정부과천청사', '인덕원', '평촌', '범계', '금정', '산본', '수리산', '대야미', '반월', '상록수', '한대앞', '중앙', '고잔', '초지', '안산', '신길온천', '정왕', '오이도'],
        '5호선': ['방화', '개화산', '김포공항', '송정', '마곡', '발산', '우장산', '화곡', '까치산', '신정', '목동', '오목교', '양평', '영등포구청', '영등포시장', '신길', '여의도', '여의나루', '마포', '공덕', '애오개', '충정로', '서대문', '광화문', '종로3가', 
                '을지로4가', '동대문역사문화공원', '청구', '신금호', '행당', '왕십리', '마장', '답십리', '장한평', '군자', '아차산', '광나루', '천호', '강동', '둔촌동', '올림픽공원', '방이', '오금', '개롱', '거여', '마천', '강일', '미사', '하남풍산', 
                '하남시청', '하남검단산', '명일', '고덕', '상일동', '길동', '굽은다리', '명일'],
        '6호선': ['응암', '역촌', '불광', '독바위', '연신내', '구산', '디지털미디어시티', '월드컵경기장', '마포구청', '망원', '합정', '상수', '광흥창', '대흥', '공덕', '효창공원앞', '삼각지', '녹사평', '이태원', '한강진', '버티고개', '약수', '청구', '신당', '동묘앞', '창신', 
                '보문', '안암', '고려대', '월곡', '상월곡', '돌곶이', '석계', '태릉입구', '화랑대', '봉화산', '신내'],
        '7호선': ['장암', '도봉산', '수락산', '마들', '노원', '중계', '하계', '공릉', '태릉입구', '먹골', '중화', '상봉', '면목', '사가정', '용마산', '중곡', '군자', '어린이대공원', '건대입구', '뚝섬유원지', '청담', '강남구청', '학동', '논현', '반포', '고속터미널', 
                '내방', '이수', '남성', '숭실대입구', '상도', '장승배기', '신대방삼거리', '보라매', '신풍', '대림', '가산디지털단지', '철산', '광명사거리', '천왕', '온수', '까치울', '부천종합운동장', '춘의', '신중동', '부천시청', '상동', '삼산체육관', '굴포천', 
                '부평구청', '산곡', '석남'],
        '8호선': ['암사', '천호', '강동구청', '몽촌토성', '잠실', '석촌', '송파', '가락시장', '문정', '장지', '복정', '남위례', '산성', '남한산성입구', '단대오거리', '신흥', '수진', '모란'],
        '9호선': ['개화', '김포공항', '공항시장', '신방화', '마곡나루', '양천향교', '가양', '증미', '등촌', '염창', '신목동', '선유도', '당산', '국회의사당', '여의도', '샛강', '노량진', '노들', '흑석', '동작', '구반포', '신반포', '고속터미널', '사평', '신논현', '언주', 
                '선정릉', '삼성중앙', '봉은사', '종합운동장', '삼전', '석촌', '석촌고분', '중앙보훈병원', '둔촌오륜', '한성백제', '송파나루', '올림픽공원']
    }

    all_stations = set(station for line in subway_lines.values() for station in line)

    # 호선 선택
    if selector[0] == players[0][0]:  # 사용자인 경우
        print("선택 가능한 호선:")
        for i, line in enumerate(subway_lines.keys(), 1):
            print(f"{i}. {line}")
        while True:
            try:
                line_choice = int(input("호선 번호를 선택하세요: "))
                if 1 <= line_choice <= len(subway_lines):
                    current_line = list(subway_lines.keys())[line_choice - 1]
                    break
                else:
                    print("올바른 호선 번호를 선택해주세요.")
            except ValueError:
                print("숫자를 입력해주세요.")
    else:  # AI 플레이어인 경우
        current_line = random.choice(list(subway_lines.keys()))
    
    print(f"{selector[0]}님이 {current_line}을 선택했습니다.")

    used_stations = set()
    current_player_index = players.index(selector)
    direction = 1  # 1: 정방향, -1: 역방향

    def timer_expired():
        nonlocal timer_expired_flag
        timer_expired_flag = True

    while True:
        current_player = players[current_player_index]
        print(f"\n{current_player[0]}의 차례입니다. (현재 노선: {current_line})")

        timer_expired_flag = False
        timer = threading.Timer(5.0, timer_expired)
        timer.start()

        if current_player[0] == players[0][0]:  # 사용자 차례
            station = input("역 이름을 입력하세요 (제한 시간 5초): ")
        else:  # AI 플레이어 차례
            time.sleep(random.uniform(1, 3))  # AI가 생각하는 시간
            if random.random() < 0.3:  # 30% 확률로 실수
                mistake_type = random.choice(["used", "wrong_line", "non_existent"])
                if mistake_type == "used":
                    station = random.choice(list(used_stations)) if used_stations else random.choice(list(all_stations))
                elif mistake_type == "wrong_line":
                    wrong_lines = [line for line in subway_lines.keys() if line != current_line]
                    wrong_line = random.choice(wrong_lines)
                    station = random.choice(subway_lines[wrong_line])
            else:
                station = random.choice([s for s in subway_lines[current_line] if s not in used_stations])
            print(f"{current_player[0]}의 선택: {station}")

        timer.cancel()

        if timer_expired_flag:
            print("시간 초과!")
            return current_player

        if station in used_stations:
            print(f"{station}은 이미 사용된 역입니다.")
            return current_player
        
        if station not in subway_lines[current_line]:
            if station in all_stations:
                print(f"{station}은 {current_line}에 없는 역입니다.")
            else:
                print(f"{station}은 존재하지 않는 역입니다.")
            return current_player

        used_stations.add(station)
        print(f"{current_player[0]}님이 {station}을(를) 선택했습니다.")

        # 다음 플레이어로 넘어가기
        current_player_index = (current_player_index + direction) % len(players)

        # 가끔 방향 변경
        if random.random() < 0.1:  # 10% 확률로 방향 변경
            direction *= -1
            print("진행 방향이 변경되었습니다!")

    return random.choice(players) 

##-게임 3. 007빵 ---------------------------------------------------------------------


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
                if random.random() < 0.5 or timer_expired_flag:  # 30% 확률로 AI가 실수 또는 시간 초과
                    timer.cancel()
                    print(f"{left_player[0]} 또는 {right_player[0]}가 제 시간에 반응하지 못했습니다!")
                    return random.choice([left_player, right_player])
            
            timer.cancel()
            print(f"{left_player[0]}와 {right_player[0]}: 으악!")

        seq_index = (seq_index + 1) % 4
        current_player = next_player

    return current_player


##-게임 4. 더 게임 오브 데스 ---------------------------------------------------------------------

def theGameofDeath(players, selector):
    if not (2 <= len(players) <= 4):
        print("플레이어 수는 최소 2명에서 최대 4명이어야 합니다.")
        return random.choice(players)
    # 시작할 플레이어 선정
    current_player = selector
    print(f"\n{current_player[0]}님이 시작합니다.")
    #죽음의 숫자 선택
    if current_player == players[0]:  # 사용자가 시작자일 경우
        death_number = int(input(f"{current_player[0]}의 차례입니다. 죽음의 번호를 입력하세요 (2-10): "))
        while death_number < 2 or death_number > 10:
            death_number = int(input("잘못된 입력입니다. 죽음의 번호를 2-10 사이로 입력하세요: "))
    else:
        death_number = random.randint(2, 10)
        print(f"{current_player[0]}의 차례입니다. 죽음의 번호는 {death_number}입니다.")

    print(f"\n죽음의 숫자는 {death_number}입니다.\n")
    # 각 플레이어가 지목할 사람 설정 (자신을 제외한 다른 플레이어)
    target_list = []
    for player in players:
        if player == players[0]:  # 사용자가 지목할 사람을 입력하는 경우
            while True:
                target_name = input(f"{player[0]}님, 지목할 사람의 이름을 입력하세요 (자신은 지목할 수 없습니다): ")
                if target_name in [p[0] for p in players if p != player]:
                    target = next(p for p in players if p[0] == target_name)
                    break
                else:
                    print("잘못된 입력입니다. 플레이어 목록에서 선택하세요.")
        else:  # AI 플레이어가 지목할 사람을 무작위로 선택하는 경우
            valid_targets = [p for p in players if p != player]
            target = random.choice(valid_targets)
        target_list.append(target)

    print("\n각 플레이어가 지목할 사람 설정 완료:")
    for idx, target in enumerate(target_list):
        print(f"{players[idx][0]} -> {target[0]}")

    # 라운드 진행
    count = 1
    current_index = players.index(current_player)
    print(f"카운트 시작: ")

    while count <= death_number:
        next_player = target_list[current_index]
        print(f"카운트 {count}: {players[current_index][0]} -> {next_player[0]}")
        time.sleep(0.5)
        current_index = players.index(next_player)
        count += 1

    eliminated_player = players[current_index]
    print(f"\nPlayer {eliminated_player[0]} is eliminated.")
    return eliminated_player



##-게임 5. 만두 게임 -----------------------------------------------


def get_mando_value(mando):
    if mando == "만두 만두":
        return 0
    elif mando == "만두":
        return 5
    elif mando == "X":
        return 10
    else:
        raise ValueError("잘못된 입력입니다.")
    

def play_mando_game(players):
    user_name = players[0][0]  # 사용자의 이름을 저장합니다.

    while True:
        main_player = random.choice(players)  # 매 라운드마다 무작위로 메인 플레이어를 선택합니다.
        max_value = len(players) * 10  # 가능한 최대 값

        # 메인 플레이어가 숫자를 외칩니다.
        if main_player[0] == user_name:  # 사용자가 메인 플레이어인 경우
            while True:
                try:
                    player_number = int(input(f"{main_player[0]}, 5의 배수인 숫자를 외쳐주세요 (0, 5, 10, ..., {max_value}): "))
                    if player_number % 5 == 0 and 0 <= player_number <= max_value:
                        break
                    else:
                        print("5의 배수인 숫자를 0부터 최대값까지 입력해주세요.")
                except ValueError:
                    print("숫자만 입력해주세요.")
        else:  # AI가 메인 플레이어인 경우
            player_number = random.choice(range(0, max_value + 1, 5))
            print(f"{main_player[0]}이(가) {player_number}를 외쳤습니다.")

        total_value = 0
        user_mando_value = None  # 사용자의 만두 값을 저장할 변수

        # 다예가 플레이어일 경우 만두 값을 입력받음
        for player in players:
            if player[0] == user_name:
                while True:
                    mando = input(f"\n{player[0]}, 당신의 만두를 입력하세요 (만두 만두 = 0 / 만두 = 5 / X = 10): ").strip()
                    try:
                        user_mando_value = get_mando_value(mando)
                        total_value += user_mando_value
                        break
                    except ValueError:
                        print("유효한 만두 입력만 가능합니다 ('만두 만두', '만두', 'X'). 다시 입력해주세요.")
        
        print("\n~~~~참가자들이 만두 값을 선택합니다.~~~~\n")
        for player in players:
            if player[0] != user_name:  # AI 플레이어가 만두 값을 선택합니다.
                mando_value = random.choice([0, 5, 10])
                mando = "만두 만두" if mando_value == 0 else "만두" if mando_value == 5 else "X"
                print(f"{player[0]}이(가) {mando}을(를) 선택했습니다.")
                total_value += mando_value

        print(f"\n모든 손가락의 합은 {total_value}입니다.")
        if player_number == total_value:
            print(f"\n{main_player[0]}이(가) 이겼습니다!")
            continue  # 이겼을 때는 계속 게임을 진행
        else:
            print(f"\n{main_player[0]}이(가) 졌습니다!")
            return main_player  # 패배한 메인 플레이어를 반환
        

##-게임 상태 업데이트 ---------------------------------

def update_player_status(player, drinks):
    player[2] += drinks  # glasses_drunk 증가
    player[3] -= drinks  # glasses_left 감소
    print_player_status(player)

##-게임 잔행 ---------------------------------------

def main():
    print_intro()
    
    while True:
        user_input = input("게임을 진행할까요? (y/n): ").strip().lower()
        if user_input == 'y':
            start_game()
            break
        elif user_input == 'n':
            print("게임을 종료합니다. 안녕!")
            return
        else:
            print("y 또는 n을 입력해주세요.")
    
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
    players_who_chose = set()  # 게임을 선택한 플레이어들을 추적

    while all(player[3] > 0 for player in all_players):
        print(f"\n======= 라운드 {game_round} ========")
        
        # 게임을 선택하지 않은 플레이어들 중에서 랜덤하게 선택
        available_choosers = [p for p in all_players if p[0] not in players_who_chose]
        if not available_choosers:
            players_who_chose.clear()
            available_choosers = all_players

        choosing_player = random.choice(available_choosers)
        players_who_chose.add(choosing_player[0])
        
        print(f"\n{choosing_player[0]}님이 게임을 선택합니다.")
        
        if choosing_player[0] == all_players[0][0]:  # 사용자인 경우
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
        
        print(f"\n{choosing_player[0]}님이 {selected_game}을(를) 선택했습니다.")
        
        loser = play_game(selected_game, all_players, choosing_player)
        update_player_status(loser, 1)  # 패자는 1잔을 마심
        
        if loser[3] <= 0:
            print(f"\n{loser[0]}님이 치사량에 도달했습니다!🤢🤮")
            break
        
        game_round += 1

    print("\n게임이 종료되었습니다!\n")
    print("================= 최종 결과 ====================")
    for player in all_players:
        print_player_status(player)

if __name__ == "__main__":
    main()