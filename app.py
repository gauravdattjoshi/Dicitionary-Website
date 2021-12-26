import os

from flask import Flask, app, render_template, request
import requests
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key


class MyForm(FlaskForm):
    name = StringField(label='', validators=[DataRequired()], render_kw={"placeholder": "Enter the word"})


def get_data(word):
    header = {'authorization': os.environ.get('token'), 'Accept-Language': 'en-IN,en-US,en-GB;', }
    print(os.environ.get('token'))
    base_url = f'https://owlbot.info/api/v4/dictionary/{word}'
    data = requests.get(base_url, headers=header)
    print(data)
    print(data.json())
    return data.json()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()

    if form.validate_on_submit():
        print(form.name.data)
        word = form.name.data.strip()
        data = get_data(word=word)
        return render_template('index.html', data=data, form=form)

    return render_template('index.html', data='', form=form)


if __name__ == '__main__':
    app.run()
