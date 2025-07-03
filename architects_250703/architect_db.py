
import sqlite3
import os

DATABASE_NAME = 'architects.db'

def get_db_path():
    # 현재 스크립트 파일의 디렉토리를 기준으로 데이터베이스 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, DATABASE_NAME)

def create_tables():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS architects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_date TEXT,
            death_date TEXT,
            nationality TEXT,
            bio TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            architect_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            year_completed INTEGER,
            description TEXT,
            image_path TEXT,
            FOREIGN KEY (architect_id) REFERENCES architects(id)
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database and tables created at {get_db_path()}")

def add_architect(name, birth_date=None, death_date=None, nationality=None, bio=None):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO architects (name, birth_date, death_date, nationality, bio)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, birth_date, death_date, nationality, bio))
    architect_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return architect_id

def add_building(architect_id, name, location=None, year_completed=None, description=None, image_path=None):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO buildings (architect_id, name, location, year_completed, description, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (architect_id, name, location, year_completed, description, image_path))
    building_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return building_id

def get_architects():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM architects')
    architects = cursor.fetchall()
    conn.close()
    return architects

def get_buildings_by_architect(architect_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buildings WHERE architect_id = ?', (architect_id,))
    buildings = cursor.fetchall()
    conn.close()
    return buildings

def get_all_buildings():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buildings')
    buildings = cursor.fetchall()
    conn.close()
    return buildings

if __name__ == '__main__':
    create_tables()
    # 예시 데이터 추가 (나중에 google_web_search로 채울 부분)
    # architect_id = add_architect("Frank Lloyd Wright", "1867-06-08", "1959-04-09", "American", "Considered the greatest American architect of all time.")
    # add_building(architect_id, "Fallingwater", "Mill Run, Pennsylvania, USA", 1939, "A house built partly over a waterfall.", "path/to/fallingwater.jpg")
    # add_building(architect_id, "Guggenheim Museum", "New York City, USA", 1959, "A spiral-shaped museum.", "path/to/guggenheim.jpg")
