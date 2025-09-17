import os

import _sqlite3
from flask import Flask, g, redirect, render_template, request

app = Flask(__name__)

TASKS = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    TASKS.append(task)
    return render_template("add.html", tasks=TASKS)
