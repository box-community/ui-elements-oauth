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

    return render_template('home/index.html', segment='index',avatar_url=current_user.avatar_url)

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


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
