from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Connection
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing in .env file")

client = MongoClient(MONGODB_URI)
db = client.flask_db  # Database name
collection = db.users  # Collection name

# API Route
@app.route('/api')
def api():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/todo')
def todo():
    return render_template('todo.html')

# Home → Shows form
@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')

            if not name or not email:
                return render_template('form.html', error="Name and Email are required")

            # Insert into MongoDB
            collection.insert_one({
                "name": name,
                "email": email,
                "created_at": datetime.now()
            })

            return redirect(url_for('success'))

        except Exception as e:
            return render_template('form.html', error=str(e))

    return render_template('form.html')

# Success Page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    # Create sample data.json if not exists
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f:
            json.dump([{"id": 1, "message": "Sample data"}], f)

    app.run(debug=True)
