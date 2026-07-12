from flask import redirect, render_template, url_for, request, flash
import os
import secrets
from PIL import Image 
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user



from car_app import app, db, bcrypt
from car_app.models import Cars, News, User
from car_app.form import new_car, new_news, new_account, login_account, update_profile



@app.route("/")
def home():
    All_Cars = Cars.query.all()
    return render_template("main/home.html", cars=All_Cars, title="home")

@app.route("/about")
def about():
    return render_template("main/about.html", title="about")

@app.route("/news")
def news():
    allNews = News.query.all()
    return render_template("main/news.html", new=allNews, title="news")

@app.route("/add_new_car", methods=['GET', 'POST'])
def add_new_car():

    form = new_car()
    if form.validate_on_submit():

        image_name = 'default.jpg'

        if form.photo.data:
            file = form.photo.data

            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            image_name = random_hex + f_ext

            upload_path = os.path.join(app.root_path, 'static/uploads', image_name)

            file.save(upload_path)

        car_name = form.name.data
        car_description = form.discrption.data
        car_price = form.price.data
        newCar = Cars(name=car_name, description=car_description, price=car_price, image_file=image_name)
        db.session.add(newCar)
        db.session.commit()
        flash("you add a car seccsassfully")
        return redirect(url_for('home'))
    
    return render_template("main/add_new_car.html", form=form, title="add-new-car")

@app.route("/add_new_news", methods=['GET', 'POST'])
def add_new_news():
    form = new_news()
    if form.validate_on_submit():

        image_name = 'default.jpg'

        if form.photo.data:
            file = form.photo.data

            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            image_name = random_hex + f_ext

            upload_path = os.path.join(app.root_path, 'static/uploads', image_name)

            file.save(upload_path)
        
        news_title = form.title.data
        news_description = form.description.data
        newnews = News(title=news_title, description=news_description, image_file=image_name)
        db.session.add(newnews)
        db.session.commit()
        flash("you add a new seccsasfully")
        return redirect(url_for('news'))
    return render_template("main/add_new_news.html", form=form, title="add-new-news")

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = new_account()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = User(username=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user_data)
        db.session.commit()
        flash("you create a new account succcsussfully")
        return redirect(url_for('login'))
    return render_template("user/create_account.html", form=form, title="creat-account")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = login_account()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user)
            flash("your login is succsusfully")
            return redirect(url_for('home'))
        else:
            flash("Invaled password or email")
    return render_template("user/login.html", form=form, title="login-account")

@app.route("/all_users")
def all_users():
    users = User.query.all() 
    return render_template("main/all_user.html", user=users, title="all-users")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    form = update_profile()
    if form.validate_on_submit():
        if form.profile_pitcir.data:
            random_token = secrets.token_hex(8)
            picture_file_name = random_token + form.profile_pitcir.data.filename
            picture_path = os.path.join(app.root_path, 'static/imges', picture_file_name)

            image = Image.open(form.profile_pitcir.data)
            image.thumbnail(size=(150, 150))
            image.save(picture_path)

            if current_user.image_file:
                os.remove(os.path.join(app.root_path, 'static/imges', current_user.image_file))

            current_user.image_file = picture_file_name

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = hashed_password
        db.session.commit()
        flash("you updata your profile succsusfully")
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("user/profile.html", form=form, title="profile")



