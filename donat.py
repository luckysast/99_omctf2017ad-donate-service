#!/usr/bin/python
# -*- coding: UTF-8 -*-

from donatFlask import create_app
from flask import request, render_template_string

# create an app instance
app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    template = '''{%% extends "base.html" %%}
{%% block body %%}
    <div class="center-content error">
        <h2>Oops! That page doesn't exist.</h2>
        <h3>%s</h3>
    </div>
{%% endblock %%}
''' % (request.url)
    return render_template_string(template), 404

app.run(host="0.0.0.0",port=31415 ,debug=True)
