# Tasha Was Here
from flask import Flask, render_template_string, request

app = Flask(__name__)

if any(x in feeling for x in ["happy", "awesome", "good", "great"]):
    return f"God loves seeing his children happy {name}, Keep that {feeling}"
elif any(x in feeling for x in ["sad", "upset", "tired", "exhausted"]):
    return f"I'm so sorry, {name}. God say's to call upon him during troubling times, let's pray things get better, and you start to feel better"
elif any(x in feeling for x in ["anxious", "worried", "scared"]):
    return f"I can understand why you feel that way {name}. Sometimes it helps to pray about it and to a professional; Google can help you find a professional."
elif any(x in feeling for x in ["angry", "frustrated"]):
    return f"Y{name}, pray about and and let God handle it, he's better at handling situations like that, hand over everything to God and he will provide and help you"
elif any(x in feeling for x in ["hurt", "pain"]):
    return f"I'm so sorry, {name}. If you want to talk more about it, that's what I'm here for, we can pray about it, but please get professional help."
else:
    return "Thank you for sharing how you feel. I'm here for you no matter what."


@app.route("/", methods=["GET", "POST"])
@app.route("/christian_mental", methods=["GET", "POST"])
def home():
    response = ""
    name = ""
    topic = ""
    feeling = ""

    if request.method == "POST":
        name = request.form.get("name", "")
        topic = request.form.get("topic", "")
        feeling = request.form.get("feeling", "").lower().strip()

        response = respond_to_feeling(name, feeling)

    return render_template(
        "christan_mental.html",
        response=response,
        name=name,
        topic=topic,
        feeling=feeling
    )


if __name__ == "__main__":
    app.run(debug=True, port=50013)