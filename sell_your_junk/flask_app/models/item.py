from sqlite3 import connect
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash
import re

db = "sell_your_junk"

class Item:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @staticmethod
    def validate_item(item):
        is_valid = True
        if len(item['name']) <= 0 or len(item['description']) <= 0 or len(item['price']) <= 0:
            flash("All fields required.")
            is_valid = False
        if len(item['name']) < 3 and len(item['name']) > 0:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(item['description']) < 10 and len(item['description']) > 0:
            flash("Please enter a more detailed description of your item.")
            is_valid = False
        if len(item['price']) < 0:
            flash("Please enter a price for your item.")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_user_items(cls):
        query = "SELECT * FROM users JOIN items ON items.user_id = users.id"
        results = connectToMySQL(db).query_db(query)
        print(results)
        items = []
        for item in results:
            seller = User(item)
            item_data = {
                'id':item['items.id'],
                'name':item['name'],
                'description':item['description'],
                'price':item['price'],
                'created_at':item['created_at'],
                'updated_at':item['updated_at'],
                'user_id':item['user_id']
            }
            seller.item = Item(item_data)
            items.append(seller)
        return items

    @classmethod
    def create_item(cls, data):
        query = "INSERT INTO items (name, description, price, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(price)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_item(cls, data):
        query = "SELECT * FROM items LEFT JOIN users ON items.user_id = users.id WHERE items.id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        item = cls(results[0])
        for row in results:
            user_data = {
                'id':row['id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at']
            }
        item.creator = User(user_data)
        return item

    @classmethod
    def get_by_id(cls, item_id):
        query = "SELECT * FROM items WHERE id = %(id)s"
        data = {'id':item_id}
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE items SET name = %(name)s, desription = %(description)s, price = %(price)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM items WHERE items.id = %(id)s"
        return connectToMySQL(db).query_db(query,data)