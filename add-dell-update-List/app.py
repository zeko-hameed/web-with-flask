from flask import Flask, render_template, redirect, url_for, request
from form import Do_list, update_list
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from models import listtable



app = Flask(__name__)
app.config["SECRET_KEY"] = 'e053ce5bc93a6c14c4542e430caf9a9f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/Do-list-db'
db = SQLAlchemy(app)


class listtable(db.Model):
    __tablename__ = 'dolist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    descrption = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)





@app.route("/")
def show_list():
    show = listtable.query.all()
    return render_template("show_list.html", title="show-list", show=show)



@app.route("/add_list", methods=['GET', 'POST'])
def add_list():
    form = Do_list()
    if form.validate_on_submit():
        add_list_to_db = listtable(title=form.title.data, descrption=form.descrption.data)
        db.session.add(add_list_to_db)
        db.session.commit()
        return redirect(url_for('show_list'))
    return render_template("add_list.html", title="add-list", form=form)


@app.route("/updata/<int:id_list>", methods=['GET', 'POST'])
def update(id_list):
    test = listtable.query.get_or_404(id_list)

    form = update_list()
    if form.validate_on_submit():
        test.title = form.title.data
        test.descrption = form.descrption.data

        db.session.commit()
        return redirect(url_for('show_list'))
    elif request.method == 'GET':
        form.title.data = test.title
        form.descrption.data = test.descrption
    return render_template("update_list.html", title="update-list", form=form)


@app.route("/delete/<int:id_list>", methods=['GET', 'POST'])
def delete(id_list):
    test = listtable.query.get_or_404(id_list)

    db.session.delete(test)
    db.session.commit()
    return redirect(url_for('show_list'))



if __name__ == "__main__":
    app.run(debug=True)
