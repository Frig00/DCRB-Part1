import mysql.connector
import os
from dotenv import load_dotenv
from cache import LocalCache

cache = LocalCache()
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

    from_db = 0
    from_cache = 0
    matched_files = []
    cached_files_id = []
    for key, value in cache.get_all_items():
        if search_string in value[0] or search_string in value[4]:
            matched_files.append([key] + value + ['cache'])
            cached_files_id.append(key)
            from_cache += 1

    query = ("SELECT *, "
             "IF(f.readable = TRUE, (LENGTH(f.content) - LENGTH(REPLACE(f.content, %s, ''))) / LENGTH(%s), NULL) AS occurrences "
             "FROM files f "
             "WHERE BINARY f.name LIKE %s OR BINARY f.content LIKE %s AND FIND_IN_SET(f.id, %s) = 0;")

    db_cursor.execute(query, (f"{search_string}", f"{search_string}", f"%{search_string}%", f"%{search_string}%", ','.join([str(id) for id in cached_files_id])))
    results = db_cursor.fetchall()

    if results:
        for result in results:
            dir_id = result[4]
            path = get_full_path(dir_id)
            result_list = list(result)
            result_list.append(path)
            result_list.append('db')
            matched_files.append(result_list)
            from_db += 1
            cache.set(result_list[0], result_list[1:-1])
    elif not matched_files:
        print("\nNo files found matching the searched string.\n")

    print_files(matched_files, from_cache, from_db)

def print_files(files, from_cache, from_db):
    for file in files:
        file_id, file_name, file_type, readable, dir_id, content, occurences, path, prov = file
        match_count = f"Occurences: {int(occurences)}" if readable else "File type reading not supported."
        file_from = "cache" if prov == 'cache' else "database"
        print(f"{match_count:<35} File: {path}/{file_name + '.' + file_type} \nFile from: {file_from}\n")

    try:
        print(f"\nCache hit rate: {from_cache/(from_cache+from_db)*100:.2f}%\n\n")
    except ZeroDivisionError:
        pass

if __name__ == "__main__":
    load_dotenv()

    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DATABASE")
    )
    db_cursor = db_connection.cursor()

    while True:
        try:
            search_string = input("Enter string to search (press ctrl+c to exit): ")
        except KeyboardInterrupt:
            print("\n\nCtrl+C detected.")
            print("Clearing cache...")
            print("Exiting...\n")
            cache.clear()
            exit()

        retrieve_file_path(search_string)

    db_cursor.close()
    db_connection.close()

