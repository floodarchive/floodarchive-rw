from flask import Flask, render_template, jsonify, request, make_response
from db_connection import cursor
from datetime import datetime as dt
from time import sleep

app = Flask(__name__)

@app.route("/")
def index():
    cursor.execute("SELECT COUNT(*) FROM floods")
    total_row_count = cursor.fetchone()["COUNT(*)"]

    cursor.execute("SELECT created_utc from floods ORDER BY id DESC LIMIT 1")
    last_row_created = dt.fromtimestamp(cursor.fetchone()["created_utc"]).ctime()

    return render_template("index.html", total_flood=total_row_count, last_build_date=last_row_created)

@app.route("/about")
def about():
    return render_template("about.html")


cursor.execute("SELECT * FROM floods")
floods = cursor.fetchall()
quantity = 10

@app.route("/api/floods")
def get_floods():
    sleep(0.5)

    if request.args:
        counter = int(request.args.get("c"))

        if counter == 0:
            print(f"Returning floods 0 to {quantity}")
            res = make_response(jsonify(floods[0: quantity]), 200)

        elif counter == len(floods):
            print("No more floods!")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning floods {counter} to {counter + quantity}")
            res = make_response(jsonify(floods[counter: counter + quantity]), 200)

        return res


if __name__ == "__main__":
    app.run()