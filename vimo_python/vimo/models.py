import sys
import requests
import pickle
import os
import pandas as pd
import platform
import re
from io import StringIO
from datetime import datetime

def upload(model, model_name, model_desc, target, tags, train_dataset, train_dataset_name, dataset_desc, requirements_file, user_name, password):
	"""Function uploads scikit-learn model, the training set and all needed metadata to the vimo base.

	Parameters
	----------
	model : scikit-learn model or string
		model object or path to the model pickle
	model_name : string
		name of the model that will be visible in the vimo
	model_desc : string
		description of the model
	tags : list
		list of tags
	train_dataset : array-like or string
		array-like or path to csv file (must contain '/') or hash of already uploaded data, structure X|Y is required
	train_datset_name : string
		name of the dataset that will be visible in the vimo
	dataset_desc : string
		description of the dataset
	requirements_file : string
		path to python style requirements file, can be easily obtained by running: "pip freeze > requirements.txt" at your command line
	user_name : string
		your user name
	password : string 
		your password

	Returns
	-------
	string
		Returns an information if uploading the model was successful.
	"""

	timestamp = str(datetime.now().timestamp())

	if re.search('^[a-z0-9A-Z_]+$', model_name) is None:
		return "Your model name contains non alphanumerical signs."

	# url to post
	url = 'http://192.168.137.64/models/post'

	# collecting system info
	if platform.system() == 'Linux':
		info = {'system': platform.system(),
			'system_release': platform.release(),
			'distribution': platform.linux_distribution()[0],
			'distribution_version': platform.linux_distribution()[1],
			'language': 'python',
			'language_version': platform.python_version(),
			'architecture': platform.architecture()[0],
			'processor': platform.machine()}

	info['model_name'] = model_name
	info['train_data_name'] = train_dataset_name

	info['target'] = target


	# init of flag if train_dataset is a hash
	info['train_dataset_hash'] = 0

	# init of flags what temporary file should be removed at the end of function
	del_model = False
	del_train_data = False

	# uploading model
	if type(model) == str:
		# case when model is a path
		files = {'model': open(model, 'rb')}
	else:
		# case when model is an object

		# creating temporary file
		with open('.tmp_model_' + timestamp +'.pkl', 'wb') as fd:
			pickle.dump(model, fd)

		# uploading model
		files = {'model': open('.tmp_model_' + timestamp + '.pkl', 'rb')}

		# setting flag
		del_model = True

	# creating regexp to findout if the train_dataset is a path or id
	reg = re.compile("/")

	# uploading train dataset
	if type(train_dataset) == str and reg.search(train_dataset) is None:
		# case when train_dataset is a hash of already uploaded dataset

		info['train_dataset_hash'] = train_dataset

	elif type(train_dataset) == str:
		# case when train_dataset is a path to dataset

		files['train_dataset'] = open(train_dataset, 'rb')

	else:
		# case when train_dataset is a matrix

		# conversion to pandas data frame
		train_dataset = pd.DataFrame(train_dataset)

		# creating temporary file
		train_dataset.to_csv('.tmp_train_data_' + timestamp + '.csv', index = False)

		# uploading dataset
		files['train_dataset'] = open('.tmp_train_data_' + timestamp + '.csv', 'rb')

		# setting flag
		del_train_data = True

	if type(model_desc) == str and reg.search(model_desc) is not None:
		info['model_desc'] = open(model, 'rb').read()
	elif type(model_desc) == str:
		info['model_desc'] = model_desc

	if type(dataset_desc) == str and reg.search(dataset_desc) is not None:
		info['dataset_desc'] = open(model, 'rb').read()
	elif type(dataset_desc) == str:
		info['dataset_desc'] = dataset_desc

	# uploading requirements file
	files['requirements'] = open(requirements_file, 'rb')

	# setting session info flag
	info['is_sessionInfo'] = 0

	# user_name
	info['user_name'] = user_name

	# password
	info['password'] = password

	# tags
	info['tags'] = tags

	# creating request
	r = requests.post(url, files = files, data = info)

	# removing temporary files
	if del_model:
		os.remove('.tmp_model_' + timestamp + '.pkl')
	if del_train_data:
		os.remove('.tmp_train_data_' + timestamp + '.csv')

	return r.text

