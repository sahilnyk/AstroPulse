from django.shortcuts import render
import requests
from datetime import datetime, date, timedelta


# Astronomy of the day 

def home_view(request):
    selected_date = request.GET.get("date")
    show_all = request.GET.get("all")

    apod_data = []
    today = datetime.today().date()

    if show_all == "true":
        # Get last 10 days of APODs
        for i in range(10):
            date = (today - timedelta(days=i)).isoformat()
            try:
                res = requests.get("https://api.nasa.gov/planetary/apod", params={
                    "api_key": "qlwIBry7tXiaLw8P4ebAVvq4tA2YahTwyZFxQJOi",
                    "date": date
                })
                if res.status_code == 200:
                    data = res.json()
                    apod_data.append({
                        "title": data.get("title"),
                        "image_url": data.get("url"),
                        "description": data.get("explanation"),
                        "date": data.get("date"),
                        "media_type": data.get("media_type", "image")
                    })
            except:
                continue
    else:
        # Show specific date or today's
        date = selected_date or today.isoformat()
        try:
            res = requests.get("https://api.nasa.gov/planetary/apod", params={
                "api_key": "qlwIBry7tXiaLw8P4ebAVvq4tA2YahTwyZFxQJOi",
                "date": date
            })
            if res.status_code == 200:
                data = res.json()
                apod_data.append({
                    "title": data.get("title"),
                    "image_url": data.get("url"),
                    "description": data.get("explanation"),
                    "date": data.get("date"),
                    "media_type": data.get("media_type", "image")
                })
        except:
            pass

    return render(request, "home.html", {
        "apods": apod_data,
        "sel_date": selected_date,
        "show_all": show_all == "true"
    })



# space Information
def today_in_space(request):
    sel_date = request.GET.get("date", date.today().isoformat())
    category = request.GET.get("category", "news")

    # Fetch space news
    news_res = requests.get(
        f"https://api.spaceflightnewsapi.net/v4/articles/?_limit=10&_sort=published_at:desc&published_at__gte={sel_date}"
    )
    headlines = news_res.json().get("results", []) if news_res.ok else []

    # Launches
    upcoming = []
    past = []
    if category in ("launches", "all"):
        up = requests.get("https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=5")
        past_r = requests.get("https://ll.thespacedevs.com/2.2.0/launch/previous/?limit=5")
        upcoming = up.json().get("results", []) if up.ok else []
        past = past_r.json().get("results", []) if past_r.ok else []

    # Expeditions
    expeditions = []
    if category in ("missions", "all"):
        exp_r = requests.get("https://ll.thespacedevs.com/2.2.0/expedition/?limit=5")
        expeditions = exp_r.json().get("results", []) if exp_r.ok else []

    return render(request, "today_in_space.html", {
        "sel_date": sel_date,
        "category": category,
        "headlines": headlines,
        "upcoming": upcoming,
        "past": past,
        "expeditions": expeditions,
    })





# Quizzes -
def quizzes(request):
    try:
        res = requests.get(
            "https://opentdb.com/api.php",
            params={
                "amount": 5,
                "category": 17,  # Science & Nature (includes space)
                "type": "multiple",
                "difficulty": "medium",
                "encode": "url3986"
            }
        )
        data = res.json()
        questions = []
        if data.get("response_code") == 0:
            for q in data["results"]:
                import urllib.parse
                questions.append({
                    "question": urllib.parse.unquote(q["question"]),
                    "choices": [urllib.parse.unquote(c) for c in q["incorrect_answers"]] + [urllib.parse.unquote(q["correct_answer"])],
                    "answer": urllib.parse.unquote(q["correct_answer"])
                })
                questions[-1]["choices"].sort()  # shuffle or sort as needed
        else:
            questions = []
    except:
        questions = []

    return render(request, "quizzes.html", {"questions": questions})








def isro_tweet(request):
    return render(request, "isro_tweet.html")