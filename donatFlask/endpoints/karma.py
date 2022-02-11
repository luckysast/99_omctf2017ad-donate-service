# -*- coding: UTF-8 -*-

import datetime
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from markupsafe import escape
from wtforms.fields import *
from wtforms.validators import ValidationError
from wtforms.validators import *
from karmaModel import KarmaDonation, getHex

connect('mongodb://omctf-mongo:27017/donations')
#connect('mongodb://localhost:27017/donations')

class KarmaForm(FlaskForm):
    value = IntegerField('', [Required()])
    submit = SubmitField('Поддержать мысленно')

karma = Blueprint('karma', __name__)

@karma.route('/', methods=('GET', 'POST'))
def index():
    karmaForm = KarmaForm()

    if request.method == 'POST' and karmaForm.validate():
        flash('Karma updated')

        karma = KarmaDonation.objects.all().order_by([('ddate', -1)]).limit(1)
        karma_val = int(request.form['value'])
        karma_val = min(100, max(-100, karma_val))

        if (karma.count() < 1):
            # empty
            KarmaDonation(value = karma_val,
            minimum = karma_val,
            maximum = karma_val,
            ddate = datetime.datetime.now()).save()
        else:
            karma = karma.first()
            karma_val += int(karma.value)
            KarmaDonation(value = karma_val,
            minimum = min(int(karma.minimum), karma_val),
            maximum = max(int(karma.maximum), karma_val),
            ddate = datetime.datetime.now()).save()

        return redirect(url_for('karma.index'))
    return render_template('karma.html', form=karmaForm, hval=getHex())
