import sqlite3 as sq

def new_user(conn: sq.Connection, cursor: sq.Cursor, name: str, id, url):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (id,))
    data = cursor.fetchone()
    if data is not None:
        return
    cursor.execute("INSERT INTO users (user_id, score, name, booster, photo) VALUES (?, ?, ?, ?, ?)", (id, 1, name, 1, url))
    conn.commit()

    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    task_ids = []
    for i in data:
        task_ids.append(str(i[0]))
    print(task_ids, id)
    cursor.execute("INSERT INTO user_task (user_id, undone_tasks_ids) VALUES (?, ?)", (id, " ".join(task_ids)))
    conn.commit()

def click(conn: sq.Connection, cursor: sq.Cursor, user_id):
    cursor.execute("SELECT score, booster, name, photo FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchall()
    click = data[0][1]
    score = data[0][0]
    name = data[0][2]
    cursor.execute("UPDATE users SET score=? WHERE user_id=?", (score+click, user_id))
    conn.commit()
    return score+click, name, data[0][3]

def boosters(conn: sq.Connection, cursor: sq.Cursor):
    cursor.execute("SELECT cost FROM costs WHERE booster=?",(1,))
    data = cursor.fetchone()
    if data is not None:
        return
    for i in range(0, 100):
        name = "booster"
        cost = i*50
        boost = i
        cursor.execute("INSERT INTO costs (cost, name, booster) VALUES (?, ?, ?)", (cost, name, boost))
        conn.commit()

# def tasks(conn: sq.Connection, cursor: sq.Cursor):
#     cursor.execute("SELECT * FROM tasks")
#     data = cursor.fetchone()
#     if data is not None:
#         return

def task_done(conn: sq.Connection, cursor: sq.Cursor, user_id: int, task_id: int):
    cursor.execute("SELECT undone_tasks_ids FROM user_task WHERE user_id=?", (user_id,))
    old = cursor.fetchone()[0].split(" ")
    old.remove(str(task_id))
    cursor.execute("UPDATE user_task SET undone_tasks_ids=? WHERE user_id=?", (" ".join(old), user_id))
    conn.commit()
    cursor.execute("SELECT reward FROM tasks WHERE id=?", (task_id,))
    reward = cursor.fetchone()[0]
    cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    score = cursor.fetchone()[0]
    cursor.execute("UPDATE users SET score=? WHERE user_id=?", (reward+score, user_id))
    conn.commit()