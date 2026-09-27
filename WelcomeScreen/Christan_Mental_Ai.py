# Tasha Was Here
from flask import Flask, render_template, request

app = Flask(__name__)


def respond_to_feeling(name, feeling):
    if any(x in feeling for x in ["happy", "awesome", "good", "great"]):
        return f"Really, that's awesome {name}, I hope that happy feeling continues, God loves seeing his children happy!"
    elif any(x in feeling for x in ["sad", "upset"]):
        return f"I'm so sorry, {name}. If you want to talk more about it, that's what I'm here for, it also helps to pray about it."
    elif any(x in feeling for x in ["tired", "exhausted"]):
        return f"Yeah {name}, that sounds like a lot. Pray to God about it, always hand over your troubles to God, he can sort it out!"
    elif any(x in feeling for x in ["anxious", "worried", "scared"]):
        return "It's understandable to feel that way. Sometimes it helps to pray about it and talk to a professional; Google can help you find one. There is also a link to a free bible!"
    elif any(x in feeling for x in ["angry", "frustrated"]):
        return f"Yeah {name}, that sounds like a lot. God is here for you, as am I."
    elif any(x in feeling for x in ["hurt", "pain"]):
        return f"I'm so sorry, {name}. If you want to talk more about it, that's what I'm here for, also pray and reading the bible but please get professional help."
    else:
        return "Thank you for sharing how you feel. We can pray about it also, I'm here for you no matter what."


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
    app.run(debug=True, port=5006)
