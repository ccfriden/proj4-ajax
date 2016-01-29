"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions
from math import modf

import json
import logging


# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from kilometers, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of kilometers. 
  """
  app.logger.debug("Got a JSON request");
  kilometers = request.args.get('kilometers', 0, type=int)

  if kilometers <= 200:
      return jsonify(result=timesForSpeed(kilometers, 15, 34))
  elif kilometers <= 400:
      return jsonify(result=timesForSpeed(kilometers, 15, 32))
  elif kilometers <= 600:
      return jsonify(result=timesForSpeed(kilometers, 15, 30))
  elif kilometers <= 1000:
      return jsonify(result=timesForSpeed(kilometers, 11.428, 28))
  elif kilometers <= 1300:
      return jsonify(result=timesForSpeed(kilometers, 13.333, 26))
 
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"

###############
# Private Funcs
###############

def timesForSpeed(kilometers, minSpeed, maxSpeed):
    hour = int(modf(kilometers / maxSpeed)[1])
    minutes = int(modf(kilometers / maxSpeed)[0] * 60)
    open = "Opening Time: " + str(hour) + ":" + str(minutes)
    hour = int(modf(kilometers / minSpeed)[1])
    minutes = int(modf(kilometers / minSpeed)[0] * 60)
    close = "   Closing Time: " + str(hour) + ":" + str(minutes)
    return open + close


#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
