from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

db = "sell_your_junk"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_registration(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Inavlid email address.", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        query = """
                SELECT * FROM users WHERE email = %(email)s
                """
        results = connectToMySQL(db).query_db(query, user)
        if len(results) != 0:
            flash("Email already taken.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # create when needed
    @classmethod
    def get_all(cls):
        pass

