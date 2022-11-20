# imports
import numpy as np
import datetime as dt
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
Base.prepare(engine, reflect=True)
# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Homepage
@app.route("/")
def homepage():
    # List all the available routes
    return(
        f"<b>Available Routes:</b><br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/TYPE START YEAR (format yyyy-mm-dd)<br/>"
        f"/api/v1.0/TYPE START AND END YEAR (format yyyy-mm-dd/yyyy-mm-dd)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
    session = Session(engine)

    year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=366)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).all()

    session.close()

    # Convert results to a dictionary using date as the key and prcp as the value.
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    session = Session(engine)

    year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=366)

    results = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= year_ago).all()

    session.close()

    # Convert results to a dictionary
    tobs_list = []
    for tobs, date in results:
        tobs_dict = {}
        tobs_dict['tobs'] = tobs
        tobs_dict['date'] = date
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range.
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Convert results to a dictionary
    temp_list = []
    for min, max, avg, in results:
        temp_dict = {}
        temp_dict['minimum temperature'] = min
        temp_dict['maximum temperature'] = max
        temp_dict['average temperature'] = avg
        temp_list.append(temp_dict)

    # Try statement that returns a 404 if a minimum temperature is not found
    try:
        for each in temp_list:
            if temp_list[0]['minimum temperature'] > -999:
                return jsonify(each)
    except TypeError:
        return jsonify({"error": f"Data with date {start} not found."}), 404

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert results to a dictionary
    temp_list = []
    for min, max, avg, in results:
        temp_dict = {}
        temp_dict['minimum temperature'] = min
        temp_dict['maximum temperature'] = max
        temp_dict['average temperature'] = avg
        temp_list.append(temp_dict)

    # Try statement that returns a 404 if a minimum temperature is not found
    try:
        for each in temp_list:
            if temp_list[0]['minimum temperature'] > -999:
                return jsonify(each)
    except TypeError:
        return jsonify({"error": f"No data found between the dates of {start} and {end}"}), 404

# Plate of boilers
if __name__ == '__main__':
    app.run(debug=True)