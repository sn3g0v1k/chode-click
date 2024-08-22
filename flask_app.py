from flask import Flask, render_template, request, redirect, url_for
from db_logic import click, boosters, task_done
import sqlite3 as sq

conn = sq.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id BIGINT, score INTEGER, name TEXT, booster INTEGER, photo TEXT)")
conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS costs (cost INTEGER, name TEXT, booster INTEGER)")
conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, reward INTEGER, url TEXT)")
conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS user_task (user_id BIGINT, undone_tasks_ids TEXT)")
conn.commit()

boosters(conn, cursor)

app = Flask(__name__)


class Task:
    def __init__(self, id, text, reward, url):
        self.text = text
        self.reward = reward
        self.id = id
        self.url = url







@app.route("/")
def index():
    return "rwerwerwrwjroiwejroiwejrweoijr"


@app.route('/clicking/<user_id>', methods=['GET', "POST"])
def hello_world(user_id):
    if request.method == "POST" and "click" in request.form:
        data = click(conn, cursor, int(user_id))
        return render_template('main.html', score=data[0], user_name=data[1], user_picture=data[2])
    
    if request.method == "POST" and "improve" in request.form:
        return redirect(url_for("evolve", user_id=user_id))
    
    if request.method == "POST" and "Earn" in request.form:
        return redirect(url_for("tasks", user_id=user_id))
    
    cursor.execute("SELECT score, name, booster, photo FROM users WHERE user_id=?", (user_id,))
    try:
        data = cursor.fetchall()[0]
    except:
        return "No such user"
    
    score = data[0]
    name = data[1]
    boosters = data[2]
    photo = data[3]

    return render_template('main.html', score=score, user_name=name, user_picture=photo)

@app.route('/evolve/<user_id>', methods=['GET', "POST"])
def evolve(user_id):
    cursor.execute("SELECT score, booster FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchall()[0]
    score = data[0]
    booster = data[1]
    cursor.execute("SELECT cost FROM costs WHERE name=? AND booster=?", ("booster", int(booster)+1))

    if request.method == "POST" and "back" in request.form:
        return redirect(url_for("hello_world", user_id=user_id))
    
    try:
        cost = cursor.fetchall()[0][0]
    except IndexError:
        return render_template('evolves.html', score=score, boost=booster+1, cost=0, warning="You achieved maximum potential. Good Job!")
    
    if request.method == "POST" and "boosting" in request.form:
        if score-cost < 0:
            return render_template('evolves.html', score=score, boost=booster+1, cost=cost)
        cursor.execute("UPDATE users SET booster=?, SCORE=? WHERE user_id=?", (int(booster)+1, score-cost, user_id))
        conn.commit()
        cursor.execute("SELECT cost FROM costs WHERE name=? AND booster=?", ("booster", int(booster)+2))

        try:
            cost = cursor.fetchall()[0][0]
        except IndexError:
            return render_template('evolves.html', score=score, boost=booster+1, cost=0, warning="You achieved maximum potential. Good Job!")
        
        return render_template('evolves.html', score=score, boost=booster+2, cost=cost)
    
    return render_template('evolves.html', score=score, boost=booster+1, cost=cost)


@app.route("/tasks/<user_id>", methods=["GET", "POST"])
def tasks(user_id):
    if request.method == "POST" and "Task" in request.form:
        task_id = request.form.get("id")
        cursor.execute("SELECT url FROM tasks WHERE id=?", (task_id,))
        url = cursor.fetchone()[0]
        task_done(conn, cursor, user_id, task_id)
        return redirect(url)
    blocks_list = []
    cursor.execute("SELECT undone_tasks_ids FROM user_task WHERE user_id=?", (user_id,))
    data = cursor.fetchone()[0].split(" ")
    print(data)
    if data == [""]:
        return render_template("tasks.html")
    if data[0] == "":
        data = data[1:]
    for i in data:
        print(i)
        cursor.execute("SELECT * FROM tasks WHERE id=?", (int(i),))
        data = cursor.fetchone()
        blocks_list.append(Task(int(i), data[1], data[2], data[3]))

    return render_template("tasks.html", blocks=blocks_list)


app.run(debug=True)