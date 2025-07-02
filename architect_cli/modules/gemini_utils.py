# modules/gemini_utils.py

# Gemini API 관련 함수들을 여기에 구현합니다.
# 예: 텍스트 요약, 정보 추출 등

# 현재 제공된 도구에는 직접적인 텍스트 생성(generative text) 기능이 없으므로,
# 이 함수는 Gemini 모델이 수행할 작업을 개념적으로 보여줍니다.

def summarize_text_with_gemini(text):
    if not text:
        return "[Gemini 요약]: 요약할 텍스트가 없습니다."
    
    # 실제 Gemini 모델이 연결된다면, 여기에 텍스트를 요약하는 API 호출 로직이 들어갑니다.
    # 현재는 입력 텍스트의 일부를 사용하여 요약된 것처럼 보여줍니다.
    summary_prefix = "[Gemini 요약]: "
    if len(text) > 200:
        # 긴 텍스트의 경우, 시작 부분과 끝 부분을 발췌하여 요약된 것처럼 보여줍니다.
        return f"{summary_prefix}{text[:100]}... (중략) ...{text[-50:]}"
    else:
        # 짧은 텍스트의 경우, 전체를 보여줍니다.
        return f"{summary_prefix}{text}"
