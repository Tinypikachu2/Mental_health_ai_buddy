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


def respond_to_feeling(name, feeling):
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
<h1>⚠️DISCAIMER⚠️THIS IS FOR ENTERTAINMENT PURPOSES ONLY!</h1>
<h2>DO NOT give any personal or medical info!</h2>
<h2>By using this you understand that this is for entertainment purposes only and have no legal authority</h2>
<h2>if you wish to "talk again" just erase your answers and put new answers in!</h2>
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
<label for="bgColorPicker">Pick a background color:</label>
<input type="color" id="bgColorPicker" value="#ff69b4">
{% if response %}
  <h2>Bot:</h2>
  <p>{{response}}</p>
{% endif %}
<script>
  const bgPicker = document.querySelector('#bgColorPicker');
  bgPicker.addEventListener('input', function (event) {
    document.body.style.backgroundColor = event.target.value;
  });
</script>
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
        response = respond_to_feeling(name, feeling)
    return render_template_string(HTML_PAGE, response=response, name=name, topic=topic, feeling=feeling)


if __name__ == "__main__":
    app.run(debug=True, port=50010)
