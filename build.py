from json import loads
from markdown import markdown
from urllib3 import PoolManager
from datetime import datetime as dt

LIMIT = 100
SUBREDDIT = "kopyamakarna"
IGNORE_FLAIRS = ["META", "DUYURU"]
API_BASE_URL = "https://api.pushshift.io/reddit/search/submission"

after = 1540846800  # Subreddit created_utc
all_submissions = []
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

        all_submissions.append(
            {
                "title": submission.get("title"),
                "selftext": selftext,
                "full_link": submission.get("full_link"),
                "created": dt.fromtimestamp(
                    submission.get("created_utc")
                ).ctime(),
            }
        )