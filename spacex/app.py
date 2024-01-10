#Flask application that gathers informtation of SpaceX launches
#creates page in order to display the launch data for failed, successful, and upcoming launches

from flask import Flask, render_template
from datetime import datetime
import requests

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", Launches=launches)

@app.template_filter("date_only")
def date_only_filter(s):
    date_object = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.date()

def fetch_spacex_launches():
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    if response.status_code==200:
        return response.json()
    else:
        return []

def categorize_launches(Launches):
    successful = list(filter(lambda x: x["success"] and not x["upcoming"], Launches))
    failed = list(filter(lambda x: not x["success"] and not x["upcoming"], Launches))
    upcoming = list(filter(lambda x: x["upcoming"], Launches))
    
    return {
        "successful": successful,
        "failed": failed,
        "upcoming": upcoming
    }


launches = categorize_launches(fetch_spacex_launches())

app.config["APPLICATION_ROOT"] = "/spacex"
application = DispatcherMiddleware(Flask("main"), {"/spacex": app})

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True, host='0.0.0.0', request_handler="waitress")
