import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DB_Connection:
    def db_connect(self):
        try:
            connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST')

            )

            # cursor = connection.cursor()

            return connection
    
        except Exception as e:
            print(f"An error occurred: {e}")

    def db_schema(self):
        try:
            sql = '''CREATE TABLE IF NOT EXISTS server (
            id SERIAL PRIMARY KEY,
            guild_id BIGINT NOT NULL UNIQUE,
            name TEXT,
            join_date TIMESTAMP NOT NULL
        );
            
            CREATE TABLE IF NOT EXISTS channel (
            id SERIAL PRIMARY KEY,
            channel_id BIGINT NOT NULL UNIQUE,
            name TEXT,
            join_date TIMESTAMP NOT NULL,
            command CHAR(20) NOT NULL,
            activator BIGINT NOT NULL,
            remove_date TIMESTAMP,
            server_id BIGINT,
            FOREIGN KEY (server_id) REFERENCES server(id) ON DELETE CASCADE
        );
            '''
            conn = self.db_connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            print("Tables created successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

  

    def drop_table(self):
        try:
            sql = '''drop table channel; drop table server;'''
            conn = self.db_connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            print("Tables dropped!")
        except Exception as e:
            print(f"Raised an Exception {e}")



# if db_connection():
#     print("DB connected successfully!")

connection = DB_Connection()
conn = connection.db_schema()
if conn:
    print("DB connected Successfully!")