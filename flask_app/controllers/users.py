from flask_app import app
from flask import render_template,redirect,request,session,flash,Flask,url_for
from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)  
from flask_app.models.user import User
from flask_app.models.pet import Pet
from flask_app.controllers import pets
from flask_mail import Mail, Message
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get("EMAIL_USER"),
    "MAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD")
}

app.config.update(mail_settings)

mail = Mail(app)

s = URLSafeTimedSerializer("thisisasecret")

@app.route("/")
def index():
    
    return render_template("login_reg.html")

@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
        
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "email_is_confirm": "False"
    }
    
    session["email_is_confirm"] = False
    email = request.form['email']
    token = s.dumps(email, salt="email-confirm")
    
    msg = Message("Confirm Email from Speaking for Pets", sender="candicema2018@gmail.com", recipients=[email])
    
    link = url_for("confirm_email", token=token, _external=True)
    
    msg.body = f"Please click the link below to confirm your email: {link}"
    
    mail.send(msg)
    
    user_id = User.create(data)
    session["user_id"] = user_id 
    
    return f"<h1> The email you entered is {email}.<br>Please go to your inbox to confirm your email!</h1>"

@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = s.loads(token, salt="email-confirm", max_age = 3600)
    except SignatureExpired:
        return f"<h1>The token is expired!<br> To resend the link please input your email again: <form action={'/resend'} method={'POST'}><input type={'text'} name={'re_email'}></input>&nbsp;<input type={'submit'} value={'Resend'}></form></h1>"
    
    data = {
        "id": session["user_id"],
        "email_is_confirm": "True"
    }
    User.update(data)
    session["email_is_confirm"] = True

    return redirect("/account")
    

@app.route("/resend", methods=["POST"])
def resend():
    email = request.form['re_email']
    token = s.dumps(email, salt="email-confirm")
    
    msg = Message("Confirm Email from Speaking for Pets", sender="candicema2018@gmail.com", recipients=[email])
    
    link = url_for("confirm_email", token=token, _external=True)
    
    msg.body = f"Please click the link below to confirm your email: {link}"
    
    mail.send(msg)
    
    return f"<h1> The email you entered is {email}.<br>Please go to your inbox to confirm your email!</h1>"

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["lemail"] }
    user_in_db = User.get_by_email(data)
    
    if not user_in_db:
        flash("* Invalid Email/Password", "lemail")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['lpassword']):
        flash("* Invalid Email/Password", "lpassword")
        return redirect("/")
    
    if "remember" in request.form:
        session.permanent = True
    else:
        session.permanent = False
    
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route("/logout")
def logout():  
    if session.permanent == False:
        session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login before trying to go to dashboard page')
        return redirect('/')
    
    if "location" in session:
        session.pop("location")
        session.pop("animal")
        print(session)
    return render_template('dashboard.html')

@app.route("/account")
def acc():
    if 'user_id' not in session:
        flash('Please login before trying to go to dashboard page')
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    user = User.get_user_with_pets(data)
    
    return render_template('account.html',user=user, watch_names = session["watch_name"], watch_urls = session["watch_url"])

@app.route("/watch", methods=["POST"])
def watchlist():
    # session["watch_name"] = request.form["pet_name"]
    if "watch_name" in session:
        watchlist_names = session["watch_name"]
        watchlist_names.append(request.form["pet_name"])
        session["watch_name"] = watchlist_names
    else:
        watchlist_names = []
        watchlist_names.append(request.form["pet_name"])
        session["watch_name"] = watchlist_names
    # session["watch_url"] = request.form["pet_url"]
    if "watch_url" in session:
        watchlist_urls = session["watch_url"]
        watchlist_urls.append(request.form["pet_url"])
        session["watch_url"] =  watchlist_urls
    else:
        watchlist_urls = []
        watchlist_urls.append(request.form["pet_url"])
        session["watch_url"] =  watchlist_urls
    
    return redirect("/account")