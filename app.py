from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

from urllib.parse import urlparse

DATABASE_URL = os.environ.get("DATABASE_URL")  # provided by Render

def get_db_connection():
    if not DATABASE_URL:
        return None
    # psycopg2 works with a postgres URL directly
    conn = psycopg2.connect(DATABASE_URL)
    return conn


# DATABASE_URL = os.environ.get("DATABASE_URL")

# def get_db_connection():
#     db_host = os.getenv('DB_HOST')
#     db_name = os.getenv('DB_NAME')
#     db_user = os.getenv('DB_USER')
#     db_pass = os.getenv('DB_PASSWORD')
#     if not all([db_host, db_name, db_user, db_pass]):
#         return None
#     return psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)


@app.route('/')
def home():
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/youtube')
def youtube():
    return render_template('youtube.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        conn = get_db_connection()
        if conn is None:
            # If DB not configured, still accept but save to a local file as fallback
            with open('leads_fallback.jsonl', 'a', encoding='utf-8') as f:
                import json, datetime
                f.write(json.dumps({'name': name, 'email': email, 'message': message, 'ts': str(datetime.datetime.utcnow())}) + '\n')
            return redirect(url_for('contact') + '?saved=fallback')

        cur = conn.cursor()
        cur.execute("""INSERT INTO leads (name, email, message) VALUES (%s, %s, %s)""", (name, email, message))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('contact') + '?saved=true')

    saved = request.args.get('saved')
    return render_template('contact.html', saved=saved)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
