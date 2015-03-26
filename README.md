# Dependencies
## Backend
-  sqlite3
-  python
-  flask

## Frontend

-  Bootstrap 
-  jQuery

# Setup
Ensure that the dependencies are installed

Use the commmand: ``` sqlite3 /tmp/flaskr.db < schema.sql ``` to create a new database and table to be stored on the disk at ``` /tmp/flaskr.db``` with the schema specified at ```schema.sql```

# Usage
To start the server use:
``` python flaskr.py ```

Point your browser to ```http://localhost:3000/ ``` to view the tool

# Design 

The basic design is as follows:
- Initialize the database connection each time the server is run
- Defined the root route ('/') to return the ```show_entires.html``` page
- Defined an api endpoint ('/add') to store the input values, calculate bmi and return the percentile value
- Use an ajax request to send the data from a form and output the result bmi and percentile values on the template
- There are two templates being used, the ```layout.html``` which contains the basic layout to be imported to all the other views and the ```show_entries.html``` which is the main page. These are both found in the ```templates/``` directory
- All static content to be served is in the ```static/``` directory
- The ```formsubmit.js``` houses the javascript code to perform the ajax queries and display the response on the page

# References

Used the following page to figure out how to get the percentile value (Definition 1)

http://www.regentsprep.org/regents/math/algebra/AD6/quartiles.htm