from flask import Flask, Blueprint, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models import Location, Sensor, Record
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['deploy_button'] == 'Deploy Sensor':
            sensor = Sensor()
            db.session.add(sensor)
            db.session.commit()

    return render_template('index.html')

@views.route("/admin")
def admin():
    return redirect(url_for("views.home"))

@views.route("/push-data", methods=['POST'])
def post_status():
    if request.method == 'POST':
        data = json.loads(request.get_json())
        print(data)
        device_id = data["device_id"]
        exists = Sensor.query.filter_by(sensor_id = device_id).first() is not None
        if not exists:
            sensor = Sensor()
            db.session.add(sensor)
        sensor = Sensor.query.filter_by(sensor_id = device_id).first()
        sensor.records = data["status"]
        db.session.commit()
        return redirect('/')

        

