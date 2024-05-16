import mysql.connector
import os
from dotenv import load_dotenv

def get_full_path(dir_id):
    db_cursor.execute("""
            WITH RECURSIVE FilePath AS (
                SELECT id, name, parent_dir, name AS path
                FROM directories 
                WHERE id = %s
                UNION ALL
                SELECT d.id, d.name, d.parent_dir, CONCAT(d.name, '/', fp.path) AS path
                FROM directories AS d
                JOIN FilePath AS fp ON d.id = fp.parent_dir
                WHERE d.id <> 1
            )
            
            
    SELECT IF(EXISTS (SELECT 1 FROM FilePath WHERE path = (SELECT name FROM directories WHERE id = 1)),
        (SELECT path FROM FilePath),
        CONCAT((SELECT name FROM directories WHERE id = 1), '/', (SELECT path FROM (SELECT path FROM FilePath ORDER BY id LIMIT 1) AS subquery))
    ) AS path;

    """, (dir_id,))

    result = db_cursor.fetchall()

    return result[-1][0]


def retrieve_file_path(search_string):

    query = ("SELECT f.dir, f.content, f.name, f.readable, f.type, "
             "IF(f.readable = TRUE, (LENGTH(f.content) - LENGTH(REPLACE(f.content, %s, ''))) / LENGTH(%s), NULL) AS occurrences "
             "FROM files f "
             "WHERE BINARY f.name LIKE %s OR BINARY f.content LIKE %s")

    db_cursor.execute(query, (f"{search_string}", f"{search_string}",f"%{search_string}%", f"%{search_string}%"))
    results = db_cursor.fetchall()

    if results:
        for result in results:
            dir_id, content, file_name, readable, type, occurences = result
            path = get_full_path(dir_id)
            match_count = f"Occurences: {int(occurences)}" if readable else "File type reading not supported."
            print(f"{match_count:<35} File: {path}/{file_name+'.'+type}")
    else:
        print("No files found matching the searched string.")

if __name__ == "__main__":
    load_dotenv()

    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DATABASE")
    )
    db_cursor = db_connection.cursor()

    search_string = input("Enter string to search: ")
    retrieve_file_path(search_string)

    db_cursor.close()
    db_connection.close()

