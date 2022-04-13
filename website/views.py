from flask import Flask, Blueprint, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views.route("/admin")
def admin():
    return redirect(url_for("views.home"))
