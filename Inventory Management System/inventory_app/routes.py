from inventory_app import app, db, bcrypt
from inventory_app.froms import create_account_form, login_account_form, add_item_Form, profile_form, update_item_Form
from inventory_app.models import Users, Item
import os, secrets
from PIL import Image 
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps

from flask import render_template, redirect, url_for, request, abort, flash

# الحماية
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. التحقق من تسجيل الدخول
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # 2. التحقق من أن الصلاحية هي أدمن
        if current_user.role != 'admin':
            abort(403) # إرجاع خطأ "غير مصرح لك بالدخول"
            
        return f(*args, **kwargs)
    return decorated_function

# للمستخدمين
@app.route("/")
def home():
    item = Item.query.all()
    return render_template('main/home.html', title='الصفحة الرئيسية', item=item)

@app.route("/create_account", methods=['GET', 'POST'])
def regester():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = create_account_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Users(
            name = form.username.data,
            email = form.email.data,
            password = hashed_password,
            role = 'user'
        )
        db.session.add(new_user)
        db.session.commit()
        flash("تم إنشاء الحساب بنجاح , يمكنك الان تسجيل الدخول", 'success')
        return redirect(url_for('login'))
    return render_template('user/regester.html', title='إنشاء حساب', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = login_account_form()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user)
            flash("تم تسجيل الدخول بنجاح", "success")
            return redirect(url_for('home'))
        else:
            flash("البريد او كلمة السر غير صحيحة", 'error')
    return render_template('user/login.html', title='دخول بحسابك', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = profile_form()
    if form.validate_on_submit():
        # 1. إذا قام المستخدم برفع صورة جديدة
        if form.image_url.data:
            random_token = secrets.token_hex(8)
            picture_file_name = random_token + form.image_url.data.filename
            picture_path = os.path.join(app.root_path, 'static/profile', picture_file_name)

            image = Image.open(form.image_url.data)
            image.thumbnail(size=(150, 150))
            image.save(picture_path)

            # احذف الصورة القديمة فقط إذا لم تكن الصورة الافتراضية للموقع
            if current_user.image_url and current_user.image_url != 'default.jpg': 
                try:
                    os.remove(os.path.join(app.root_path, 'static/profile', current_user.image_url))
                except FileNotFoundError:
                    pass # إذا لم يجد الملف لا توجد مشكلة، تابع العمل
            
            # تحديث اسم الصورة في قاعدة البيانات يحدث هنا "داخل" الشرط فقط
            current_user.image_url = picture_file_name

        # 2. تحديث باقي البيانات (خارج شرط الصورة لأنها تتحدث دائماً)
        current_user.name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("تم تعديل الملف الشخصي بنجاح", 'success')
        return redirect(url_for('profile'))
        
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
    else:
        flash("أعد المحاولة مرة أخرى", 'error')
    return render_template('user/profile.html', title='الملف الشخصي', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('home'))


# للأدمن
@app.route("/admin_control")
@admin_required
def admin_control():  
    user = Users.query.all()
    item = Item.query.all()
    return render_template('admin/admin_control.html', title='لوحة التحكم', user=user, item=item)


@app.route("/admin_user")
@admin_required
def admin_user():
    user = Users.query.all()
    return render_template('admin/admin_user.html', title='إدارة المستخدمين', user=user)


@app.route('/admin_add_item', methods=['GET', 'POST'])
@admin_required
def admin_add_item():
    form = add_item_Form()
    if form.validate_on_submit():

        image_name = 'hello.png'

        if form.image_url.data:
            file = form.image_url.data

            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            image_name = random_hex + f_ext

            upload_path = os.path.join(app.root_path, 'static/item_image', image_name)

            file.save(upload_path)

        new_item = Item(
            name = form.name.data,
            description = form.description.data,
            image_url = image_name,
            price = form.price.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash('تم إضافة المنتج بنجاح', 'success')
        return redirect(url_for('admin_item'))

    return render_template('admin/admin_add_item.html', title='إضافة منتج', form=form)


@app.route('/admin_item')
@admin_required
def admin_item():
    item = Item.query.all()
    return render_template('admin/admin_item.html', title='عرض المنتجات', item=item)


@app.route("/delete/<int:id>")
def delete(id):
    dell = Item.query.get_or_404(id)
    db.session.delete(dell)
    db.session.commit()
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('admin_item'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_update(id):
    item = Item.query.get_or_404(id)

    form = update_item_Form()
    if form.validate_on_submit():

        if form.image_url.data:
            file = form.image_url.data

            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            image_name = random_hex + f_ext

            upload_path = os.path.join(app.root_path, 'static/item_image', image_name)

            file.save(upload_path)

        item.name = form.name.data
        item.description = form.description.data
        item.image_url = image_name
        item.price = form.price.data
        db.session.commit()
        flash('تم تعديل المنتج بنجاح', 'success')
        return redirect(url_for('admin_item'))
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.price.data = item.price
    else:
        flash('أعد المحاولة مرة أخرى', 'error')
    return render_template('admin/admin_update.html', title='تعديل المنتج', form=form)


@app.route('/dell/<int:id>')
def delelte_user(id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        abort(403)
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('تم حذف المستخدم بنجاح', 'success')
    return redirect(url_for('admin_user'))



@app.route("/update_user/<int:id>")
@admin_required
def update_user(id):
    role = Users.query.get_or_404(id)
    role.role = 'admin'
    db.session.commit()
    flash('تم ترقية المستخدم بنجاح', 'success')
    return redirect(url_for('admin_user'))


@app.route("/indate_user/<int:id>")
@admin_required
def indate_user(id):
    role = Users.query.get_or_404(id)
    role.role = 'user'
    db.session.commit()
    flash('تم خفض المستخدم بنجاح', 'success')
    return redirect(url_for('admin_user'))

