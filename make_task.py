import sqlite3 as sq

text = input("Enter text ")
cost = input("Enter cost ")
url = input("Enter url ")

conn = sq.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("INSERT INTO tasks (text, reward, url) VALUES (?, ?, ?)", (text, cost, url))
conn.commit()

cursor.execute("SELECT id FROM tasks WHERE url=?", (url,))
task_id = cursor.fetchone()[0]

cursor.execute("SELECT * FROM user_task")
data = cursor.fetchall()
for i in data:
    uti = i[1].split(" ")
    uti.append(str(task_id))
    cursor.execute("UPDATE user_task SET undone_tasks_ids=? WHERE user_id=?", (" ".join(uti), i[0]))
    conn.commit()


print("Success")
