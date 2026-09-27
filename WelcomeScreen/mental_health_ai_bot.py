from flask import Flask, render_template_string, request

app = Flask(__name__)

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

if __name__ != "__main__":
    pass
else:
    app.run(debug=True, port=50010)

