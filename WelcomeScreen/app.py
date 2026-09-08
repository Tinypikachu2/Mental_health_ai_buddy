from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def robot():
    robot_face = "🤖"
    if request.method == 'POST':
        feeling = request.form['feeling'].lower().strip()
        if "happy" in feeling or "good" in feeling or "great" in feeling:
            reply = "I'm glad you're feeling good!"
        elif "sad" in feeling or "upset" in feeling:
            reply = "I'm sorry to hear that. I'm here for you."
        else:
            reply = "Thank you for sharing. I'm listening."
        return f"""
            <h1 style='font-size:5em'>{robot_face}</h1>
            <p style='font-size:2em'>{reply}</p>
            <a href="/">Talk again</a>
        """
    else:
        return f"""
            <h1 style='font-size:5em'>{robot_face}</h1>
            <form method="post">
                <label style='font-size:1.5em'>How are you feeling?</label><br>
                <input name="feeling" style='font-size:1.5em'/><br><br>
                <input type="submit" value="Tell the robot!" style='font-size:1em'/>
            </form>
        """

if __name__ == '__main__':
    app.run(debug=True)