from . import db
from sqlalchemy.sql import func

# Stores the location of each sensor.
class Location(db.Model):
    location_id = db.Column(db.Numeric(1,1, asdecimal=False), nullable=False, primary_key=True)
    location_name = db.Column(db.String(50))
    longitude = db.Column(db.Numeric(8,5))
    latitude = db.Column(db.Numeric(8,5))
    sensors = db.relationship('Sensor')

# Data for each individual sensor.
class Sensor(db.Model):
    sensor_id = db.Column(db.Numeric(1,1, asdecimal=False), nullable=False, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True), default=func.now())
    location_id = db.Column(db.Numeric(asdecimal=False), db.ForeignKey('location.location_id'))
    records = db.relationship('Record')

# Record data for each sensor, with accurate timelogs.
class Record(db.Model):
    reading_id = db.Column(db.Numeric(1,1, asdecimal=False), nullable=False, primary_key=True)
    reading = db.Column(db.Boolean())
    record_timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    sensor_id = db.Column(db.Numeric(asdecimal=False), db.ForeignKey('sensor.sensor_id'))