def predict(model_name, X, pred_type = 'exact', prepare_columns = True):
	"""
	Function uses model in the database to make a prediction on X.

	Parameters
	----------
	model_name : string
		name of the model in the base that you want to use
	X : array-like/string
		array-like or path to csv file (must containt '/') or hash of already uploaded dataset,
		must have column names if prepare_columns is set to False
	pred_type : string
		type of the prediction: exact/prob
	prepare_columns : boolean
		if true and if X is an object then take column names from model in the database

	Returns
	-------
	array-like
		Returns a pandas data frame with made predictions.
	"""

	timestamp = str(datetime.now().timestamp())

	# url
	url = 'http://192.168.137.64/models/' + model_name + '/predict/' + pred_type

	# regexp to find out if X is a path
	reg = re.compile("/")

	# uploading data
	if type(X) == str and reg.search(X) is None:
		# case when X is a hash
		info = {'is_hash': 1}
		info['hash'] = X

		# request
		r = requests.get(url, data = info)
	elif type(X) == str:
		# case when X is a path

		info = {'is_hash': 0}
		files = {'data': open(X, 'rb')}

		# request
		r = requests.get(url, files=files, data=info)
	else:
		# case when X is an object

		# conversion to pandas data frame
		X = pd.DataFrame(X)

		if prepare_columns:
			columns = model_info(model_name)['data_info']['columns']
			c = []
			for col in columns:
				c.append(col[1])
			c = c[0:-1]
			X.columns = c

		# creating temporary file
		X.to_csv('.tmp_data_' + timestamp + '.csv', index = False)

		info = {'is_hash': 0}
		files = {'data': open('.tmp_data_' + timestamp + '.csv', 'rb')}

		# request
		r = requests.get(url, files=files, data = info)

		# removing temporary file
		os.remove('.tmp_data_' + timestamp + '.csv')

	return pd.read_csv(StringIO(r.text), header=None)

def model_info(model_name):
	"""
	Function model_ino

	...::: DESCRIPTION :::...
	Take all metadata about the model from vimo. It will return a dict.

	...::: PARAMS :::...
	model_name - name of the model in the vimo base

	...::: RETURN :::...
	Dict with fields:
		model_info
		data_info
	"""
	r = requests.get('http://192.168.137.64/models/' + model_name + '/info')
	return r.json()

def search_model(row=None, column=None, missing=None, classes=None, owner=None, tags=None, regex=None):
	"""
	Search vimo base for models with specific tags. If all parameters are set to None, then returns all models' name in vimo.

	Params
	------
	row : string
		string describing how many rows should have training dataset
		examples:
			row = '<101;'; row = '>120;'; row = '>100;<200;'
	column : string
		string describing how many columns should have training dataset
		examples:
			column = '<101;'; column = '>120;'; column = '>100;<200;'
	missing : string
		string descibing how many missing values should have training dataset
		examples:
			missing = '=0;'; missing = '>120;'; missing = '<10001;'; missing = '>100;<200;'
	classes : string
		string descibing how many classes should have training dataset
		examples:
			classes = '=2;'; classes = '<3;'; classes = '>2;'; classes = '>2;<11;'
	owner : string
		owner's user name
	tags : list
		list of tags, all should be strings
	regex : string
		regex for models' names

	Returns
	-------
	list
		Returns a list of models' names that have at least one common tag with that provided in parameter 'tags'
	"""
	data = {'row': row, 'column': column, 'missing': missing, 'classes': classes, 'owner': owner, 'tags': tags, 'regex': regex}
	r = requests.get('http://192.168.137.64/models/search', data=data)
	return r.json()['models']

def audit_model(model_name, measure, user, password, data, target, data_name=None, data_desc=None):
	"""TODO"""

	info = {'model_name': model_name, 'measure': measure, 'user': user, 'password': password, 'target': target}

	timestamp = str(datetime.now().timestamp())
	del_data = False

	# regexp to find out if data is a path
	reg = re.compile("/")


	# uploading data
	if type(data) == str and reg.search(data) is None:
		# case when data is a hash
		info['is_hash'] = 1
		info['hash'] = data

		r = requests.post('http://192.168.137.64/models/audit', data=info)
	elif type(data) == str:
		# case when data is a path
		files = {'data': open(data, 'rb')}
		info['is_hash'] = 0
		info['data_name'] = data_name
		info['data_desc'] = data_desc

		r = requests.post('http://192.168.137.64/models/audit', files=files, data=info)
	else:
		# case when data is an object

		info['is_hash'] = 0
		info['data_name'] = data_name
		info['data_desc'] = data_desc

		# conversion to pandas data frame
		data = pd.DataFrame(data)

		# creating temporary file
		data.to_csv('.tmp_data_' + timestamp + '.csv', index = False)

		files = {'data': open('.tmp_data_' + timestamp + '.csv', 'rb')}

		del_data = True

		r = requests.post('http://192.168.137.64/models/audit', files=files, data=info)

	if del_data:
		os.remove('.tmp_data_' + timestamp + '.csv')

	return r.text
