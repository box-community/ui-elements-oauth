# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from apps.home import blueprint
from flask import render_template, request
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from apps.authentication.box_oauth import access_token_get
from apps.home.explorer import explorer
from apps.home.previewer import previewer
from apps.home.picker import picker
from apps.home.uploader import uploader


@blueprint.route('/index')
@login_required
def index():
    return explorer(token=access_token_get())
    # return render_template('home/index.html', segment='index',avatar_url=current_user.avatar_url)

@blueprint.route('/event/', methods=['POST'])
def event():
    request_data = request.get_json()
    print('***********************************************************')
    print(request_data)
    print('***********************************************************')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@blueprint.route('/explorer')
@login_required
def page_explorer():

    return explorer(token=access_token_get())    

@blueprint.route('/uploader')
@login_required
def page_uploader():

    return uploader(token=access_token_get())       

@blueprint.route('/previewer')
@login_required
def page_previewer():

    return previewer(token=access_token_get())   

@blueprint.route('/picker')
@login_required
def page_picker():

    return picker(token=access_token_get())   

