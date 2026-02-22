import hashlib
import os.path
import random
import sqlite3


class DataBase:
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    def __init__(self, database_path="database.sqlite", upload_folder="uploads"):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
        self.upload_folder = upload_folder

    def _get_free_filename(self, extension):
        name = os.path.join(self.upload_folder, f"{random.randint(0, 10000000000)}.{extension}")
        while os.path.exists(name):
            name = os.path.join(self.upload_folder, f"{random.randint(0, 10000000000)}.{extension}")
        return name

    def upload_photo(self, photo_file):
        try:
            if photo_file is None:
                return None
            filename = photo_file.filename.lower()
            extension = filename.rsplit(".", 1)[1]
            if extension not in DataBase.ALLOWED_EXTENSIONS:
                return None

            free_filename = self._get_free_filename(extension)
            photo_file.save(free_filename)
            return os.path.basename(free_filename)
        except Exception as error:
            print(error)
            return

    def init_tables(self):
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        
                        username TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        
                        name TEXT,
                        artists_id INTEGER,
                        description TEXT,
                        birthday TEXT,
                        gender TEXT,
                        photo TEXT,
                        
                        email TEXT
                    );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS artists (
                        id INTEGER PRIMARY KEY,           
                        group_id INTEGER,    
                        likes INTEGER
                    );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS artists_group (
                        id INTEGER PRIMARY KEY,           
                        name TEXT NOT NULL,
                        creation_date TEXT,
                        description TEXT,
                        banner_photo TEXT,
                        likes INTEGER
                    );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS concerts (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        group_id INTEGER,
                        start_time TEXT,
                        event_location TEXT,
                        banner_photo TEXT,
                    );""")
        self.connection.commit()

    def get_closest_concerts(self, limit=10):
        return [
            {
                "image": "static/images/con1.jpg",
                "name": "Пошумим блин",
                "description": "Самый лучший концерт в мире, именно здесь соберутся все известные звёзды мира. Таки как: MrBeast, T-series, Jeffry Epstein и множество других!",
                "date": "3.03.2026",
                "cost": "от 3500р"
            },
            {
                "image": "static/images/s2.jpg",
                "name": "Ееее роо-ок",
                "description": "Ееееееееееееееееееееееееее роооооооооок",
                "date": "Через 3 дня",
                "cost": "Бесплатно"
            },
            {
                "image": "static/images/s3.png",
                "name": "𓅃𓉔𓇌, 𓇋𓅓 𓎼𓄿𓇌",
                "description": "𓆑𓇋𓈖𓄿𓃭𓃭𓇌 𓇋 𓎼𓏏 𓃀𓄿𓈖𓈖𓂧!! 𓇌𓅲𓉔. 𓇋𓅓 𓎼𓄿𓇌, 𓇋 𓃭𓆯 𓃀𓇌𓋴",
                "date": "Уже идёт",
                "cost": "от 8000р"
            }
        ]

    def add_concert(self, concert_data):
        try:
            name = concert_data.get("name")
            description = concert_data.get("description")
            group_id = concert_data.get("group_id")
            start_time = concert_data.get("start_time")
            event_location = concert_data.get("event_location")
            banner_photo = concert_data.get("banner_photo")
            self.cursor.execute("""
                INSERT INTO concerts (name, description, group_id, start_time, event_location, banner_photo)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (name, description, group_id, start_time, event_location, banner_photo))

        except Exception as error:
            return

    def get_base_user_info(self, user_id):
        try:
            matched = self.cursor.execute("""
                SELECT username, name, photo FROM users WHERE id == ? 
            """, (user_id,)).fetchone()
            if matched:
                return {
                    "success": True,
                    "data": {
                        "id": matched[0],
                        "username": matched[1],
                        "name": matched[2],
                        "photo": matched[3]
                    }
                }
        except Exception as error:
            return {"success": False, "error": error}

    def get_all_user_info(self, user_id):
        try:
            matched = self.cursor.execute("""
                SELECT * FROM users WHERE id == ? 
            """, (user_id,)).fetchone()
            if matched:
                columns = [description[0] for description in self.cursor.description]
                return {
                    "success": True,
                    "data": dict(zip(columns, matched))
                }
        except Exception as error:
            return {"success": False, "error": error}

    def add_user(self, userdata, artist_data=None):
        try:
            username = userdata["username"]
            password_hash = hashlib.sha256(userdata["password"])

            name = userdata.get("name", username)
            description = userdata.get("description")
            birthday = userdata.get("birthday")
            gender = userdata.get("gender")
            photo = userdata.get("photo")
            email = userdata.get("email")
            if artist_data:
                group_id = artist_data.get("group_id")
                likes = 0
                self.cursor.execute("""
                    INSERT INTO artists (group_id, likes)
                    VALUES (?, ?);
                """, (group_id, likes))
                artists_id = self.cursor.lastrowid
            else:
                artists_id = 0

            self.cursor.execute("""
                INSERT INTO users (username, password_hash, name, artists_id, description, birthday, gender, photo, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (username, password_hash, name, artists_id, description, birthday, gender, photo, email))
            return {"success": True, "user_id": self.cursor.lastrowid}
        except Exception as error:
            return {"success": False, "error": error}

    def __del__(self):
        self.connection.close()
