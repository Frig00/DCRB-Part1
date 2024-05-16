import os
import mysql.connector
from dotenv import load_dotenv


readable_types = ['txt', 'html']
def insert_directory(name, parent_dir_id):
    sql = "INSERT INTO directories (name, parent_dir) VALUES (%s, %s)"
    db_cursor.execute(sql, (name, parent_dir_id))
    db_connection.commit()
    print(f'Directory "{name}" inserted successfully.')
    return db_cursor.lastrowid

def insert_file(name, file_type, readable, dir_id, content):
    sql = "INSERT INTO files (name, type, readable, dir, content) VALUES (%s, %s, %s, %s, %s)"
    db_cursor.execute(sql, (name, file_type, readable, dir_id, content))
    db_connection.commit()
    print(f'File "{name}" inserted successfully.')

def fill_db(root_path, parent_dir_id=None):

    current_dir_id = insert_directory(os.path.basename(root_path), parent_dir_id if parent_dir_id else 1)

    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)

        if os.path.isdir(item_path):
            fill_db(item_path, current_dir_id)
        elif os.path.isfile(item_path):
            with open(item_path, 'r', encoding='utf-8') as file:
                content = file.read()
                readable = True if item.rsplit('.', 1)[1] in readable_types else False
                insert_file(item.rsplit('.', 1)[0], item.rsplit('.', 1)[1], readable, current_dir_id, content)


if __name__ == "__main__":
    load_dotenv()

    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DATABASE")
    )
    db_cursor = db_connection.cursor()

    root_dir = "DCRB"

    fill_db(root_dir)

    db_cursor.close()
    db_connection.close()
