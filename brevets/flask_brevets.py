"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import os

import arrow  # Replacement for date_time, based on moment.js
import acp_times  # Brevet time calculations

import config
import sys
import logging

from mongo_brevets import get_brevets, insert_brevets

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

###
# API 
### 

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"


###
# Flask Routes
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    # Arugments
    km = request.args.get('km', 999, type=float)
    date = request.args.get('date', 0, type=str)

    distance = request.args.get('distance', 0, type=float)  # Request the time given
    time = request.args.get('time', 0, type=str)    # Request the time specified

    # Checking
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    # Formating date_time
    date_time = date + ' ' + time + ':00'   # Fix how the date is put in to include the time as well
    arrow_time = arrow.get(date_time, 'YYYY-MM-DD HH:mm:ss')    # Formats the date_time into arrow

    open_time = arrow.get(acp_times.open_time(km, distance, arrow_time))
    
    # Happens on invalid input simply does not return anything helpful
    if open_time == None:
        return error

    open_time = arrow.get(open_time)

    close_time = acp_times.close_time(km, distance, arrow_time)
    
    # Happens on invalid input does not return anything helpful
    if close_time == None:
        return error

    close_time = arrow.get(close_time)  

    result = {"open": open_time.format('YYYY-MM-DD HH:mm'), "close": close_time.format('YYYY-MM-DD HH:mm')}

    return flask.jsonify(result=result)

@app.route("/submit", methods=["POST"])
def submit():
    """
    /submit : inserts a brevet table into the database.

    Accepts POST requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        total_distance = input_json["total_distance"]   # Should be a string containing the total distance of the race 
        date_time = input_json["date_time"]         # Should be a string containing the date_time
        control_data = input_json["control_data"]   # Should be a list of dictionaries of brevet information

        brevets_id = insert_brevets(total_distance, date_time, control_data)  # Make a call to our database file to store the brevets

        return flask.jsonify(brevet={},
                        message="Submitted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brevets_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(brevet={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')


@app.route("/display", methods=["GET"])
def display():
    """
    /display : fetches the latest brevets from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        total_distance, date_time, control_data = get_brevets()   # Fetch the data from the database
        return flask.jsonify(
                brevet={"total_distance" : total_distance,  # Return the data to json
                         "date_time" : date_time,
                         "control_data" : control_data
                        }, 
                status=1,
                message="Successfully fetched the brevets!")
    except:
        return flask.jsonify(
                brevet={}, 
                status=0,
                message="Something went wrong, couldn't fetch any brevets!")

@app.route("/api/brevets", methods=["GET", "POST"])
def all_brevets():
    """
    Gets all brevets from the database
    """
    if request.method == "GET": 
        try:
            out = []
            for brevet in get_all_brevets():
                _id = brevet["_id"]["$oid"]

                total_distance = brevet["total_distance"]
                date_time = brevet["date_time"]
                control_data = brevet["control_data"]

                brevet={"id": _id, 
                        "total_distance": total_distance, 
                        "date_time": date_time, 
                        "control_data": control_data}
                out.append(brevet)

            return flask.jsonify(out)

        except:
            return flask.jsonify(
                    brevet={}, 
                    status=0,
                    message="Uh Oh, no brevet data fetched!")
    
    if request.method == "POST":
        try:
            input_json = request.json
            # if successful, input_json is automatically parsed into a python dictionary

            total_distance = input_json["total_distance"]
            date_time = input_json["date_time"] 
            control_data = input_json["control_data"] 

            _id = insert_brevet(total_distance, date_time, control_data)

            return flask.jsonify(brevet={},
                            message="Succesfully inserted!", 
                            status=1, 
                            mongo_id=_id)
        except:
            return flask.jsonify(brevet={},
                            message="Oh no! Server error!", 
                            status=0, 
                            mongo_id='None')


@app.route("/api/brevet/<id>", methods=["GET", "PUT", "DELETE"])
def specific_brevet(id):
    """
    Requests a single brevet from the database
    """

    if request.method == "GET":
        try:
            brevet = get_control_brevet(id)
            _id = brevet["_id"]["$oid"]

            control_data = brevet["control_data"]
            total_distance = brevet["total_distance"]
            date_time = brevet["date_time"]

            result={"id": _id, 
                    "total_distance": total_distance, 
                    "date_time": date_time, 
                    "control_data": control_data}

            return flask.jsonify(result)

        except:

            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Something went wrong, couldn't fetch any brevet data!")
    
    elif request.method == "PUT":
        try:
            input_json = request.json
            # if successful, input_json is automatically parsed into a python dictionary

            total_distance = input_json["total_distance"] # Should be a string
            date_time = input_json["date_time"] # Should be a string
            control_data = input_json["control_data"] # Should be a list of dictionaries
            
            brevet_update(id, total_distance, date_time, control_data)
            
            return flask.jsonify(
                result={},
                status=1,
                message=f"Updated brevet {id} successfully!")
        except:
            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Uh Oh, unable to update brevet data!")

    elif request.method == "DELETE":
        try:
            delete_brevet(id)
            return flask.jsonify(
                result={},
                status=1,
                message=f"Deleted brevet {id} successfully!")
        except:
            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Uh Oh, was not able to delete brevet data!")







#############


if __name__ == "__main__":
    app.run(port=port, host="0.0.0.0")
