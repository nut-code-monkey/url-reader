#!/usr/bin/env python

import os
from flask import Flask, render_template, redirect
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import html2text

app = Flask("url-reader")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class URLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Read')

@app.route('/')
def homepage():
    form = URLForm()
    return render_template('main.html', form=form)

@app.route('/',  methods=['POST'])
def url_handler():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('main.html', form=form)

    try:
        f = requests.get(form.url.data)
    except requests.exceptions.MissingSchema as e:
        return e
    except requests.exceptions.ConnectionError as e:
        return e

    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(f.text)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)