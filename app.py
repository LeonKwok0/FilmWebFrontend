"""
server side  of TMDB for CSCI571 HW06
@author LiangGuo 
"""

import requests
from datetime import datetime
from flask.globals import request
from flask import jsonify
from flask import Flask, json
from requests.models import PreparedRequest
from werkzeug.datastructures import iter_multi_items

KEY = "bec75727adfa221f20fb0a25788e805c"
BASE = "https://api.themoviedb.org"
IMG_PR = "https://image.tmdb.org/t/p/"
app = Flask(__name__, static_folder="front", static_url_path='')

genre = {10759: 'Action & Adventure', 16: 'Animation', 35: 'Comedy',
         80: 'Crime', 99: 'Documentary', 18: 'Drama',
         10751: 'Family', 10762: 'Kids', 9648: 'Mystery',
         10763: 'News', 10764: 'Reality', 10765: 'Sci-Fi & Fantasy',
         10766: 'Soap', 10767: 'Talk', 10768: 'War & Politics',
         37: 'Western', 28: 'Action', 12: 'Adventure', 14: 'Fantasy',
         36: 'History', 27: 'Horror',
         10402: 'Music', 10749: 'Romance', 878: 'Science Fiction',
         10770: 'TV Movie', 53: 'Thriller', 10752: 'War'}


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
    data = fetch(url)

    resp = []
    for item in data.get("results", [])[:5]:
        path = item.get("backdrop_path")
        if not path:
            path = ""
        resp.append(
            {
                "title": item.get("title"),
                "backdrop_path": IMG_PR+"w780" + path if path else "statics/movie-placeholder.jpg",
                "release_date": item.get("release_date")
            }
        )
    return jsonify(resp)


@app.route("/airtoday")
def fetch_airtoday():
    url = f"{BASE}/3/tv/airing_today?api_key={KEY}"
    data = fetch(url)
    resp = []
    for item in data.get("results", [])[:5]:
        path = item.get("backdrop_path")
        if not path:
            path = ""
        resp.append(
            {
                "name": item.get("name"),
                "backdrop_path": IMG_PR+"w780"+path if path else "",
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
    """
    params: kv, type: movie tv multi
    """
    kv = request.args.get("kv")
    type = request.args.get("type")
    url = f"{BASE}/3/search/{type}?api_key={KEY}&query={kv}&language=en-US&page=1&include_adult=false"
    data = fetch(url)
    res = data.get("results", [])
    resp = []
    for item in res:
        one = {
            k: item.get(k, "") for k in mov_fields
        }
        # for multi type, if this item is tv type OR if query type is tv
        if (item.get("media_type") == "tv") or (type == "tv"):
            one["title"] = item.get("name", "")
            one["release_date"] = item.get("first_air_date", "")
            one["type"] = 1
        elif (item.get("media_type") == "movie") or(type == "movie"):
            one["type"] = 2
        one["genres"] = [genre[gen_id] for gen_id in one["genre_ids"]]

        if not one["poster_path"]:
            one["poster_path"] = "statics/movie_poster.png"
        else:
            one["poster_path"] = "https://image.tmdb.org/t/p/w185" + \
                one["poster_path"]

        for k, val in one.items():
            if not val:
                one[k] = "N/A"

        resp.append(one)
    return jsonify(resp)


@app.route("/media_basic")
def media_basic():
    """fetch deatil info of tv/movies 
    params: type: movie,tv ; media_id
    """
    media_id = request.args.get("media_id")
    type = request.args.get("type")
    url = f"{BASE}/3/{type}/{media_id}?api_key={KEY}&language=en-US"
    
    item = fetch(url)

    one = {}
    # deal with img
    if item["backdrop_path"]:
        one["backdrop_path"] = IMG_PR+"w780" + item["backdrop_path"]
    else:
        one["backdrop_path"] = "statics/movie-placeholder.jpg"
    #  diff key name between tv and movie
    if type == "tv":
        one["name"] = item.get("name")
        one["year"] = item.get("first_air_date")
    else:
        one["name"] = item.get("title")
        one["year"] = item.get("release_date")
    one["year"] = one["year"][:4] if one["year"] else ""
    # genres
    one["genres"] = [gen.get("name") for gen in item.get("genres", [])]
    # spoken_languages
    one["spoken_languages"] = [lag.get("english_name")
                               for lag in item.get("spoken_languages", [])]
    # vote_average
    one["vote_average"] = item.get(
        "vote_average")/2 if item.get("vote_average") else "NA"
    # vote_count
    one["vote_count"] = item.get("vote_count")
    # overview
    one["overview"] = item.get("overview")
    return jsonify(one)

@app.route("/media_cast")
def fetch_cast():
    media_id = request.args.get("media_id")
    type = request.args.get("type")
    url = f"{BASE}/3/{type}/{media_id}/credits?api_key={KEY}&language=en-US"
    data = fetch(url)
    resp = [] 
    for item in data.get("cast",[])[:8]:
        one = {}
        one["name"] = item.get("name")
        path = item.get("profile_path") 
        one["profile_path"] = IMG_PR+"w185"+path if path else "statics/person-placeholder.png"
        one["character"] = item.get("character")
        resp.append(one)
    return jsonify(resp)

@app.route("/media_review")
def fetch_review():
    media_id = request.args.get("media_id")
    type = request.args.get("type")
    url = f"{BASE}/3/{type}/{media_id}/reviews?api_key={KEY}&language=en-US"
    data = fetch(url).get("results",[])
    resp = [] 
    
    for item in data[:5]:
        one = {} 
        one["username"] = item.get("author_details",{}).get("username","")
        one["content"] = item.get("content")
        rating = item.get("author_details",{}).get("rating")
        one["rating"] = rating/2 if rating else -1
        raw_time = item.get("created_at","")[:10]
        print(raw_time)
        if len(raw_time)==10:
            one["created_at"] = f"{raw_time[5:7]}/{raw_time[8:10]}/{raw_time[0:4]}"
        else:
            one["created_at"] = ""
        resp.append(one)
    return jsonify(resp)


def fetch(url):
    retry_time = 0
    while retry_time < 3:
        try:
            data = requests.get(url, verify=False)
            js_data = data.json()
            return js_data
        except requests.exceptions.SSLError as e:
            print("ssl error")
            retry_time += 1
        except Exception:
            retry_time += 1
    return None


def fetch_genre():
    tv_url = f"{BASE}/3/genre/tv/list?api_key={KEY}&language=en-US"
    tv_res = requests.get(tv_url, verify=False).json()
    for item in tv_res.get("genres"):
        genre[item["id"]] = item["name"]
    mov_url = f"{BASE}/3/genre/movie/list?api_key={KEY}&language=en-US"
    mov_res = requests.get(mov_url, verify=False).json()
    for item in mov_res.get("genres"):
        genre[item["id"]] = item["name"]
    print(genre)


def replace_gen(ids):
    return [genre[gen_id] for gen_id in ids]


if __name__ == "__main__":
    # fetch_genre()
    app.run(debug=True)
