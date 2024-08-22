import sqlite3 as sq

conn = sq.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("UPDATE users SET score=? WHERE user_id=?", (1000000, 1018684785))
conn.commit()