import sqlite3
conn = sqlite3.connect('server.sqlite3')
cursor = conn.cursor()
cursor.close()
conn.commit()
conn.close()