from flask import render_template, redirect, url_for, request
from personal_blog import app, db
from personal_blog.form import add_new_blog_form, add_new_part_form, update_new_blog_form
from personal_blog.models import Blog, Part


@app.route("/")
def home():
    blog = Blog.query.all()
    return render_template("home.html", title="home", blog=blog)



@app.route("/blog", methods=['GET', 'POST'])
def add_blog():
    form = add_new_blog_form()
    if form.validate_on_submit():
        # نتحقق أولاً أن المستخدم اختار قسماً بالفعل لتجنب أخطاء الـ None
        if form.part.data:
            new_blog = Blog(
                name=form.title.data, 
                discription=form.description.data, 
                part_id=form.part.data.id  # <-- التعديل هنا (إضافة .id)
            )
            db.session.add(new_blog)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("add_blog.html", title="add-blog", form=form)



@app.route("/part", methods=['GET', 'POST'])
def add_part():
    form = add_new_part_form()
    if form.validate_on_submit():
        new_part = Part(name=form.part.data)
        db.session.add(new_part)
        db.session.commit()
        return redirect(url_for('home'))


    return render_template("add_part.html", title="add-part", form=form)

@app.route('/dell/<int:id_blog>', methods=['GET', 'POST'])
def dell(id_blog):

    test = Blog.query.get_or_404(id_blog)

    db.session.delete(test)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    test = Blog.query.get_or_404(id)
    form = update_new_blog_form()
    if form.validate_on_submit():
        test.name = form.title.data
        test.discription = form.description.data
        test.part_id = form.part.data.id
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = test.name
        form.description.data = test.discription
    return render_template("update.html", title='update', form=form)


@app.route("/part/<int:id>")
def parts(id):
    test=Blog.query.filter_by(part_id=id)
    part = Part.query.all()
    return render_template('filter.html', blog_part=test, part=part)



@app.route("/show_more/<int:id_show>")
def show_more(id_show):
    test = Blog.query.get_or_404(id_show)
    return render_template('show_more.html', title="show-more", post=test)






