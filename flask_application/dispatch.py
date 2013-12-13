#!/usr/bin/env python

""" dispatch.py - This is where the app launches from"""

# Flask
from flask import Flask, jsonify
app = Flask(__name__)

import pusher

@app.route('/')
def index():
    return '<iframe width="420" height="315" src="//www.youtube.com/embed/IwBS6QGsH_4" frameborder="0" allowfullscreen></iframe>'


@app.errorhandler(404)
def handler404(e=None):
    return '<iframe width="420" height="315" src="//www.youtube.com/embed/otCpCn0l4Wo" frameborder="0" allowfullscreen></iframe>'

@app.route('/newcommit')
def newcommit():
    result = pusher.pushToPivotal({})

    resp = jsonify({"success": result})
    resp.status_code = 200

    return resp