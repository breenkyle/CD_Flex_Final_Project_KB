from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db_name='final_project_schema'

class User():
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        # self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sellers = None

    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['username']) < 2:
            flash('Username must be at least 2 characters')
            is_valid=False
        # if len(data['last_name']) < 2:
        #     flash('Last name must be at least 2 characters')
        if not EMAIL_REGEX.match(data['email']):
            flash('Email is invalid')
            is_valid=False
        if  User.get_by_email({'email': data['email']}):
            flash('Whoa there Brickster! That Email is already in use!')
            is_valid=False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters, *cough* like Password1')
            is_valid=False
        if not any(char.isdigit() for char in data['password']):
            flash('Password should have at least one number, *cough* like Password1')
            is_valid = False
        if not any(char.isupper() for char in data['password']):
            flash('Password should have at least one uppercase letter, *cough* like Password1')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Sorry Brickaroo, Passwords do not match')
            is_valid=False
        return is_valid

    @classmethod
    def save(cls, data):
        query='INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);'
        return connectToMySQL(db_name).query_db(query, data)


    @classmethod
    def get_by_email(cls, data):
        query='SELECT * FROM users WHERE email = %(email)s'
        data=connectToMySQL(db_name).query_db(query, data)
        if data == ():
            return False
        else:
            return cls(data[0])


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query,data)
        return cls(results[0])