from flask import Flask, render_template_string, request
import re

app = Flask(__name__)


def respond_to_feeling(name, bot_topic, feeling):
    if any(x in feeling for x in ["happy", "awesome", "good", "great"]):
        return f"Really, that's awesome {name}, I hope that happy feeling continues!"
    elif any(x in feeling for x in ["sad", "upset"]):
        return f"I'm so sorry, {name}. If you want to talk more about it, that's what I'm here for."
    elif any(x in feeling for x in ["tired", "exhausted"]):
        return f"Yeah {name}, that sounds like a lot. I'm here for you."
    elif any(x in feeling for x in ["anxious", "worried", "scared"]):
        return "It's okay to feel that way. Sometimes it helps to talk to a professional; Google can help you find one."
    elif any(x in feeling for x in ["angry", "frustrated"]):
        return f"Yeah {name}, that sounds like a lot. I'm here for you."
    elif any(x in feeling for x in ["hurt", "pain"]):
        return f"I'm so sorry, {name}. If you want to talk more about it, that's what I'm here for but please get professional help."
    else:
        return "Thank you for sharing how you feel. I'm here for you no matter what."


HTML_PAGE = """
<!doctype html>
<title>Tasha's AI Mental Health Bot</title>
<h1>Tasha's AI Mental Health Bot 🤖</h1>
<h1>⚠️DISCLAIMER: FOR ENTERTAIMENT PUROPSES ONLY⚠️</h1>
<h2>Please DO NOT give any personal info other than first name (if you wish)!</h2>
<!doctype html>
<title>Tasha's AI Mental Health Bot</title>
<style>
  body {
    background-color: #ff69b4;
  }
</style>

<form method=post>
  Your name: <input name="name" value="{{name}}" required><br>
  What do you want to talk about?: <input name="topic" value="{{topic}}" required><br>
  How does it make you feel?: <input name="feeling" value="{{feeling}}" required><br>
  <input type="submit" value="Submit">
</form>
{% if response %}
  <h2>Bot:</h2>
  <p>{{response}}</p>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    name = ""
    topic = ""
    feeling = ""
    if request.method == "POST":
        name = request.form["name"]
        topic = request.form["topic"]
        feeling = request.form["feeling"].lower().strip()
        bot_topic = swap_pronouns(topic)
        response = respond_to_feeling(name, bot_topic, feeling)
    return render_template_string(HTML_PAGE, response=response, name=name, topic=topic, feeling=feeling)


if __name__ == "__main__":
    app.run(debug=True, port=50010)
