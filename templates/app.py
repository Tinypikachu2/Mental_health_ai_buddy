#TashaWasHere
#Gemini helped
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Xweather Credentials
CLIENT_ID = "bEBpOy8aDzTRZbRNZIK7L"
CLIENT_SECRET = "qwfmrG6o7w17z1IDiQTsQ5EAleWic3bd8Y14H8a4"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_msg = None

    if request.method == "POST":
        location = request.form.get("city")
        if location:
            # Xweather Conditions Endpoint
            url = f"https://data.api.xweather.com/conditions/{location}"
            params = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }

            response = requests.get(url, params=params)
            print("Status Code:", response.status_code)
            data = response.json()
            print("API Response:", data)  # Prints output to PyCharm console

            if response.status_code == 200 and data.get("success"):
                if data.get("response"):
                    result = data["response"][0]
                    ob = result.get("ob", {})

                    weather_data = {
                        "city": result.get("place", {}).get("name", location).title(),
                        "country": result.get("place", {}).get("country", "").upper(),
                        "temp": round(ob.get("tempF", 0)),
                        "humidity": ob.get("humidity", 0),
                        "description": str(ob.get("weather", "")).title(),
                        "wind_speed": round(ob.get("windSpeedMPH", 0))
                    }
                else:
                    error_msg = "No weather data found for that location."
            else:
                error_msg = data.get("error", {}).get("description", "Location not found or API error.")

    return render_template("index.html", weather=weather_data, error=error_msg)


if __name__ == "__main__":
    app.run(debug=True, port=80010)

