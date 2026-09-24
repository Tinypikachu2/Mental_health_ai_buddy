#TashaWasHere
#Gemini helped
from flask import Flask, render_template, request

app = Flask(__name__)

import requests

CLIENT_ID = "bEBpOy8aDzTRZbRNZIK7L"
CLIENT_SECRET = "qwfmrG6o7w17z1IDiQTsQ5EAleWic3bd8Y14H8a4"

url = "https://data.api.xweather.com/conditions/40165"
params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.get(url, params=params)
data = response.json()


import requests

API_KEY = "your_actual_api_key_here"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_msg = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            # Call OpenWeatherMap Current Weather API (units=imperial for Fahrenheit)
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": round(data["main"]["temp"]),
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                    "wind_speed": data["wind"]["speed"]
                }
            else:
                error_msg = "City not found. Please try again."

    return render_template("bot.html", weather=weather_data, error=error_msg)


if __name__ == "__main__":
    app.run(debug=True, port= 50020)

