# -*- coding: UTF-8 -*-

#   $ flask --app=sample_app dev
# Afterwards, point your browser to http://localhost:5000, then check out the
# source.

from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask.ext.pymongo import PyMongo

from flask_nav import register_renderer
from .nav import nav, CustomRenderer

from endpoints.common import donation
from endpoints.credits import credits
from endpoints.karma import karma

# register common navigation bar for this app
def register_navbar():
    nav.register_element('base_navbar', Navbar(
    Link(u"НИИ Ракетостроения", '/donation/'),
    Link(u"Новости", '/newz/'),
    Subgroup(
        u"Донат",
        Separator(),
        View(u"MARSterCard", 'credits.index'),
        View(u"Последние", 'credits.history'),
        Separator(),
        View(u"Карма", 'karma.index'),
        ),
    Link(u"Проекты V.I.T.I.", '/viti/'),
    Link(u"Тендер", '/tender/'),
    Link(u"Вакансии", '/careers/')
    ))

# create app, register all blueprints, run app
def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)

    # connect to mongo db
    mongo = PyMongo(app)

    # Install our Bootstrap extension
    Bootstrap(app)

    # Our application uses blueprints as well; these go well with the
    # application factory. We already imported the blueprint, now we just need
    # to register it:
    app.register_blueprint(donation, url_prefix="/donation")
    app.register_blueprint(credits, url_prefix="/donation/credits")
    app.register_blueprint(karma, url_prefix="/donation/karma")

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.jinja_env.autoescape = False

    # We initialize the navigation as well
    register_navbar()
    # register renderer for wide common styles
    register_renderer(app, 'base_front', CustomRenderer)

    nav.init_app(app)

    return app
