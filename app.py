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
    pending = db.execute(
        "SELECT id, title FROM tasks WHERE completed = 0 ORDER BY created_at DESC"
    ).fetchall()
    done = db.execute(
        "SELECT id, title FROM tasks WHERE completed = 1 ORDER BY created_at DESC"
    ).fetchall()
    return render_template("index.html", pending=pending, done=done)


@app.route("/add", methods=["POST"])
def add():
    task_name = request.form.get("task", "").strip()
    if task_name:
        db = get_db()
        db.execute("INSERT INTO tasks (title) VALUES (?)", (task_name,))
        db.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/tasks/<int:id>/state", methods=["POST"])
def toggle_task_state(id):
    value = request.form.get("completed", "0")
    completed = 1 if value == "1" else 0

    db = get_db()
    db.execute("UPDATE tasks SET completed = ? WHERE ID = ?", (completed, id))
    db.commit()
    return redirect(url_for("index"))
