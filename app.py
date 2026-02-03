from flask import Flask, render_template, jsonify, request
import requests
import os
from googletrans import Translator
import random

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html', hostname=os.getenv("HOSTNAME", "localhost"))

@app.route('/api/fact')
def get_fact():
    target_lang = request.args.get('lang', 'en')
    category = request.args.get('category', 'random')
    
    try:
        # 1. שליפת עובדה
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        response = requests.get(url, timeout=5)
        fact_en = response.json().get('text')
        
        # 2. תרגום
        if target_lang != 'en':
            translation = translator.translate(fact_en, dest=target_lang)
            fact_final = translation.text
        else:
            fact_final = fact_en
            
        # 3. הגרלת תמונה (חדש!)
        random_id = random.randint(1, 1000)
        image_url = f"https://picsum.photos/seed/{random_id}/400/250"
            
        status = "success"
        
    except Exception as e:
        print(f"Error: {e}")
        fact_final = "לא הצלחנו להביא עובדה כרגע. נסו שוב!" if target_lang == 'he' else "Error fetching data. Try again."
        image_url = "https://picsum.photos/400/250?blur=5" # תמונה מטושטשת במקרה שגיאה
        status = "error"

    return jsonify({
        "fact": fact_final,
        "image": image_url,
        "pod": os.getenv("HOSTNAME", "localhost"),
        "status": status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
