from crypt import methods
from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
import re

@app.route('/items/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':session['user_id']}
    user = User.get_by_id(data)
    items = Item.get_all_user_items()
    return render_template('dashboard.html', user = user, items = items)

@app.route('/my_items/<int:id>')
def my_items(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':id}
    user = User.get_by_id(data)
    items = Item.get_all_user_items()
    return render_template('my_items.html', user = user, items = items)

@app.route('/create_listing')
def create_listing():
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':session['user_id']}
    user = User.get_by_id(data)
    return render_template('create_listing.html', user = user)

# process - add a tree to the database
@app.route('/item/create', methods=['POST'])
def create_item():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "name": request.form["name"],
        "description": request.form["description"],
        "price": request.form["price"],
    }
    if not Item.validate_item(data):
        return redirect('/create_listing')
    Item.create_item(data) 
    print('PASS')
    return redirect('/items/dashboard')

@app.route('/item/info/<int:id>')
def item_info(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':id}
    user = User.get_by_id({'id':session['user_id']})
    item = Item.get_item(data)
    return render_template('item_info.html', user = user, item = item)

@app.route('/payment/info')
def payment_page():
    pass

@app.route('/edit/<int:id>')
def edit_item(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id':session['user_id']})
    item = Item.get_by_id(id)
    return render_template('edit_item.html', user = user, item = item)

@app.route('/listing/update/<int:id>', methods=['POST'])
def update_item(id):
    item_data = {
        "user_id": session['user_id'],
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "price": request.form["price"]
    }
    if Item.validate_item(item_data):
        Item.update(item_data)
        print('PASS')
        return redirect ('/items/dashboard')
    print('FAIL')
    return redirect('/items/dashboard')

# delete tree - remove from database
@app.route('/delete/<int:id>')
def delete(id):
    data = {'id':id}
    Item.delete(data)
    return redirect(f'/my_items/{id}')

