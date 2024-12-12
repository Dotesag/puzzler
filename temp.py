import sqlite3

with sqlite3.connect('db/database.db') as db:
    cursor = db.cursor()
    # CREATE TABLE IF NOT EXISTS planes(name TEXT, wood_type TEXT, width INT)

    query = '''
                
                INSERT INTO planes (name, wood_type, width) VALUES ('Береза 3 мм', 'Береза', 3)    

            '''
    cursor.execute(query)
