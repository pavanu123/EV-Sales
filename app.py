from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
import sqlite3


flask_app = Flask(__name__)
flask_app.secret_key = 'your_secret_key'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'


# Connect to the database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('db_web.db')
cursor = conn.cursor()

# Check if the users table already exists
cursor.execute('''
SELECT name FROM sqlite_master WHERE type='table' AND name='users';
''')

# If the table does not exist, create it
if cursor.fetchone() is None:
    cursor.execute('''
    CREATE TABLE users (
        SNo INTEGER PRIMARY KEY AUTOINCREMENT,
        CNAME TEXT NOT NULL,
        COUNTRY TEXT NOT NULL,
        YEAR INTEGER NOT NULL,
        SALES REAL NOT NULL
    )
    ''')

# Commit the changes and close the connection
conn.commit()
conn.close()

@flask_app.route('/')
def index():
    return render_template("index.html")

@flask_app.route('/history')
def history():
    return render_template('history.html')

@flask_app.route('/evchargingpoints')
def evchargingpoints():
    return render_template('ev charging points.html')



@flask_app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        cname = request.form['cname']
        country = request.form['country']
        year = request.form['year']
        sales = request.form['sales']
        conn=sql.connect("db_web.db")
        cur=conn.cursor()
        cur.execute("INSERT into users (CNAME,COUNTRY,YEAR,SALES) values (?,?,?,?)",(cname,country,year,sales))
        conn.commit()
        flash('Details added','success')
        return redirect(url_for("dashboard"))
    return render_template("add_user.html")

@flask_app.route("/edit_user/<string:sno>", methods=['POST', 'GET'])
def edit_user(sno):
    if request.method == 'POST':
        cname = request.form['cname']
        country = request.form['country']
        year = request.form['year']
        sales = request.form['sales']
        conn = sql.connect("db_web.db")
        cur = conn.cursor()
        cur.execute("update users set CNAME=?, COUNTRY =?,YEAR=?,SALES=? where SNo=?", (cname,country,year,sales,sno))
        conn.commit()
        flash('Details Updated', 'success')
        return redirect(url_for("dashboard"))
    conn = sql.connect("db_web.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("select * from users where SNo=?", (sno,))
    data = cur.fetchone()
    return render_template("edit_user.html", datas=data)

@flask_app.route("/delete_user/<string:sno>", methods=['GET'])
def delete_user(sno):
    conn = sql.connect("db_web.db")
    cur = conn.cursor()
    cur.execute("delete from users where SNo=?", (sno,))
    conn.commit()
    flash('Details Deleted', 'warning')
    return redirect(url_for("dashboard"))



@flask_app.route('/govt')
def govt():
    return render_template('govt.html')

@flask_app.route('/buy')
def buy():
    return render_template('buy.html')


@flask_app.route('/dashboard')
def dashboard():
    conn = sql.connect("db_web.db")
    conn.row_factory = sql.Row  # This allows us to access columns by name
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")  # Query to select all records
    data = cur.fetchall()  # Fetch all records
    conn.close()  # Close the connection
    return render_template('dashboard.html', users=data)


@flask_app.route('/about')
def about():
    return render_template('about.html')

@flask_app.route('/team')
def team():
    return render_template('team.html')

@flask_app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=8005,
        debug=True
    )