#Flask application that gathers informtation of SpaceX launches
#creates page in order to display the launch data for failed, successful, and upcoming launches

from flask import Flask, render_template, Blueprint
from datetime import datetime
import requests

app = Flask(__name__, static_url_path="/spacex/static", static_folder="static")
spacex_bp = Blueprint('spacex_bp', __name__, url_prefix='/spacex')

@spacex_bp.route("/")
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

app.register_blueprint(spacex_bp)

if __name__ == "__main__":
    app.run(debug=True)
