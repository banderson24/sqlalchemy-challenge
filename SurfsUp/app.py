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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        #f"/api/v1.0/<start>"
        #f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Query of precipitation data
    # Perform a query to retrieve the data and precipitation scores
    # Used the specific date to go back to rather than a variable because I couldn't make it work
    precipitation_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').all()
    #Close the opened session
    session.close()
    #Create a dictionary from the query results
    all_precipitation = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(station.station).all()
    #close the session
    session.close()
    #Convert results into a normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperature():
    # Query of temperature data
    # Perform a query to retrieve the data and precipitation scores
    # Used the specific date to go back to rather than a variable because I couldn't make it work
    temperature_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-23').all()
    #Close the session
    session.close()
    #Convert results into a normal list
    temperatures = list(np.ravel(temperature_data))
    #Return jsonified results
    return jsonify(temperatures)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

