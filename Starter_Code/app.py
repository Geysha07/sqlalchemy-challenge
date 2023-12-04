# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



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
    """List all available api routes."""
    return(
        f"Welcome to Hawaii Weather Data API"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    
    precipitation_results = session.query(measurement.prcp, measurement.date).all()
    
    session.close()

    precipitation_data = []
    for prcp, date in precipitation_results:
        precipitation_dict = []
        precipitation_dict ["precipitation"] = prcp
        precipitation_dict ["date"] = date
        precipitation_data.append(precipitation_dict)
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def station():
    
    session = Session(engine)
    station_results = session.query(station.station).all()

    session.close()

    station_list = []
    for station in station_results:
        stations_list_dict = []
        stations_list_dict['station'] = station
        station_list.append(stations_list_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")



@app.route("/api/v1.0/<start>")




@app.route("/api/v1.0/<start>/<end>")