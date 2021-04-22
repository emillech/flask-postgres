from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


SERVICE_NAME = 'db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@db'
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


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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
    users = db.session.query(User).all()
    return users_schema.jsonify(users)


@app.route('/show_user/<user_id>', methods=['GET'])
def show_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        return user_schema.jsonify(user)
    return f"No user of id {user_id}"


@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return f'User of id {user_id} deleted'
    return f"No user of id {user_id}"


@app.route('/search', methods=['GET'])
def search():
    first_name = request.args.get("first_name")
    user = db.session.query(User).filter(User.first_name == first_name).first()
    if user:
        return user_schema.jsonify(user)
    return "No such user"


@app.route('/edit_user/<user_id>', methods=['PUT'])
def edit_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        first_name = request.json['first_name']
        user.first_name = first_name
        db.session.commit()
        return f'User of id {user_id} edited'
    return f"No user of id {user_id}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
