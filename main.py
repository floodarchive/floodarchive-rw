from flask import Flask, render_template
from db_connection import cursor
from datetime import datetime as dt

app = Flask(__name__)

@app.route("/")
def index():
    cursor.execute("SELECT * from floods")
    floods = cursor.fetchall()

    cursor.execute("SELECT created_utc from floods ORDER BY id DESC LIMIT 1")
    last_row_created = dt.fromtimestamp(cursor.fetchone()["created_utc"]).ctime()

    return render_template("index.html", submissions=floods, last_flood_date=last_row_created)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run()