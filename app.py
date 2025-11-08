from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from datetime import datetime
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SECRET_KEY", "temporary_secret_key")

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    """Return a PostgreSQL connection or None if DB not configured"""
    if not DATABASE_URL:
        return None
    return psycopg2.connect(DATABASE_URL)


# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/youtube')
def youtube():
    return render_template('youtube.html')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Extract form data
        name = request.form.get("name")
        email = request.form.get("email")
        user_type = request.form.get("user_type")
        company = request.form.get("company", "")
        position = request.form.get("position", "")
        project = request.form.get("project", "")
        budget = request.form.get("budget", "")
        goal = request.form.get("goal", "")
        timeline = request.form.get("timeline", "")
        message = request.form.get("message", "")

        # Combine extra info as one text block
        extra_info = json.dumps({
            "position": position,
            "project": project,
            "budget": budget,
            "goal": goal,
            "timeline": timeline
        }, ensure_ascii=False)

        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS leads (
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        user_type TEXT,
                        company TEXT,
                        message TEXT,
                        extra_info JSONB,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                    """
                )
                conn.commit()

                cur.execute(
                    """
                    INSERT INTO leads (name, email, user_type, company, message, extra_info)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (name, email, user_type, company, message, extra_info)
                )
                conn.commit()
                cur.close()
                conn.close()
                flash("Your information has been submitted successfully!", "success")
                return redirect(url_for("contact") + "?saved=true")

            except Exception as e:
                print("Error:", e)
                flash("Database error occurred, saved locally instead.", "warning")

                # Fallback to local storage
                with open("leads_fallback.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "name": name,
                        "email": email,
                        "user_type": user_type,
                        "company": company,
                        "message": message,
                        "extra_info": extra_info,
                        "timestamp": str(datetime.utcnow())
                    }) + "\n")
                return redirect(url_for("contact") + "?saved=fallback")
        else:
            # If no DB configured, fallback to file
            with open("leads_fallback.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "name": name,
                    "email": email,
                    "user_type": user_type,
                    "company": company,
                    "message": message,
                    "extra_info": extra_info,
                    "timestamp": str(datetime.utcnow())
                }) + "\n")
            flash("Saved locally (DB not configured).", "warning")
            return redirect(url_for("contact") + "?saved=fallback")

    saved = request.args.get("saved")
    return render_template("contact.html", saved=saved)


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
