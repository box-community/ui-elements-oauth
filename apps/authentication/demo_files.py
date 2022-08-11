

import os
from boxsdk import BoxAPIException
from apps.config import Config
from flask_login import current_user
from apps.authentication.box_oauth import box_client
from apps import db

from apps.authentication.models import Users

def user_check_demo_folder():
	"""	Check if the user referenced demo folder exists, 
		if not creates it 
		Returns a folder id
	"""
	user = Users.query.filter_by(id=current_user.id).first()
	demo_folder_id = user.box_demo_folder_id

	if demo_folder_id is None:
		# the user has no reference to a demo folder
		# lets check if it already exists in Box
		# this is an edge case when a user has multiple
		# logins in this app but a sigle
		# box account
		demo_folder_id = check_demo_folder()
		# Does the demo folder already exists?
		if demo_folder_id is None:
			demo_folder_id = create_demo_folder()
			update_demo_folder(demo_folder_id)
		else:
			# the folder exists in Box
			# but this app user has no reference to it
			update_demo_folder(demo_folder_id)
		return demo_folder_id

	# does folder referenced actually exist in Box?	
	if not check_folder_by_id(demo_folder_id):
		demo_folder_id = create_demo_folder()
		update_demo_folder(demo_folder_id)

	return demo_folder_id

def create_demo_folder():
	client = box_client()
	demo_folder_id = client.folder(0).create_subfolder(Config.DEMO_FOLDER_NAME).id
	return demo_folder_id

def update_demo_folder(demo_folder_id:str):
	user = Users.query.filter_by(id=current_user.id).first()
	user.box_demo_folder_id = demo_folder_id
	db.session.commit()
	

def check_folder_by_id(folder_id:str)->bool:
	"""	Check if the folder exists in Box
		returns True if folder exists
	"""
	client = box_client()
	try:
		folder = client.folder(folder_id).get()
	except BoxAPIException:
		return False
	return True	# folder exists

def check_demo_folder():
	"""	Check if the standard demo folder exists in Box
		by name on the root folder
	"""
	client = box_client()

	# check if folder exists in root
	# ? exact match on folder name (string between quotes) ?
	search_results = client.search().query(
		'"'+Config.DEMO_FOLDER_NAME+'"', 
		type = 'folder'	,
		ancestor_folder_ids = [0],
		content_types = ['name']
	)

	for item in search_results:
		if item.name == Config.DEMO_FOLDER_NAME:
			return item.id

	return None

def demo_folder_id_get():
	user = Users.query.filter_by(id=current_user.id).first()
	return user.box_demo_folder_id


def demo_file_ids_get()->list:
	
	user = Users.query.filter_by(id=current_user.id).first()
	file_list = []
	client = box_client()
	
	try:
		files = client.folder(user.box_demo_folder_id).get_items()
		for file in files:
			file_list.append(file.id)

	except BoxAPIException:
		# no files exist in demo folder
		pass
	
	return file_list



def upload_demo_files():

	demo_folder_id = user_check_demo_folder()
	client = box_client()
	demo_folder = client.folder(demo_folder_id).get()
	
	path = Config.basedir+"/"+Config.ASSETS_ROOT+'/demo_files/'
	files = os.listdir(path)

	for file in files:
		print(os.path.join(path,file))
		try:
			demo_folder.upload(os.path.join(path,file))
		except BoxAPIException as error:
			pass