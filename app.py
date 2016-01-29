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

  close_times = []
  open_times = []
  closeTimeFinal = [0, 0]
  openTimeFinal = [0, 0]

  if kilometers < 0:
      return jsonify(result="You can't travel negative kilometers stupid!")
  elif kilometers <= 200:
      openTimeFinal = timesForSpeed(kilometers, 34)
      if kilometers == 0:
          closeTimeFinal[0] = 1
      else:
          closeTimeFinal = timesForSpeed(kilometers, 15)
      if openTimeFinal[1] > 60:
          openTimeFinal[0] += openTimeFinal[1] % 60
          openTimeFinal[1] = openTimeFinal[1] // 60
      if closeTimeFinal[1] > 60:
          closeTimeFinal[0] += closeTimeFinal[1] % 60
          closeTimeFinal[1] = closeTimeFinal[1] // 60
      times = "Opening time: " + str(openTimeFinal[0]) + ":" + str(openTimeFinal[1]) + \
              " Closing time: " + str(closeTimeFinal[0]) + ":" + str(closeTimeFinal[1])
      return jsonify(result=times)
  elif kilometers <= 400:
      open_times.append(timesForSpeed(200, 34))
      open_times.append(timesForSpeed(kilometers-200, 32))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(kilometers-200, 15))
      for time in open_times:
          print(str(openTimeFinal[0]) + "\n")
          openTimeFinal[0] += time[0]
          print(str(openTimeFinal[0]) + "\n")
          openTimeFinal[1] += time[1]
      if openTimeFinal[1] > 60:
          openTimeFinal[0] += openTimeFinal[1] % 60
          openTimeFinal[1] = openTimeFinal[1] // 60
      for time in close_times:
          closeTimeFinal[0] += time[0]
          closeTimeFinal[1] += time[1]
      if closeTimeFinal[1] > 60:
          closeTimeFinal[0] += closeTimeFinal[1] % 60
          closeTimeFinal[1] = closeTimeFinal[1] // 60
      times = "Opening time: " + str(openTimeFinal[0]) + ":" + str(openTimeFinal[1]) + \
              " Closing time: " + str(closeTimeFinal[0]) + ":" + str(closeTimeFinal[1])
      return jsonify(result=times)
  elif kilometers <= 600:
      open_times.append(timesForSpeed(200, 34))
      open_times.append(timesForSpeed(200, 32))
      open_times.append(timesForSpeed(kilometers-400, 30))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(kilometers-400, 15))
      for time in open_times:
          openTimeFinal[0] += time[0]
          openTimeFinal[1] += time[1]
      if openTimeFinal[1] > 60:
          openTimeFinal[0] += openTimeFinal[1] % 60
          openTimeFinal[1] = openTimeFinal[1] // 60
      for time in close_times:
          closeTimeFinal[0] += time[0]
          closeTimeFinal[1] += time[1]
      if closeTimeFinal[1] > 60:
          closeTimeFinal[0] += closeTimeFinal[1] % 60
          closeTimeFinal[1] = closeTimeFinal[1] // 60
      times = "Opening time: " + str(openTimeFinal[0]) + ":" + str(openTimeFinal[1]) + \
              " Closing time: " + str(closeTimeFinal[0]) + ":" + str(closeTimeFinal[1])
      return jsonify(result=times)
  elif kilometers <= 1000:
      open_times.append(timesForSpeed(200, 34))
      open_times.append(timesForSpeed(200, 32))
      open_times.append(timesForSpeed(200, 30))
      open_times.append(timesForSpeed(kilometers-600, 28))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(kilometers-600, 11.428))
      for time in open_times:
          openTimeFinal[0] += time[0]
          openTimeFinal[1] += time[1]
      if openTimeFinal[1] > 60:
          openTimeFinal[0] += openTimeFinal[1] % 60
          openTimeFinal[1] = openTimeFinal[1] // 60
      for time in close_times:
          closeTimeFinal[0] += time[0]
          closeTimeFinal[1] += time[1]
      if closeTimeFinal[1] > 60:
          closeTimeFinal[0] += closeTimeFinal[1] % 60
          closeTimeFinal[1] = closeTimeFinal[1] // 60
      times = "Opening time: " + str(openTimeFinal[0]) + ":" + str(openTimeFinal[1]) + \
              " Closing time: " + str(closeTimeFinal[0]) + ":" + str(closeTimeFinal[1])
      return jsonify(result=times)
  elif kilometers <= 1300:
      open_times.append(timesForSpeed(200, 34))
      open_times.append(timesForSpeed(200, 32))
      open_times.append(timesForSpeed(200, 30))
      open_times.append(timesForSpeed(400, 28))
      open_times.append(timesForSpeed(kilometers-1000, 26))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(200, 15))
      close_times.append(timesForSpeed(400, 11.428))
      close_times.append(timesForSpeed(kilometers-1000, 13.333))
      for time in open_times:
          openTimeFinal[0] += time[0]
          openTimeFinal[1] += time[1]
      if openTimeFinal[1] > 60:
          openTimeFinal[0] += openTimeFinal[1] % 60
          openTimeFinal[1] = openTimeFinal[1] // 60
      for time in close_times:
          closeTimeFinal[0] += time[0]
          closeTimeFinal[1] += time[1]
      if closeTimeFinal[1] > 60:
          closeTimeFinal[0] += closeTimeFinal[1] % 60
          closeTimeFinal[1] = closeTimeFinal[1] // 60
      times = "Opening time: " + str(openTimeFinal[0]) + ":" + str(openTimeFinal[1]) + \
              " Closing time: " + str(closeTimeFinal[0]) + ":" + str(closeTimeFinal[1])
      return jsonify(result=times)
  else:
      return jsonify(result="Must be 1300 or kilometers!")
 
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

def timesForSpeed(kilometers, speed):
    hour = int(modf(kilometers / speed)[1])
    minutes = int(modf(kilometers / speed)[0] * 60)
    return [hour, minutes]


#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
