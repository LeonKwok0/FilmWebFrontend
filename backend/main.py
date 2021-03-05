"""
server side  of TMDB for CSCI571 HW06
@author LiangGuo 
"""

import requests
from flask.globals import request
from flask import jsonify
from flask import Flask, json
KEY = "bec75727adfa221f20fb0a25788e805c"
BASE = "https://api.themoviedb.org"
IMG_PR = "https://image.tmdb.org/t/p/w780"

app = Flask(__name__, static_folder="../front", static_url_path='')


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/trending")
def fetch_trending():
    """
    fetch treding movie then return
    return json 
    """
    url = f"{BASE}/3/trending/movie/week?api_key={KEY}"
    data = requests.get(url, verify=False).json()  # TODO error handle here
    resp = []
    for item in data.get("results", [])[:5]:
        path = item.get("backdrop_path")
        if not path:
            path = ""
        resp.append(
            {
                "title": item.get("title"),
                "backdrop_path": IMG_PR + path,
                "release_date": item.get("release_date")
            }
        )
    return jsonify(resp)


@app.route("/airtoday")
def fetch_airtoday():
    url = f"{BASE}/3/tv/airing_today?api_key={KEY}"
    data = requests.get(url, verify=False).json()  # TODO error handle here
    resp = []
    for item in data.get("results", [])[:5]:
        path = item.get("backdrop_path")
        if not path:
            path = ""
        resp.append(
            {
                "name": item.get("name"),
                "backdrop_path": IMG_PR+path if path else "",
                "first_air_date": item.get("first_air_date")
            }
        )
    return jsonify(resp)


mov_fields = ["id", "title", "overview", "poster_path",
              "release_date", "vote_average", "vote_count",
              "genre_ids"]
# tv_fields has "name""first_air_date"

@app.route("/search")
def search():
    kv = request.args.get("kv")
    type = request.args.get("type")
    url = f"{BASE}/3/search/{type}?api_key={KEY}&query={kv}&language=en-US&page=1&include_adult=false"
    data = requests.get(url, verify=False).json()
    res = data.get("results", [])
    resp = []
    for item in res:
        one = {
            k:item.get(k,"") for k in mov_fields
        }
        # for multi type, if this item is tv type OR if query type is tv 
        if (item.get("media_type")=="tv") or (type=="tv"):
            one["title"] = item.get("name","")
            one["release_date"] = item.get("first_air_date","")
        resp.append(one)
    return jsonify(resp)

if __name__ == "__main__":
    app.run(debug=True)
