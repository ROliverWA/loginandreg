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
    if request.form['form_side']== 'register' :       
        if len(request.form['fname']) < 2:
            flash('fname_error')
            error = 1
        else:
            session['fname'] = request.form['fname']
        if len(request.form['lname']) < 2:
            flash('lname_error')
            error = 1
        else:
            session['lname'] = request.form['lname']             
        if not EMAIL_REGEX.match(request.form['email']):
            flash('email_error')
            error = 1
        else:
            session['email'] = request.form['email']              
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
            mysql = connectToMySQL("loginapp")
            query = "SELECT  * FROM users WHERE email = %(e)s"
            data = {
                "e": request.form['email']
            }
            if_exists = mysql.query_db(query, data)        
            if if_exists:
                flash('already_exists')                
                return redirect('/')
            else:
                i_love_hash = bcrypt.generate_password_hash(request.form['pass_it'])
                mysql = connectToMySQL("loginapp")
                query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at) VALUES (%(fn)s, %(ln)s, %(e)s, %(hash)s, NOW());"   
                data = { "fn": request.form['fname'],
                    "ln": request.form['lname'],
                    "e": request.form['email'],
                    "hash" : i_love_hash
                }
                user_info = mysql.query_db(query, data)
                session.clear()
                session['user'] = user_info
                return redirect('/success')
            
    elif request.form['form_side']=='login':
        
        if not EMAIL_REGEX.match(request.form['log_email']):
            flash("login_no_dice")
            return reroute('/')
        if not PW_REGEX.match(request.form['log_password']):            
            flash("login_no_dice")
            return redirect('/')        
        mysql = connectToMySQL("loginapp")
        query = "SELECT * FROM users WHERE email = %(e)s"
        data = {
            "e" : request.form['log_email']
        }
        user_info = mysql.query_db(query, data)
        i_love_hash = bcrypt.generate_password_hash(request.form['log_password'])
        # flash(i_love_hash)
        # flash(user_info)
        # flash(user_info[0])
        # return render_template('failure.html')
        if bcrypt.check_password_hash(user_info[0]['pw_hash'], request.form['log_password']):
            session.clear()
            session['user'] = user_info[0]['first_name']
            return redirect('/success')
        else:
            flash("login_no_dice")
            return redirect('/')
        
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        

    





























if __name__ == '__main__':
    app.run(debug=True)
