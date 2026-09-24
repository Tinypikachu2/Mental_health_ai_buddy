#Tasha Was Here!
import re
from flask import Flask, render_template, request

app = Flask(__name__)

# Master Skill List
MY_SKILLS = [
    'python', 'flask', 'html', 'css', 'git', 'github',
    'render', 'api', 'rest', 'json', 'sql', 'web development'
]

def analyze_job_description(job_text):
    # Convert text to lowercase and remove special characters
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', job_text.lower())
    words_in_job = set(cleaned_text.split())

    # Find overlapping skills
    matched_skills = [skill for skill in MY_SKILLS if skill in words_in_job]
    missing_skills = [skill for skill in MY_SKILLS if skill not in words_in_job]

    # Calculate percentage based on matched skills out of total skills checked
    match_score = round((len(matched_skills) / len(MY_SKILLS)) * 100)

    return {
        'score': match_score,
        'matched': matched_skills,
        'missing': missing_skills
    }

@app.route('/')
@app.route('/matcher', methods=['GET', 'POST'])
def matcher():
    results = None
    if request.method == 'POST':
        job_description = request.form.get('job_description', '')
        if job_description:
            results = analyze_job_description(job_description)

    return render_template('matcher.html', results=results)

if __name__ == "__main__":
    app.run(debug=True, port=5005)
