# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, request

donation = Blueprint('donation', __name__)

@donation.route('/')
def index():
    return redirect(url_for('credits.index'))
