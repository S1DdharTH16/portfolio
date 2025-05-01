from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # required for flash messages

# Connect to PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

# Routes
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()
        flash('Message sent! ✅')
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)
