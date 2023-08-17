# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json

from apps.authentication.demo_files import demo_file_ids_get, demo_folder_id_get, user_check_demo_folder
from apps.home import blueprint
from flask import flash, request
from flask_login import login_required
from apps.authentication.box_oauth import downscoped_access_token_get
from apps.home.explorer import explorer
from apps.home.previewer import previewer
from apps.home.picker import picker
from apps.home.uploader import uploader


@blueprint.route("/index")
@login_required
def index():
    return explorer(token=downscoped_access_token_get())


@blueprint.route("/event/", methods=["POST"])
def event():
    request_data = request.get_json()
    print("***********************************************************")
    print(request_data)
    print("***********************************************************")
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@blueprint.route("/explorer")
@login_required
def page_explorer():
    return explorer(token=downscoped_access_token_get())


@blueprint.route("/uploader")
@login_required
def page_uploader():
    folder_id = user_check_demo_folder()
    if folder_id == 0:
        flash(
            "No demo folder found. All uploads will end up in the root folder. Go to settings and initialize the demo",
            "alert-warning",
        )
    return uploader(token=downscoped_access_token_get(), folder_id=folder_id)


@blueprint.route("/previewer")
@login_required
def page_previewer():
    file_list = demo_file_ids_get()
    if not file_list:
        flash("No files found in the demo folder. Go to settings and initialize the demo", "alert-warning")
    return previewer(token=downscoped_access_token_get(), file_list=file_list)


@blueprint.route("/picker")
@login_required
def page_picker():
    return picker(token=downscoped_access_token_get())
