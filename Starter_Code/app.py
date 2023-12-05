# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
    f"Welcome to the Hawaii Weather API! These are all the available routes.<br/>"
    f"Returns one year of precipitation data: /api/v1.0/precipitation<br/>"
    f"Returns list of weather stations: /api/v1.0/stations<br/>"
    f"Returns dates and temperature observations from the previous year for the most active station: /api/v1.0/tobs<br/>"
    f"Returns list of minimum, maximum and average temperatures for a specified start date: /api/v1.0/START DATE<br/>"
    f"Returns list of minimum, maximum and average temperatures for a specified start-end date: /api/v1.0/START DATE/END DATE<br/>"
    f"NOTE: For start date, please use YYYY-mm-dd format. For start end-date, please use YYYY-mm-dd/YYYY-mm-dd format."
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp)\
    .filter(measurement.date >one_year_prior)\
    .order_by(measurement.date).all()

    session.close()

    precipitation_data =[]
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_data.append(precipitation_dict)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    station_data = session.query(station.station).all()

    session.close()

    station_list = list(np.ravel(station_data))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    tobs_most_active = session.query(measurement.station, measurement.date, measurement.tobs)\
    .filter(measurement.station == 'USC00519281').filter(measurement.date > '2016-08-17' ).all()

    session.close()

    tobs_list = []
    for station, date, tobs in tobs_most_active:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)
    
