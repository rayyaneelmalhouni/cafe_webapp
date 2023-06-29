
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = FloatField("Coffee Price", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets", validators=[DataRequired()])
    has_wifi = BooleanField("Has Wifi", validators=[DataRequired()])
    has_toilet = BooleanField("Has Toilet", validators=[DataRequired()])
    can_take_calls = BooleanField("Can take calls", validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={'class': 'btn btn-primary'})


db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///cafes.db")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

bootstrap = Bootstrap(app)
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    map_url = db.Column(db.String, unique=True, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template('home.html', cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if request.method == "POST":
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=int(form.has_sockets.data),
            has_wifi=int(form.has_wifi.data),
            has_toilet=int(form.has_toilet.data),
            can_take_calls=int(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=f"{form.coffee_price.data}£"
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=form)





@app.route("/delete/<cafe_id>")
def delete(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
