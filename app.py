from flask import Flask, render_template, jsonify, request
import requests
import os
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', hostname=os.getenv("HOSTNAME", "localhost"))

@app.route('/api/fact')
def get_fact():
    # קבלת הפרמטרים מהמשתמש (שפה וקטגוריה)
    target_lang = request.args.get('lang', 'en')
    category = request.args.get('category', 'random')
    
    try:
        # 1. משיכת עובדה מה-API (באנגלית)
        # הערה: בגרסה מלאה היינו משתמשים ב-Category כדי לבחור API שונה
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        response = requests.get(url)
        fact_en = response.json().get('text')
        
        # 2. תרגום העובדה אם צריך
        if target_lang != 'en':
            translator = GoogleTranslator(source='auto', target=target_lang)
            fact_final = translator.translate(fact_en)
        else:
            fact_final = fact_en
            
        status = "success"
        
    except Exception as e:
        fact_final = "Error fetching data. Try again."
        status = "error"

    return jsonify({
        "fact": fact_final,
        "pod": os.getenv("HOSTNAME", "localhost"),
        "category": category,
        "status": status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
