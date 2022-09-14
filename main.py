from flask import Flask, render_template, jsonify, request, make_response
from db_connection import cursor
from datetime import datetime as dt
from time import sleep

app = Flask(__name__)

cursor.execute("SELECT * FROM floods")
floods = cursor.fetchall()

cursor.execute("SELECT created_utc from floods ORDER BY id DESC LIMIT 1")
last_row_created = dt.fromtimestamp(cursor.fetchone()["created_utc"]).ctime()

@app.route("/")
def index():
    return render_template("index.html", total_floods=len(floods), last_build_date=last_row_created)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/floods")
def get_floods():
    sleep(0.5)

    counter = int(request.args.get("c"))
    per_loading = 10

    if counter == 0:
        print(f"Returning floods 0 to {per_loading}")
        res = make_response(jsonify(floods[0: per_loading]), 200)

    elif counter == len(floods):
        print("No more floods!")
        res = make_response(jsonify({}), 200)

    else:
        print(f"Returning floods {counter} to {counter + per_loading}")
        res = make_response(jsonify(floods[counter: counter + per_loading]), 200)

    return res

@app.route("/search")
def search_floods():
    query = request.args.get("q")

    cursor.execute(f"SELECT title, selftext, full_link, created FROM floods WHERE title LIKE '{query}%' OR selftext LIKE '{query}%' ORDER BY title, selftext")
    results = cursor.fetchall()
    
    return render_template("search.html", query=query, results=results, total_results=len(results))


if __name__ == "__main__":
    app.run()