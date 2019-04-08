from flask import Flask , render_template,session,redirect,request, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = connectToMySQL('users_db')
app.secret_key = 'bla'

@app.route('/')
def landing():
    if 'first_name' not in session:
        session['first_name']=''
        session['last_name']=''
        session['email']=''

    return render_template("landing.html")
@app.route('/process', methods=['post'])
def register():
    session['first_name']=''
    session['last_name']=''
    session['email']=''
    count = 0
    # query='SELECT email from users where email="shxwnpcw@hotmail.com";'
    # print(mysql.query_db(query))
    # users =
    randomval = mysql.query_db('SELECT email from users where email="1";')
    print(randomval)
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    for i in request.form['email']:
        if i == '@':
            count+=1
    if len(request.form['firstname']) < 2 or  any(i.isdigit() for i in request.form['firstname'])== True:
        flash("First name requires more than 2 charaters and can only contain letters", 'first_name_error')
    elif len(request.form['lastname']) < 2 or  any(i.isdigit() for i in request.form['firstname'])== True:
        flash("Last name requires more than 2 charaters and can only contain letters", 'last_name_error')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'email_error')
    elif mysql.query_db('SELECT email from users where email="'+request.form['email']+'";') != randomval:
        flash("Email already in use!",'email_error')
    elif any(i.isdigit() for i in request.form['password']) ==False or len(request.form['password']) < 6:
        flash("Password contain at least 1 number and must be longer than 6 charaters","password_error")
    elif request.form['password'] != request.form['cmpassword']:
        flash('Passwords do not match!','confirm_pass_error')
    else:
        data = {
            'first_name':request.form['firstname'],
            'last_name': request.form['lastname'],
            'email'     :request.form['email'],
            'password'  : bcrypt.generate_password_hash(request.form['password'])
        }

        flash('Successful Registration!', 'success')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s, NOW(), NOW());"
        print(query)
        mysql.query_db(query, data)
    session['first_name']= request.form['firstname']
    session['last_name']= request.form['lastname']
    session['email']= request.form['email']
    return redirect("/")

@app.route('/login', methods=['post'])
def login():
    query='SELECT * from users where email = %(email)s;'
    data = {
        'email':request.form['email']
    }
    users =mysql.query_db(query,data)
    print(users)
    for i in users:
        print(bcrypt.check_password_hash(i['password'], request.form['password']))
        if i['email'] == request.form['email'] and bcrypt.check_password_hash(i['password'], request.form['password']) ==True:
            session['currectid'] = i['id']
            print("logged in!")
        else:
            print('failed to log in')
            flash('You could not be logged in','failedLogin')
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)