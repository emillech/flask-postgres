from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=True)
    last_name = db.Column(db.String(100), unique=True)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


@app.route('/')
def index():
    return "Hello world"


@app.route('/add_user', methods=['POST'])
def add_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return f'User {first_name} {last_name} added to db'


@app.route('/all_users', methods=['GET'])
def all_users():
    users = db.session.query(User).first()
    users_schema = UserSchema()
    data = users_schema.dump(users)
    return jsonify(data)


@app.route('/show_user/<id>', methods=['GET'])
def show_user(id):
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)