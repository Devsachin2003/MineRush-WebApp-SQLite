# MineRush Web App

MineRush Web App is a Flask-based mining and internship portal backed by SQLite. It includes user and admin login flows, internship application and management, rule and act document browsing, FAQs, glossary pages, profile editing, file uploads, and a chatbot powered by Google Generative AI.

## Features

- User registration, login, and profile management
- Admin dashboard and admin profile management
- Internship browsing, application, approval, and management
- Mining rules, acts, glossary, FAQs, and disclaimer pages
- File, document, and video upload support
- Chatbot endpoint for mining-law related questions
- SQLite-backed storage for users and application data

## Tech Stack

- Python 3
- Flask
- SQLite3
- Flask-Mail
- python-dotenv
- google-generativeai

## Project Structure

- app.py - main Flask application and routes
- fetch_data_from_interndb.py - helper script for database and data fetching
- users.db - main SQLite database used by the app
- templates/ - HTML templates
- static/ - CSS, JS, images, and uploaded assets
- assets/ - additional static web assets

## Prerequisites

- Python 3.14 or compatible Python 3 version
- pip
- A Google Generative AI API key stored in a local `.env` file
- Gmail credentials in `.env` if you want email features to work

## Setup

1. Create and activate a virtual environment.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required packages.

   ```bash
   pip install Flask Flask-Mail python-dotenv google-generativeai
   ```

3. Create a local `.env` file from the example and add your own credentials.

   ```bash
   cp .env.example .env
   ```

4. Update `.env` with a valid Gemini key and optional mail credentials.

   ```env
   GEMINI_API_KEY=your-valid-gemini-api-key
   GEMINI_MODEL=gemini-2.5-flash
   ALLOW_LEGACY_API_KEY_JSON=false
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-gmail-app-password
   ```

## Run the App

Start the Flask server with:

```bash
python app.py
```

The app runs in debug mode and is available at http://127.0.0.1:5000.

## Important Notes

- The app uses users.db as its SQLite database.
- Uploaded files are saved under static/Articles/rules and acts.
- The chatbot model defaults to gemini-2.5-flash and can be changed with `GEMINI_MODEL`.
- Do not commit real API keys or mail passwords. Keep secrets in `.env`.
- The google.generativeai package is deprecated upstream, but it still works with this project for now.

## Git Ignore

This repository ignores local-only files such as .venv/, __pycache__/, *.db, api_key.json, and .env.
