# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import func
from datetime import datetime

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
        f"/api/v1.0/start_date/2015-08-01<br/>"
        f"/api/v1.0/start_date/2015-08-01/end_date/2016-08-01"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query of precipitation data
    # Perform a query to retrieve the data and precipitation scores
    # Used the specific date to go back to rather than a variable because I couldn't make it work
    # Only return data for the last year in the database. Date is one year from end of data
    precipitation_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').all()
    # Close the opened session
    session.close()
    # Create a dictionary from the query results
    all_precipitation = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    # Return jsonified results
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # List out all the stations. Also added the station name here because the station
    # wasn't unique enough to identify
    results = session.query(station.station, station.name).all()
    # close the session
    session.close()
    # Convert results into a list as stated in the instructions
    all_stations = list(np.ravel(results))
    # Return jsonified results
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperature():
    # Query of temperature data
    # Perform a query to retrieve the date and temperature scores
    # Used the specific date to go back to rather than a variable because I couldn't make it work
    # Pull the results from station USC00519281 and only returns data from the last year of data
    temperature_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-23').all()
    # Close the session
    session.close()
    # Convert results into a normal list as stated in instructions
    temperatures = list(np.ravel(temperature_data))
    # Return jsonified results
    return jsonify(temperatures)


@app.route("/api/v1.0/start_date/<start_date>")
def start_date(start_date):
    # Fetch the results whose going back to the start date
    entered_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    # The instructions just said to pull the results from the provided start date in a list
    # so I pulled the results into a list instead of a dictionary
    # Used sel to create my variable for the min, max, and avg
    sel = [func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]
    temp_averages = session.query(*sel).\
        filter(measurement.date >= entered_start_date).all()
    # Close the session
    session.close()
    # Convert the results into a list as specified in the assignment
    averages = list(np.ravel(temp_averages))

    # Return jsonified results
    return jsonify(averages)

@app.route("/api/v1.0/start_date/<start_date>/end_date/<end_date>")
def start_end_date(start_date, end_date):
    # Code to create the provided start date
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    # Code to create the provided end date
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    # Used sel to create my variable for the min, max, and avg
    # Used the provided start and end date to return the results
    sel = [func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]
    temp_averages_range = session.query(*sel).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()
    # Close the session
    session.close()
    # Convert the results into a list. Again it said list instead of dictionary in the assignment
    averages_range = list(np.ravel(temp_averages_range))

    # Return jsonified results
    return jsonify(averages_range)


if __name__ == '__main__':
    app.run(debug=True)

