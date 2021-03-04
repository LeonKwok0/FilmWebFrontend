"""
server side  of TMDB for CSCI571 HW06
@author LiangGuo 
"""

KEY = "bec75727adfa221f20fb0a25788e805c"
BASE = "https://api.themoviedb.org"
IMG_PR = "https://image.tmdb.org/t/p/w780"

from flask import Flask, json
from flask import jsonify
import requests
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello Flask</h1>"

@app.route("/trending")
def fetch_trending():
    """
    fetch treding movie then return
    return json 
    """
    url = f"{BASE}/3/trending/movie/week?api_key={KEY}"
    data = requests.get(url).json() # TODO error handle here
    resp = [] 
    for item in data.get("results",[])[:5]:
        resp.append(
            {
                "title": item.get("title"),
                "backdrop_path": IMG_PR+item.get("backdrop_path"),
                "release_date": item.get("release_date")
            }
        )
    return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True)