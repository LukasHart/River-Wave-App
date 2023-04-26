from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "river_wave"
    def __init__(self,data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        
    @classmethod 
    def save(cls,user_data):
        query = """
                INSERT INTO users 
                (user_name, first_name, last_name, email, password)
                VALUES 
                (%(user_name)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s); 
                """
        return connectToMySQL(cls.db).query_db(query,user_data)
    
    @classmethod
    def get_by_email(cls,email):
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.db).query_db(query, {'email':email})
        return cls(results[0]) if results else None
    
    @staticmethod
    def validate_registration(reg_data):
        is_valid = True
        
        if User.get_by_email(reg_data['email']) != None:
            is_valid = False
            flash('Email already in use.', 'registration')
        
        if len(reg_data['user_name']) < 4:
            is_valid = False
            flash('Username must be at least 4 characters', 'registration')
        
        if len(reg_data['first_name']) < 2:
            is_valid = False
            flash('First name must be at least 2 characters.', 'registration')
            
        if len(reg_data['last_name']) < 2:
            is_valid = False
            flash('Last name must be at least 2 characters.', 'registration')
            
        if not EMAIL_REGEX.match(reg_data['email']):
            is_valid = False
            flash('Invalid Email.', 'registration')
            
        if len(reg_data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters.', 'registration')
            
        if reg_data['password'] != reg_data['confirm_password']:
            is_valid = False
            flash('Passwords do not match.', 'registration')
            
        return is_valid