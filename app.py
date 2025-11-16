from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy'
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users])


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'id': user.id})