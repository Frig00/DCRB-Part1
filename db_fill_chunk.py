import os
import mysql.connector
from dotenv import load_dotenv
from collections import deque

dir_query = "INSERT INTO directories (name, parent_dir) VALUES (%s, %s)"
file_query = "INSERT INTO files (name, type, readable, dir, content) VALUES (%s, %s, %s, %s, %s)"
file_chunks = []
dir_chunks = []
max_chunk_size = 50
readable_types = ['txt', 'html']

def check_and_commit():

    if len(file_chunks) >= max_chunk_size:
        if dir_chunks:
            db_cursor.executemany(dir_query, dir_chunks)
            db_connection.commit()
            print(f"{len(dir_chunks)} directories committed.")
            dir_chunks.clear()

        db_cursor.executemany(file_query, file_chunks)
        db_connection.commit()
        print(f"{len(file_chunks)} files committed.")
        file_chunks.clear()

    elif len(dir_chunks) >= max_chunk_size:
        db_cursor.executemany(dir_query, dir_chunks)
        db_connection.commit()
        print(f"{len(dir_chunks)} directories committed.")
        dir_chunks.clear()
def fill_db(root_path):
    dir_id = 1
    dir_queue = deque([(root_path, None)])  # Initialize the queue with the root directory

    while dir_queue:
        current_dir, parent_dir_id = dir_queue.popleft()
        check_and_commit()
        dir_chunks.append((os.path.basename(current_dir), parent_dir_id if parent_dir_id else 1))
        current_dir_id = dir_id
        dir_id += 1

        try:
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                if os.path.isdir(item_path):
                    dir_queue.append((item_path, current_dir_id))
                elif os.path.isfile(item_path):
                    try:
                        readable = item.rsplit('.', 1)[1] in readable_types
                    except IndexError:
                        readable = False
                    try:
                        file_name = item.rsplit('.', 1)[0]
                        file_type = item.rsplit('.', 1)[1]
                    except IndexError:
                        file_name = item
                        file_type = ''
                    if readable:
                        try:
                            with open(item_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                        except Exception as e:
                            print(f"Error reading file {item_path}: {e}")
                            content = ''
                    else:
                        content = ''

                    check_and_commit()
                    file_chunks.append((file_name, file_type, readable, current_dir_id, content))


        except Exception as e:
            print(f"Error processing directory {current_dir}: {e}")

    if dir_chunks:
        db_cursor.executemany(dir_query, dir_chunks)
        db_connection.commit()
        print(f"{len(dir_chunks)} directories committed.")
        dir_chunks.clear()

    if file_chunks:
        db_cursor.executemany(file_query, file_chunks)
        db_connection.commit()
        print(f"{len(file_chunks)} files committed.")
        file_chunks.clear()

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
