# Vishal's Royal Portfolio (starter)

This repository contains a starter portfolio website with a royal color theme.
It includes a Flask backend (contact form that stores leads in PostgreSQL) and
frontend templates (HTML/CSS/JS). Use this package as-is (deploy the Flask app)
or host frontend separately on GitHub Pages and backend on Render/Railway.

## What is included
- `app.py` — Flask app serving all pages and handling the contact form
- `templates/` — HTML templates for index, projects, youtube, contact
- `static/` — CSS, JS, and a placeholder profile image (SVG)
- `requirements.txt`
- `.env.example` & `schema.sql`

## Quick local run (recommended for testing)
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill PostgreSQL credentials.
3. Create the `leads` table in your Postgres database (see `schema.sql`).
4. Run the app:
   ```bash
   python app.py
   ```
5. Visit `http://localhost:5000`

## Deploy options
- **Full app (recommended):** Deploy the entire repo to Render / Railway / Heroku (supports Flask + Postgres).
  - Set environment variables from `.env`
  - Use `gunicorn app:app` as the start command
- **Split (Frontend on GitHub Pages):** If you want only the frontend on GitHub Pages, push the `templates/*.html` content converted to static HTML (or the `static/` folder) and update the contact form action to point to your deployed backend endpoint.

## PostgreSQL schema
Run `schema.sql` to create the leads table.

## Notes
- The repository includes a lightweight fallback: if no DB credentials are provided, submitted leads are appended to `leads_fallback.jsonl` in the project root.
- Replace `static/images/yourphoto.svg` with your real photo (same path) or update the HTML to point to an external image.
