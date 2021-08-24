import csv
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

measurements = []
stations = []

file_path = 'Resources/hawaii_measurements.csv'
input_file = csv.DictReader(open(file_path))

for row in input_file:
    measurements.append(row)

file_path_2 = 'Resources/hawaii_stations.csv'
input_file_2 = csv.DictReader(open(file_path_2))

for row in input_file_2:
    stations.append(row)


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

start_date = dt.datetime(2012, 8, 22)
end_date = dt.datetime(2014, 8, 22)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Home Page of Hawaii weather data!!!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation which gives the percipitation on a given date<br/>"
        f"/api/v1.0/stations lists all the stations<br/>"
        f"/api/v1.0/tobs provides the temperatures from last year<br/>"
        f"/api/v1.0/2012.08.22 show the calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date <br/>"
        f"/api/v1.0/2012.08.22/2014.02.22 is for  `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date"
    )

@app.route("/api/v1.0/precipitation")
def perc():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    rain = []

    for date, prcp in results:
        rain_dict = {}
        rain_dict['Date'] = date
        rain_dict['Percipitation'] = prcp
        rain.append(rain_dict)

    return jsonify(rain)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    results = session.query(measurement.station).group_by(measurement.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    recent_date = dt.datetime(2016, 8, 22)
    results = st_top = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.station=='USC00516128').\
        filter(measurement.date>recent_date).all()
    session.close()    

    tobs_station = list(np.ravel(results))

    return jsonify(tobs_station)

@app.route("/api/v1.0/2012.08.22")
def start():
    session = Session(engine)

    
    
    temp_sel = session.query(func.avg(measurement.tobs),
             func.min(measurement.tobs),
             func.max(measurement.tobs)).filter(measurement.date>start_date).all()

    the_avg = session.query(func.avg(measurement.tobs).filter(measurement.date>start_date)).all(),
    the_min = session.query(func.min(measurement.tobs).filter(measurement.date>start_date)).all(),
    the_max = session.query(func.max(measurement.tobs)).filter(measurement.date>start_date).all()
    
    session.close()

    temp_start = list(np.ravel(temp_sel))

    return jsonify(temp_start,
                   f"The max is {the_max}",
                   f"The min is {the_min}",
                   f"The avg is {the_avg}"
    )

@app.route("/api/v1.0/2012.08.22/2014.02.22")
def end():
    session = Session(engine)

    
    
    temp_sel_2 = session.query(func.avg(measurement.tobs),
             func.min(measurement.tobs),
             func.max(measurement.tobs)).filter(measurement.date>start_date).filter(measurement.date<end_date).all()

    the_avg_2 = session.query(func.avg(measurement.tobs).filter(measurement.date>start_date).filter(measurement.date<end_date)).all(),
    the_min_2 = session.query(func.min(measurement.tobs).filter(measurement.date>start_date).filter(measurement.date<end_date)).all(),
    the_max_2 = session.query(func.max(measurement.tobs)).filter(measurement.date>start_date).filter(measurement.date<end_date).all()
    
    session.close()

    temp_start_2 = list(np.ravel(temp_sel_2))

    return jsonify(temp_start_2,
                   f"The max is {the_max_2}",
                   f"The min is {the_min_2}",
                   f"The avg is {the_avg_2}"
    )

if __name__ == '__main__':
    app.run(debug=True)
