""" read from a SQLite database and return data """

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask import request
from wtforms.validators import DataRequired

app = Flask(__name__)

application = app

# the name of the database; add path if necessary
db_name = 'un_data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Nation(db.Model):
    __tablename__ = 'united_nations'
    country = db.Column(db.String)
    source = db.Column(db.String)
    unit = db.Column(db.String)
    value = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)

class Goods(db.Model):
    __tablename__ = 'listofgoods'
    country = db.Column(db.String)
    industry = db.Column(db.String)
    goods = db.Column(db.String)
    alternative = db.Column(db.String)
    retailer = db.Column(db.String)
    social = db.Column(db.String)
    social_link = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)


nations = Nation.query.order_by(Nation.country).all()
good = Goods.query.order_by(Goods.country).all()

pairs_list = []
for nation in nations:
    pairs_list.append(( nation.id, nation.country ))

goods_list = []
for goods in good:
    goods_list.append(( goods.id, goods.country ))

class Form(FlaskForm):
    country = SelectField('Choose a country:', choices=pairs_list)
    submit = SubmitField('Submit')

#routes
@app.route('/')
def index():
    form=Form()
    return render_template('index.html', form=form)


@app.route('/country', methods=['GET', 'POST'])
def country_detail():
    try:
        country = request.form['country']
        n = Nation.query.filter_by(id=country).first()
        g = Goods.query.filter_by(id=country).first()
        return render_template('nation.html', n=n, g=g)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


if __name__ == '__main__':
    app.run(debug=True)
