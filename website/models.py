from cairo import RecordingSurface
from . import db
from sqlalchemy.sql import func

# Stores the location of each sensor.
class Location(db.Model):
    location_id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    location_name = db.Column(db.String(50))
    longitude = db.Column(db.Numeric(8,5))
    sensors = db.relationship('Sensor')

# Data for each individual sensor.
class Sensor(db.Model):
    sensor_id = db.Column(db.Integer(), primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True), default=func.now())
    location_id = db.Column(db.Numeric(asdecimal=False), db.ForeignKey('location.location_id'))
    records = db.relationship('Record')

    def __repr__(self):
        return f'Sensor {self.sensor_id}'

# Record data for each sensor, with accurate timelogs.
class Record(db.Model):
    reading_id = db.Column(db.Integer(), primary_key=True)
    reading = db.Column(db.Boolean())
    record_timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    sensor_id = db.Column(db.Numeric(asdecimal=False), db.ForeignKey('sensor.sensor_id'))

    def __repr__(self):
        return f'{self.reading}'
