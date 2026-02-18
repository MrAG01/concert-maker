import hashlib
import sqlite3

class DataBase:
    def __init__(self, database_path="database.db"):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

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
                        photo TEXT
                        
                        email TEXT
                    );
                    
                    CREATE TABLE IF NOT EXISTS artists (
                        id INTEGER PRIMARY KEY,           
                        group_id INTEGER,    
                        likes INTEGER
                    );
                    
                    CREATE TABLE IF NOT EXISTS artists_group (
                        id INTEGER PRIMARY KEY,           
                        name TEXT NOT NULL,
                        creation_date TEXT,
                        description TEXT,
                        banner_photo TEXT,
                        likes INTEGER
                    );
                    
                    CREATE TABLE IF NOT EXISTS concerts (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        group_id INTEGER,
                        start_time TEXT,
                        event_location TEXT
                    )
                """)

    def add_user(self, userdata, artist_data=None):
        try:
            username = userdata["username"]
            password_hash = hashlib.sha256(userdata["password"])

            name = userdata.get("name", username)
            artists_id = userdata.get("artists_id")
            description = userdata.get("description")
            birthday = userdata.get("birthday")
            gender = userdata.get("gender")
            photo = userdata.get("photo")
            email = userdata.get("email")


            #self.cursor.execute("""
            #    INSERT INTO executors (name, group_id, description, birthday, gender, likes)
            #    VALUES (?, ?, ?, ?, ?, ?);
            #""", (name, group_id, description, birthday, gender, likes))

        except KeyError:
            return

    def __del__(self):
        self.connection.close()
