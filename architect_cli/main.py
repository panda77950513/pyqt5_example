# main.py

from modules.cli_display import display_menu, get_user_choice, display_architect_info, display_building_info, press_enter_to_continue
from modules.data_fetcher import search_architect_info, search_building_info
from modules.gemini_utils import summarize_text_with_gemini

def main():
    architects = ["르 코르뷔지에", "프랭크 로이드 라이트", "미스 반 데어 로에"]

    while True:
        display_menu("유명 건축가 탐색", architects)
        choice = get_user_choice("건축가를 선택하세요 (번호 입력)", len(architects))

        if choice == '0':
            print("프로그램을 종료합니다.")
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(architects):
                selected_architect = architects[index]
                print(f"\n선택된 건축가: {selected_architect}")

                # 건축가 정보 검색 및 표시
                architect_info = search_architect_info(selected_architect)
                display_architect_info(architect_info)

                if architect_info and architect_info["buildings"]:
                    while True:
                        building_names = [b["name"] for b in architect_info["buildings"]]
                        display_menu("건축물 선택", building_names)
                        building_choice = get_user_choice("건축물을 선택하세요 (번호 입력, 0. 이전 메뉴)", len(building_names))

                        if building_choice == '0':
                            break

                        try:
                            building_index = int(building_choice) - 1
                            if 0 <= building_index < len(building_names):
                                selected_building = building_names[building_index]
                                print(f"\n선택된 건축물: {selected_building}")

                                # 건축물 정보 검색 및 표시
                                building_info = search_building_info(selected_building)
                                display_building_info(building_info)

                                # Gemini 요약 (예시)
                                if building_info and building_info["description"]:
                                    print("\n" + summarize_text_with_gemini(building_info["description"]))

                                press_enter_to_continue()
                            else:
                                print("유효하지 않은 건축물 번호입니다.")
                        except ValueError:
                            print("잘못된 입력입니다. 숫자를 입력해주세요.")
                else:
                    press_enter_to_continue()

            else:
                print("유효하지 않은 건축가 번호입니다.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

if __name__ == '__main__':
    main()
