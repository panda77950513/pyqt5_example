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
            bio TEXT,
            image_path TEXT
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
    
    # Add image_path column to architects table if it doesn't exist
    try:
        cursor.execute("ALTER TABLE architects ADD COLUMN image_path TEXT")
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise

    conn.commit()
    conn.close()
    print(f"Database and tables created/updated at {get_db_path()}")

def add_architect(name, birth_date=None, death_date=None, nationality=None, bio=None, image_path=None):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO architects (name, birth_date, death_date, nationality, bio, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, birth_date, death_date, nationality, bio, image_path))
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

def update_architect_image_path(architect_id, image_path):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE architects
        SET image_path = ?
        WHERE id = ?
    ''', (image_path, architect_id))
    conn.commit()
    conn.close()

def update_building_image_path(building_id, image_path):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE buildings
        SET image_path = ?
        WHERE id = ?
    ''', (image_path, building_id))
    conn.commit()
    conn.close()

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