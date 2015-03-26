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
    # order the dataset in desc order by bmi
    # use formula - 100*((i - 0.5)/n)
    # i = the entry number
    # n = total observations
    
    # get all the bmi values from table and order by decending
    query = 'select bmi from entries order by bmi desc'

    # get count of the number of values
    countQuery = 'select count(*) from entries'
    cur = g.db.execute(countQuery)
    count = cur.fetchone()[0]
    cur = g.db.execute(query)

    # create a list of dicts with the necessary information
    items = [dict(bmi=row[0], index=i+1) for i, row in enumerate(cur.fetchall())]

    # calculate the percentile for all the values
    for item in items:
        item['percentile'] = 100*((item['index'] - 0.5)/count)

    # return the dict for which bmi value matches the input value
    return (item for item in items if item['bmi'] == bmi).next()


if __name__ == '__main__':
    app.run()