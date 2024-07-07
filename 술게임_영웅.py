import threading
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
        print("~~~~~~~~~~~~~~~~~🍻 소주 기준 당신의 주량은? 🍻~~~~~~~~~~~~~~~~~")
        print("                 🍺1. 소주 반병(2잔)")
        print("                 🍺2. 소주 반병에서 한병(4잔)")
        print("                 🍺3. 소주 한병에서 한병 반(6잔)")
        print("                 🍺4. 소주 한병 반에서 두병(8잔)")
        print("                 🍺5. 소주 두병이상(10잔)")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #print("🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻")


        print("당신의 치사량(주량)은 얼마만큼인가요? (1~5 중에 선택하시오)")
        
        choice = input("선택 (1-5): ").strip()
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
    print(f"\n{name}님의 주량은 레벨 {tolerance}입니다!")
    
    # 상대 플레이어 추가ㅇ
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
        "지하철 게임",
        "공공칠빵 게임"
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
    elif game == "지하철 게임":
        loser = play_subway_game(players)
    elif game == "공공칠빵 게임":
        loser = play_007_game(players)
    print(f"{game} 게임이 끝났습니다!")
    print(f"패자: {loser[0]}")
    return loser

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
            
def play_subway_game(players):
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

    print("지하철 게임을 시작합니다!")
    
    # 발회자(첫 번째 플레이어)가 노선 선택
    current_line = random.choice(list(subway_lines.keys()))
    print(f"{players[0][0]}님이 {current_line}을 선택했습니다.")

    used_stations = set()
    current_player_index = 0
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
                else:  # non_existent
                    station = "존재하지 않는 역"
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



def update_player_status(player, drinks):
    player[2] += drinks  # glasses_drunk 증가
    player[3] -= drinks  # glasses_left 감소
    print_player_status(player)

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