# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify


# create our little application :)
app = Flask(__name__)
app.config.from_pyfile('dbconfig.py')

# initialize the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# get db data before each request
@app.before_request
def before_request():
    g.db = connect_db()

# remove db data from g after each request
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# default route for homepage
@app.route('/')
def show_entries():
    return render_template('show_entries.html')

# define an api to add a new value and return the percentile with each new value
@app.route('/add', methods=['POST'])
def add_entry():
    # calculate bmi
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    bmi = weight/(height*height)

    # input the data to db
    g.db.execute('insert into entries (height, weight, bmi) values (?, ?, ?)',
                 [height, weight, bmi])
    g.db.commit()

    # get the percentile
    percentile = calculate_percentile(bmi)

    # return the percentile value as json object containing
    # bmi and percentile
    return jsonify(percentile)

def calculate_percentile(bmi):
    # using the forumula:
    # ((B + 0.5 * E)/n ) * 100
    # B = number of bmi's below 'x'
    # E = number of bmi's equal to 'x'
    # n = number of scores
    
    Bquery = 'select count(*) from entries where bmi < ' + str(bmi)
    Equery = 'select count(*) from entries where bmi = ' + str(bmi)

    # get count of the number of values
    countQuery = 'select count(*) from entries'
    count = g.db.execute(countQuery).fetchone()[0]
    B = g.db.execute(Bquery).fetchone()[0]
    E = g.db.execute(Equery).fetchone()[0]
    percentile = float(((B + 0.5*E)/ count)*100)
    displayDict = { 'bmi': '%.2f' % bmi, 'percentile': '%.2f' % percentile }
    return displayDict



if __name__ == '__main__':
    app.run()