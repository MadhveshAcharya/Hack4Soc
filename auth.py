from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from .views import views
from .models import User
from werkzeug.security import check_password_hash,generate_password_hash
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                print(email,password)
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                return render_template('login.html',status=False)
        else:
            return render_template('login.html',status=False)

    return render_template('login.html',status=True)

@auth.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        student_class = request.form.get('student_class')
        board = request.form.get('board')
        state = request.form.get('state')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'),method='sha256')
        print(email,state,board)

        if len(name) == 0:
            return render_template('signup.html',message='Invalid Name')
        if len(student_class) == 0:
            return render_template('signup.html',message='Invalid Class')
        if len(board) == 0:
            return render_template('signup.html',message='Invalid Board')
        if len(state) == 0:
            return render_template('signup.html',message='Invalid State')
        if int(phone_number) < pow(10,10) and int(phone_number) > pow(10,11):
            return render_template('signup.html',message='Invalid Phone Number')

        user = User(name=name,student_class=student_class,board=board,state=state,phone_number=phone_number,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('views.home')) 
    return render_template('signup.html')

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
