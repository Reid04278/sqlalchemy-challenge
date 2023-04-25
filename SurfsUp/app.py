

# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(_name_)




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API Site!<br/>"
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"

    )


    @app.route("/api/v1.0/precipitation")
    def precipitation:
        """Return the precipitation data for the last year"""
        # Calculate the date 1 year ago from the last date of the database
        year_one = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        
        # Next Query the date and precipitation for the last year
        precipitation = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= year_one).all()

            # Finally create a Dict with date as key and prcp as value and return the jsonify values
            precip = {date: prcp for date, prcp in precipitation}
            return jsonify(precip)


            @app.route("/api/v1.0/stations")
            def stations():
                """Returns a list of stations"""
                results = session.query(Station.station).all()

                # Unravel the results into a one-dimensional array and convert it to a list
                stations = list(np.ravel(results))
                return jsonify(stations)


                @app.route("/api/v1.0/tobs")
                def monthly_temp():
                    """Returns the temperature observations (tobs) from the previous year."""
                     
                # Calculate the date 1 year ago from the last date of the database
                year_one = dt.date(2017, 8, 23) - dt.timedelta(days=365)

                # Next query the primary stations of all tobs from the last year
                results = session.query(Measurement.tobs).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= year_one).all()

                    # Unravel the results into a one-dimensional array and convert it to a list
                    temps = list(np.ravel(results))

                    # Return results
                    return jsonify(temps)


                    @app.route("/api/v1.0/temp/<start>")
                    @app.route("api/v1.0/temp/<start>/<end>")
                    def stats(start=None, end=None):
                        """Returns TMIN, TAVG, TMAX"""

                        # Use sel for selection statement
                        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

                        if not end:
                            # Calculate TMIN, TAVG, TMAX for the dates greater than the start
                            results = session.query(*sel).\
                                filter(Measurement.date >= start).all()
                            # Unravel the results into a one-dimensional array and convert it to a list
                            temps = list(np.ravel(results))
                            return jsonify(temps)

                            # Cqlculate TMIN, TAVG, TMAX with start and stop
                            results = session.query(*sel).\
                                filter(Measurement.date >= start).\
                                filter(Measurement.date <= end).all()
                            # Unravel the results into a one-dimensional array and convert it to a list
                            temps = list(np.ravel(results))
                            return jsonify(temps)


                            if _name_ == '_main_':
                                app.run()


                    


                    
        







#################################################


    