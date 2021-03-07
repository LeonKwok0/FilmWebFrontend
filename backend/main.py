"""
server side  of TMDB for CSCI571 HW06
@author LiangGuo 
"""

import requests
from flask.globals import request
from flask import jsonify
from flask import Flask, json
from requests.models import PreparedRequest
KEY = "bec75727adfa221f20fb0a25788e805c"
BASE = "https://api.themoviedb.org"
IMG_PR = "https://image.tmdb.org/t/p/w780"
genre = {10759: 'Action & Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime', 99: 'Documentary', 18: 'Drama',
         10751: 'Family', 10762: 'Kids', 9648: 'Mystery',
         10763: 'News', 10764: 'Reality', 10765: 'Sci-Fi & Fantasy', 
         10766: 'Soap', 10767: 'Talk', 10768: 'War & Politics',
         37: 'Western', 28: 'Action', 12: 'Adventure', 14: 'Fantasy', 36: 'History', 27: 'Horror',
         10402: 'Music', 10749: 'Romance', 878: 'Science Fiction', 10770: 'TV Movie', 53: 'Thriller', 10752: 'War'}
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
    """
    params: kv, type: movie tv multi
    """
    kv = request.args.get("kv")
    type = request.args.get("type")
    url = f"{BASE}/3/search/{type}?api_key={KEY}&query={kv}&language=en-US&page=1&include_adult=false"
    data = requests.get(url, verify=False).json()
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
        elif (item.get("media_type") == "movie") or(type=="movie"):
            one["type"] = 2
        one["genres"] =[genre[gen_id] for gen_id in one["genre_ids"]]
        
        if not one["poster_path"]:
            one["poster_path"] = "statics/movie_poster.png"
        else:
            one["poster_path"] = "https://image.tmdb.org/t/p/w185"+one["poster_path"]
        
        for k,val in one.items():
            if not val:
                one[k] = "N/A"

        resp.append(one)
    return jsonify(resp)


@app.route("/detail")
def detail():

    """fetch deatil info of tv/movies 
    params: type: movie,tv ; media_id
    """
    # basic info 

    # cast

    # review
    pass

def fetch_cast(type,media_id,data):
    pass 

def fetch_review(type,media_id,data):
    pass 




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


"""
basic
v1. id - the id of the movie.
2. title - the title of the movie.
3. runtime - The runtime of the movie.
4. release_date - the date the movie was released.
v5. spoken_languages - different audio languages the movie is available in.
v6. vote_average - the average of ratings given by reviewers.
v7. vote_count - total number of reviews received by the movie.
v8. poster_path - path for the image of the poster.
v9. backdrop_path - path for the larger backdrop image.
v10. genres - genres of the movie.


- 2. episode_run_time - duration of each episode.
- 3. first_air_date - first air date of the show
- 6. name - the name of the tv show.
没用到 7. number_of_seasons - number of seasons the tv show was aired for.
8. overview - the synopsis of the tv show.


https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US
https://api.themoviedb.org/3/tv/{tv_show_id}?api_key=<<api_key>>&language=en-
US


cast all
1. name - Name of the actor
2. profile_path - Path for the image of the actor
3. character - The character played by the actor.
https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=<<api_key>>&language=en-US


https://api.themoviedb.org/3/tv/{tv_show_id}/credits?api_key=<<api_key>>&language=en-US

review 
1. username - The username of the reviewer, inside the author_details object.
2. content - The content of the review
3. rating - The rating given by the reviewer for the movie, inside the author details object.
4. created_at - The date the review was created.
https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key=<<api_key>>&language=en- US&page=1
https://api.themoviedb.org/3/tv/{tv_show_id}/reviews?api_key=<<api_key>>&language=en- US&page=1

"""