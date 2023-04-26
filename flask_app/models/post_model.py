from flask_app import app
from flask_app.models import user_model
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    db = "river_wave"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_title = data['post_title']
        self.post_content = data['post_content']
        self.date_posted = data['date_posted']
        self.created_by = None
    
    @classmethod
    def save(cls,post_data):
        query = """
                INSERT INTO 
                posts
                (user_id, post_title, post_content, date_posted)
                VALUES
                (%(user_id)s, %(post_title)s, %(post_content)s, %(date_posted)s);
                """
        return connectToMySQL(cls.db).query_db(query,post_data)
    
    @classmethod
    def edit(cls,data):
        query = """
                UPDATE posts
                SET
                post_title = %(post_title)s,
                post_content = %(post_content)s,
                date_posted = %(date_posted)s
                WHERE posts.id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,id):
        query = """
                DELETE FROM posts
                WHERE posts.id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,{'id':id})
    
    @classmethod 
    def get_users_posts(cls):
        query = """
                SELECT * FROM
                posts
                LEFT JOIN users
                ON posts.user_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        all_posts = []
        for row in results:
            post = cls(row)
            user_data = {
                'id':row['users.id'],
                'user_name':row['user_name'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password': ''
            }
            posted_by = user_model.User(user_data)
            post.created_by = posted_by
            all_posts.append(post)
        return all_posts
    
    @classmethod
    def get_post_by_id(cls,post_id):
        query = """
                SELECT * FROM posts
                LEFT JOIN users
                ON posts.user_id = users.id
                WHERE posts.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, {'id' : post_id})
        for row in results:
            post = cls(row)
            user_data = {
                'id':row['users.id'],
                'user_name':row['user_name'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password': ''
            }
            post.created_by = user_model.User(user_data)
        return post
    
    @staticmethod
    def validate_post(post_data):
        is_valid = True
        
        if len(post_data['post_title']) < 1:
            flash('Title must not be blank.', 'post')
            is_valid = False
        
        
        if len(post_data['post_content']) < 1:
            flash('Message must not be blank.', 'post')
            is_valid = False
            
        if post_data['date_posted'] == '':
            flash('Date must not be blank.', 'post')
        
        return is_valid