from flask import Flask, Blueprint, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models import Location, Sensor, Record
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    sensors = Sensor.query.all()
    records = {}
    for sensor in sensors:
        records[sensor] = Record.query.filter_by(sensor_id = sensor.sensor_id).order_by(Record.record_timestamp.desc()).first()
    return render_template('index.html', sensors = sensors, records = records)

@views.route("/admin")
def admin():
    return redirect(url_for("views.home"))

@views.route("/push-data", methods=['POST'])
def post_status():
    if request.method == 'POST':
        data = json.loads(request.get_json())
        print(data)
        device_id = data["device_id"]
        status = data["status"]

        # finds the sensor we want to use, then makes a new record for it
        sensor = Sensor.query.filter_by(sensor_id = device_id).first()
        if sensor is None:
            sensor = Sensor()
            db.session.add(sensor)
            db.session.commit()
        record = Record()
        record.sensor_id = sensor.sensor_id

        # adds the current status to the database
        record.reading = status
        print(record.reading)
        db.session.add(record)
        db.session.commit()
        return redirect('/')

        

