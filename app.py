from flask import Flask, render_template, jsonify, request
import requests
import os
from googletrans import Translator
import random
import math

app = Flask(__name__)
translator = Translator()

FACT_API_URL = os.getenv("FACT_API_URL", "https://uselessfacts.jsph.pl/random.json?language=en")
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")

@app.route('/')
def index():
    return render_template('index.html', hostname=os.getenv("HOSTNAME", "localhost"))

@app.route('/api/fact')
def get_fact():
    target_lang = request.args.get('lang', DEFAULT_LANG)
    category = request.args.get('category', 'random')
    
    try:
        response = requests.get(FACT_API_URL, timeout=5)
        fact_en = response.json().get('text')
        
        if target_lang != 'en':
            try:
                translation = translator.translate(fact_en, dest=target_lang)
                fact_final = translation.text
            except:
                fact_final = fact_en
        else:
            fact_final = fact_en
            
        random_id = random.randint(1, 1000)
        image_url = f"https://picsum.photos/seed/{random_id}/400/250"
        status = "success"
        
    except Exception as e:
        fact_final = "Could not load fact."
        image_url = "https://via.placeholder.com/400x250?text=Error"
        status = "error"

    return jsonify({
        "fact": fact_final,
        "image": image_url,
        "pod": os.getenv("HOSTNAME", "localhost"),
        "status": status
    })

# --- הנשק הסודי: בדיקת עומס ---
@app.route('/api/stress')
def stress_cpu():
    # לולאה שנועדה להעמיס על המעבד באופן מלאכותי
    x = 0
    # רץ 3 מיליון פעמים כדי לגרום למעבד להזיע
    for i in range(3000000): 
        x += math.sqrt(i)
    
    return jsonify({
        "status": "Stress test completed!",
        "result": x,
        "pod": os.getenv("HOSTNAME", "localhost")
    })
# -----------------------------

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
