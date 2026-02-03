FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# --- השורה הקריטית ---
# מעתיקה את כל הקבצים מהתיקייה שלך (כולל templates) לתוך הקונטיינר
COPY . . 
# ---------------------

EXPOSE 5000
CMD ["python", "app.py"]
