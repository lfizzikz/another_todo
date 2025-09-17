import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), "todo.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute(
            """
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
    g.db.commit()
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    db = get_db()
    rows = db.execute("SELECT title FROM tasks ORDER BY created_at DESC").fetchall()
    tasks = [r["title"] for r in rows]
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task_name = request.form.get("task", "").strip()
    if task_name:
        db = get_db()
        db.execute("INSERT INTO tasks (title) VALUES (?)", (task_name,))
        db.commit()
        return redirect(url_for("index"))
