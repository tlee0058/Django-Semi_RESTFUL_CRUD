from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
app.secret_key = "secret"
import re, md5
from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'friends')

@app.route('/users')
def index():
    all_users = mysql.query_db("SELECT * FROM users")
    return render_template('index.html', all_users = all_users)

@app.route('/users/new')
def new_user():
    
    return render_template('new.html')

@app.route('/users/create', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']

    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at)\
            VALUES (:fn, :ln, :e, NOW(), NOW())"
    data = {
        'fn' : first_name,
        'ln' : last_name,
        'e' : email,
    }
    mysql.query_db(query, data)
    
    return redirect ('/users') 

@app.route('/users/<id>', methods=['POST', 'GET'])
def show(id):
    if request.method == 'POST':
        query = "UPDATE users SET first_name = :fn, last_name = :ln, email = :e\
        WHERE id = :id"
        data = {
            'fn' : request.form['first_name'],
            'ln' : request.form['last_name'],
            'e' : request.form['email'],
            'id' : id,
        }
        mysql.query_db(query, data)
        new_query = "SELECT * FROM users WHERE id= :id"
        new_data = {'id': id}
        person = mysql.query_db(new_query, new_data)
    else:
        query = "SELECT * FROM users WHERE id = :id"
        data = {'id' : id}
        person = mysql.query_db(query, data)
      
    return render_template('show.html', user = person[0])

@app.route('/users/<id>/edit') 
def edit(id):

    query = "SELECT * FROM users WHERE id = :id"
    data = {'id': id}
    person = mysql.query_db(query, data)
    print person
    return render_template('edit.html', user = person[0])

@app.route('/users/<id>/destroy')
def destroy(id):
    query = "DELETE FROM users WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect ('/users')

app.run(debug=True)