#Tasha was here
#MaeBots helped with this code

from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

def swap_pronouns(topic):
    rules = [
        (r"\bours\b", "yours"),
        (r"\bOurs\b", "Yours"),
        (r"\bmine\b", "yours"),
        (r"\bMine\b", "Yours"),
        (r"\bour\b", "your"),
        (r"\bOur\b", "Your"),
        (r"\bmy\b", "your"),
        (r"\bMy\b", "Your"),
        (r"\bI\b", "you"),
        (r"\bme\b", "you"),
        (r"\bwe\b", "you"),
        (r"\bWe\b", "You"),
    ]
    for pattern, replacement in rules:
        topic = re.sub(pattern, replacement, topic)
    return topic

def respond_to_feeling(name, bot_topic, feeling):
    feeling = feeling.lower()
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

# ⬇️ PUT THE HTML_PAGE RIGHT AFTER YOUR FUNCTIONS
HTML_PAGE = """
<!doctype html>
<html>
<head>
  <title>Tasha's AI Mental Health Bot</title>
  <style>
    body {
      background-color: {{ bg_color }};
      font-family: Arial, sans-serif;
    }
  </style>
</head>
<body>
<h1>Tasha's AI Mental Health Bot 🤖</h1>
<h2>DISCLAIMER: THIS IS FOR ENTERTAINMENT PURPOSES ONLY!</h2>
<h2>Please DO NOT give any personal or medical info!</h2>

<form method="post">
  Your name: <input name="name" value="{{name}}" required><br>
  What do you want to talk about?: <input name="topic" value="{{topic}}" required><br>
  How does it make you feel?: <input name="feeling" value="{{feeling}}" required><br>

  mood color:
  <input type="color" name="color" value="{{bg_color}}">
  <br>

  <button type="submit">Submit</button>
</form>

{% if response %}
  <h2>Bot:</h2>
  <p>{{response}}</p>
  <p>If you want to talk again, just change what you wrote above and hit Submit 💬</p>
{% endif %}
</body>
</html>
"""

# ⬇️ ROUTE GOES AFTER HTML_PAGE
@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    name = ""
    topic = ""
    feeling = ""
    bg_color = "#ffffff"  # default white

    if request.method == "POST":
        name = request.form["name"]
        topic = request.form["topic"]
        feeling = request.form["feeling"]
        bg_color = request.form.get("color", "#ffffff")

        bot_topic = swap_pronouns(topic)
        response = respond_to_feeling(name, bot_topic, feeling)

    return render_template_string(
        HTML_PAGE,
        response=response,
        name=name,
        topic=topic,
        feeling=feeling,
        bg_color=bg_color,
    )

# ⬇️ KEEP THIS AT THE VERY BOTTOM
if __name__ == "__main__":
    app.run(debug=True, port=5008)