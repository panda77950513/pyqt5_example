# modules/cli_display.py

# CLI 화면 출력 및 사용자 입력 처리 함수들을 여기에 구현합니다.

def display_menu(title, options):
    print(f"\n--- {title} ---")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    
    # 메인 메뉴에서는 '종료', 서브 메뉴에서는 '이전 메뉴'로 표시
    if "유명 건축가 탐색" in title: # 메인 메뉴
        print("0. 종료")
    else: # 서브 메뉴
        print("0. 이전 메뉴")

def get_user_choice(prompt, max_choice=None, allow_empty=False):
    while True:
        try:
            choice_str = input(f"\n{prompt}: ")
            
            if allow_empty and choice_str == '':
                return '' # Enter만 눌렀을 경우 빈 문자열 반환

            if choice_str == '0':
                return '0'
            
            choice_int = int(choice_str)
            if max_choice is not None and not (1 <= choice_int <= max_choice):
                print("유효하지 않은 번호입니다. 다시 입력해주세요.")
                continue
            return str(choice_int) # 문자열로 반환하여 일관성 유지
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")
        except EOFError:
            print("입력이 감지되지 않았습니다. 다시 시도해주세요.")

def press_enter_to_continue():
    input("\n계속하려면 Enter를 누르세요...")

def display_architect_info(info):
    print("\n" + "=" * 50)
    if info:
        print(f"--- {info['name']} ---\n")
        print(info["description"])
        print("\n" + "-" * 50)
        print("주요 건축물:")
        if info["buildings"]:
            for i, building in enumerate(info["buildings"]):
                print(f"{i+1}. {building['name']}")
        else:
            print("건축물 정보를 찾을 수 없습니다.")
    else:
        print("건축가 정보를 찾을 수 없습니다.")
    print("=" * 50)

def display_building_info(info):
    print("\n" + "=" * 50)
    if info:
        print(f"--- {info['name']} ---\n")
        print(f"위치: {info['location']}")
        print(f"완공: {info['year']}")
        print(f"설명: {info['description']}")
        if info.get("image_url"):
            print("이미지 URL: {}".format(info.get("image_url")))
    else:
        print("건축물 정보를 찾을 수 없습니다.")
    print("=" * 50)
