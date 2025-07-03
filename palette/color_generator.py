
import json
import os
import random

class ColorGenerator:
    def __init__(self, data_file="color_data.json"):
        self.data_file = os.path.join(os.path.dirname(__file__), data_file)
        self.color_data = self._load_color_data()

    def _load_color_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.data_file}.")
            return {}

    def generate_palette(self, keyword):
        # 키워드를 소문자로 변환하여 검색
        keyword_lower = keyword.lower()

        # 정확히 일치하는 키워드 검색
        if keyword_lower in self.color_data:
            return self.color_data[keyword_lower]

        # 부분적으로 일치하는 키워드 검색 (더 복잡한 로직은 향후 추가)
        # 예: '차분함' -> '차분한'
        for key, value in self.color_data.items():
            if keyword_lower in key or key in keyword_lower:
                return value

        # 일치하는 키워드가 없을 경우, 기본 팔레트 또는 랜덤 팔레트 반환
        # 여기서는 간단히 첫 번째 키워드의 팔레트를 반환하거나, '기본' 키워드가 있다면 그것을 반환
        if "기본" in self.color_data:
            return self.color_data["기본"]
        elif self.color_data:
            return random.choice(list(self.color_data.values()))
        
        return None # 데이터가 전혀 없을 경우

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb_color):
        return '#%02x%02x%02x' % rgb_color
