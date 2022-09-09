from json import loads
from markdown import markdown
from urllib3 import PoolManager
from datetime import datetime as dt
from db_connection import db, cursor

LIMIT = 100
SUBREDDIT = "kopyamakarna"
IGNORE_FLAIRS = ["META", "DUYURU"]
API_BASE_URL = "https://api.pushshift.io/reddit/search/submission"

cursor.execute("SELECT created_utc from floods ORDER BY id DESC LIMIT 1")
after = cursor.fetchone()["created_utc"] or 1540846800  # Subreddit created_utc
http = PoolManager()

while True:
    response = http.request(
        "GET", API_BASE_URL, fields={
            "subreddit": SUBREDDIT, "after": after, "limit": LIMIT
        }
    )

    if response.status != 200:
        break
    submissions = loads(response.data.decode("utf-8"))["data"]
    if not len(submissions):
        print("Up to date, no new data in API...")
        break
    after = submissions[-1]["created_utc"]

    for submission in submissions:
        if submission.get("link_flair_text", "") in IGNORE_FLAIRS:
            continue

        selftext = markdown(
            submission.get("selftext", "")
        )
        if selftext.strip() in "<p>[removed]</p>":
            continue

        sql = "INSERT INTO floods (title, selftext, full_link, created, created_utc) VALUES (%s, %s, %s, %s, %s)"
        val = (
            submission.get("title"),
            selftext,
            submission.get("full_link"),
            dt.fromtimestamp(submission.get("created_utc")).ctime(),
            submission.get("created_utc")
        )

        cursor.execute(sql, val)
        db.commit()
        print("Data successfully inserted into MySql database...")
