from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt        
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'theansweris42'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{3}$') 
PW_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$")


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/validate', methods=['POST'])
def validate_fields():  
    error = 0        
    if len(request.form['fname']) < 2:
        flash('fname_error')
        error = 1        
    if len(request.form['lname']) < 2:
        flash('lname_error')
        error = 1             
    if not EMAIL_REGEX.match(request.form['email']):
        flash('email_error')
        error = 1               
    if not request.form['pass_it'] == request.form['times_two']:
        flash('match_error')
        error = 1        
    else:
        if not PW_REGEX.match(request.form['pass_it']):
            flash('format_error')
            error = 1            
    if not error == 0:        
        return redirect('/')
    else:
        return redirect('/add_user')
        
            
    
    
        
           
                




























if __name__ == '__main__':
    app.run(debug=True)
