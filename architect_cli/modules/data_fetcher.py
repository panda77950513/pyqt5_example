# modules/data_fetcher.py

# 웹 검색 및 데이터 추출 함수들을 여기에 구현합니다.
# 예: Google Web Search API 호출, 웹 스크래핑 등

from default_api import google_web_search

def search_architect_info(query):
    print(f"\n[정보 검색 중]: 건축가 '{query}' 정보...")
    description = "정보를 찾을 없습니다."
    buildings = []

    try:
        search_results = google_web_search(query=f"{query} 건축가 정보")
        if search_results and search_results.get('search_results'):
            # 첫 번째 검색 결과 스니펫을 설명으로 사용
            if search_results['search_results'] and search_results['search_results'][0].get('snippet'):
                description = search_results['search_results'][0]['snippet']
        
        print(f"[정보 검색 중]: '{query}'의 주요 건축물 목록...")
        building_search_results = google_web_search(query=f"{query} 주요 건축물 목록")
        if building_search_results and building_search_results.get('search_results'):
            building_keywords = ['건축물', '성당', '주택', '미술관', '박물관', '센터', '빌딩', '도서관', '극장', '학교']
            for item in building_search_results['search_results']:
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                
                # 건축가 이름이 제목이나 스니펫에 포함되고, 건축물 관련 키워드가 있는 경우
                if query.lower() in title.lower() or query.lower() in snippet.lower():
                    if any(keyword in title or keyword in snippet for keyword in building_keywords):
                        buildings.append({"name": title, "description": snippet, "image_url": "(이미지 URL)"})
                        if len(buildings) >= 5: # 최대 5개 건축물만 가져옴
                            break
    except Exception as e:
        print(f"[오류 발생]: 건축가 정보 검색 중 오류가 발생했습니다: {e}")
        print("네트워크 연결을 확인하거나 잠시 후 다시 시도해주세요.")

    return {"name": query, "description": description, "buildings": buildings}

def search_building_info(query):
    print(f"\n[정보 검색 중]: 건축물 '{query}' 정보...")
    description = "정보를 찾을 수 없습니다."
    location = "알 수 없음"
    year = "알 수 없음"
    image_url = "(이미지 URL)"

    try:
        search_results = google_web_search(query=f"{query} 건축물 상세 정보")
        if search_results and search_results.get('search_results'):
            if search_results['search_results'] and search_results['search_results'][0].get('snippet'):
                description = search_results['search_results'][0]['snippet']
            
            # 추가 정보 추출 (간단한 예시)
            for item in search_results['search_results']:
                if "위치" in item.get('snippet', ''):
                    location = item['snippet'].split("위치:")[-1].strip().split(".")[0]
                if "완공" in item.get('snippet', '') or "년" in item.get('snippet', ''):
                    import re
                    match = re.search(r'\b(1[0-9]{3}|20[0-9]{2})년\b', item.get('snippet', ''))
                    if match:
                        year = match.group(0)
                if item.get('thumbnail') and item['thumbnail'].get('url'):
                    image_url = item['thumbnail']['url']
                    break
    except Exception as e:
        print(f"[오류 발생]: 건축물 정보 검색 중 오류가 발생했습니다: {e}")
        print("네트워크 연결을 확인하거나 잠시 후 다시 시도해주세요.")

    return {"name": query, "description": description, "location": location, "year": year, "image_url": image_url}