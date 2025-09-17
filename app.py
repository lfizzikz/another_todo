import os

import _sqlite3
from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)

TASKS = []


@app.route("/")
def index():
    return render_template("index.html", tasks=TASKS)


@app.route("/add", methods=["POST"])
def add():
    task_name = request.form.get("task")
    if task_name:
        TASKS.append(task_name)
        return redirect(url_for("index"))
