# -*- coding: UTF-8 -*-

import datetime, uuid, random
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
import pymongo
from flask import Blueprint, render_template, render_template_string, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_paginate import Pagination
from markupsafe import escape
from wtforms.fields import *
from wtforms.validators import ValidationError
from wtforms.validators import *
from karmaModel import getHex

SHOW_N_TOP_RECORDS = 10

connect('mongodb://omctf-mongo:27017/donations')
#connect('mongodb://localhost:27017/donations')

def checkNhul(form, field):
    # nhul algo for checking number field
    num = "".join(field.data.split())
    sum = 0

    for i in range(len(num)):
        a = int(num[i])
        if (i%2 != 0):
            a *= 2
            if (a>9):
                a -= 9
        sum += a
    if (sum % 10 == 0):
        return True

    raise ValidationError(u"Неизвестный формат номера " + str(sum))

class CreditForm(FlaskForm):
    name = TextField(u"Имя владельца", [Required()])
    number = TextField(u"Номер карты", [Required(), Regexp(r'[\d]{4}[\s]*[\d]{4}[\s]*[\d]{4}[\s]*[\d]{4}[\s]*', message='Number format error (16 numbers)'), checkNhul])
    expired = TextField(u"Месяц/год",[Required(), Regexp(r'[\d]{1,2}[\/,\w][\d]{2}', message='Unknown date format')])
    ccv = IntegerField(u"CCV код",[Required()])
    value = IntegerField(u"Сумма",[Required(), NumberRange(min=0, message='Donation summ should be positive!')])
    email = TextField(u"Электронная почта (опционально)",[Optional(), Email()])
    comment = TextField(u"Комментарий (опционально)", [Optional()])

    submit = SubmitField(u"Помочь НИИ")

# models section
class CreditDonation(MongoModel):
    uid = fields.CharField(required=True)
    name = fields.CharField(required=True)
    number = fields.CharField(required=True)
    expired = fields.CharField(required=True)
    ccv = fields.CharField(required=True)
    value = fields.IntegerField(required=True)
    email = fields.EmailField(blank=True)
    comment = fields.CharField(blank=True)
    donation_date = fields.DateTimeField(required=True)

# routing section
credits = Blueprint('credits', __name__)

@credits.route('/', methods=('GET', 'POST'))
def index():

    creditForm = CreditForm()

    if request.method == 'POST' and creditForm.validate():
        uniq_id = uuid.uuid3(uuid.NAMESPACE_X500, str("".join(request.form['number'].split()) + str(request.form['name'])))

        CreditDonation(uid = uniq_id,
            name = request.form['name'],
            number = "".join(request.form['number'].split()),
            expired = request.form['expired'],
            ccv = request.form['ccv'],
            value = request.form['value'],
            email = request.form['email'],
            comment = request.form['comment'],
            donation_date = datetime.datetime.now()).save()

        flash(u"Спасибо за помощь, мистер {}! Информация о пожертвовании доступна по <a href={}>ссылке</a>!"
              .format(escape(creditForm.name.data), url_for('credits.info', id=uniq_id)))

        return redirect(url_for('credits.history'))

    qs = CreditDonation.objects.all()
    cursor = qs.aggregate(
        {'$group': {'_id': '$name',
                    'value': {'$sum': '$value'}}},
        {'$sort': {'value': pymongo.DESCENDING}},
        {'$limit' : SHOW_N_TOP_RECORDS },
        allowDiskUse=True)

    return render_template('credits.html', form=creditForm, donats=list(cursor), hval=getHex())

@credits.route('/history')
def history():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)

    total_count = CreditDonation.objects.count()
    per_page = 10

    donats = CreditDonation.objects.all().order_by([('donation_date', -1)]).skip((page-1)*per_page).limit(per_page)

    donats = list(donats)
    for d in donats:
        position = random.randint(0, 2)
        part = d.number[1+position*5:6+position*5]

        d.number = 'x'*11
        d.number = d.number[:1+position*5] + part + d.number[1+position*5:]

    pagination = Pagination(page=page, total=total_count, search=search, record_name='donations', bs_version=3)

    return render_template('history.html',
                            donats=donats,
                            pagination=pagination,
                            hval=getHex())

@credits.route('/info')
def info():

    donat_id = request.args.get('id')
    donats = CreditDonation.objects.raw({'uid':donat_id}).order_by([('donation_date', -1)])

    return render_template('info.html',
                            id=donat_id,
                            donats=list(donats),
                            hval=getHex())
