from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', hostname=os.getenv("HOSTNAME", "localhost"))

@app.route('/api/fact')
def get_fact():
    try:
        # פנייה ל-API חיצוני (אנגלית בלבד)
        response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
        fact = response.json().get('text')
        source = "API"
    except:
        fact = "Network error. Even the internet needs a break."
        source = "Error"

    return jsonify({
        "fact": fact,
        "pod": os.getenv("HOSTNAME", "localhost"),
        "source": source
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
