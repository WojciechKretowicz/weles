"""@package docstring
The module related to models in the **weles**
"""


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
	"""Function uploads scikit-learn or keras model, the training set and all needed metadata to the **weles** base.

	Parameters
	----------
	model : scikit-learn or keras model or string
		model object or path to the model pickle
	model_name : string
		name of the model that will be visible in the **weles**
	model_desc : string
		description of the model
	tags : list
		list of tags
	train_dataset : array-like or string
		array-like or path to csv file (must contain '/') or hash of already uploaded data, structure X|Y is required
	train_dataset_name : string
		name of the dataset that will be visible in the **weles**
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

	if not isinstance(model_name, str):
		raise ValueError("model_name must be a string")
	if not isinstance(model_desc, str):
		raise ValueError("model_desc must be a string")
	if not isinstance(target, str):
		raise ValueError("target must be a string")
	if not isinstance(tags, list):
		raise ValueError("tags must be a list")
	if not isinstance(train_dataset, (str, pd.DataFrame)):
		raise ValueError("train_dataset must be a string or pandas data frame")
	if not isinstance(train_dataset_name, str):
		raise ValueError("train_dataset_name must be a string")
	if not isinstance(dataset_desc, str):
		raise ValueError("dataset_desc must be a string")
	if not isinstance(requirements_file, str):
		raise ValueError("requirements_file must be a string")
	if not isinstance(user_name, str):
		raise ValueError("user_name must be a string")
	if not isinstance(password, str):
		raise ValueError("password must be a string")

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

	if not isinstance(model_name, str):
		raise ValueError("model_name must be a string")
	if not isinstance(X, (str, pd.DataFrame)):
		raise ValueError("X must be a string or pandas.DataFrame")
	if not isinstance(pred_type, str):
		raise ValueError("pred_type must be a string")
	if not isinstance(prepare_columns, bool):
		raise ValueError("prepare_columns must be a bool")

	timestamp = str(datetime.now().timestamp())

	# url
	url = 'http://192.168.137.64/models/' + model_name + '/predict/' + pred_type

	# regexp to find out if X is a path
	reg = re.compile("/")

	# uploading data
	if type(X) == str and reg.search(X) is None:
		# case when X is a hash
		body = {'is_hash': 1}
		body['hash'] = X

		# request
		r = requests.get(url, data = body)
	elif type(X) == str:
		# case when X is a path

		body = {'is_hash': 0}
		files = {'data': open(X, 'rb')}

		# request
		r = requests.get(url, files=files, data=body)
	else:
		# case when X is an object

		# conversion to pandas data frame
		X = pd.DataFrame(X)

		if prepare_columns:
			model_info = info(model_name)
			columns = model_info['columns']
			target = model_info['model']['target']
			columns = columns.sort_values('id')
			columns = columns.loc[columns['name'] != target, 'name']
			X.columns = columns

		# creating temporary file
		X.to_csv('.tmp_data_' + timestamp + '.csv', index = False)

		body = {'is_hash': 0}
		files = {'data': open('.tmp_data_' + timestamp + '.csv', 'rb')}

		# request
		r = requests.get(url, files=files, data = body)

		# removing temporary file
		os.remove('.tmp_data_' + timestamp + '.csv')

	return pd.read_csv(StringIO(r.text), header=None)

def info(model_name):
	"""
	Get the information about model.

	Parameters
	----------
	model_name : string
		name of the model in the **weles** base

	Returns
	-------
	dict
		dictionary with fields: model, data, columns and audits containing all metadata about the model
	"""

	if not isinstance(model_name, str):
		raise ValueError("model_name must be a string")

	r = requests.get('http://192.168.137.64/models/' + model_name + '/info')
	r = r.json()
	r['audits'] = pd.DataFrame(r['audits'])
	r['columns'] = pd.DataFrame(r['columns'])

	return r

def search(language=None, language_version=None, row=None, column=None, missing=None, classes=None, owner=None, tags=None, regex=None):
	"""
	Search **weles** base for models with specific restrictions. If all parameters are set to None, then returns all models' name in **weles**.

	Parameters
	------
	language : string
		search only for models written in given language
	language_version : string
		string describing what version of language are in you interest
		examples:
			language_version = '>3.5.0;', language_version = '=3.6.0;', lanugage_version = '>3.3.3;<3.6.6;'
	row : string
		string describing how many rows should have training dataset
		examples:
			row = '<101;', row = '>120;', row = '>100;<200;', row = '=2222;'
	column : string
		string describing how many columns should have training dataset
		examples:
			column = '<101;', column = '>120;', column = '>100;<200;', column = '=22;'
	missing : string
		string descibing how many missing values should have training dataset
		examples:
			missing = '=0;', missing = '>120;', missing = '<10001;', missing = '>100;<200;'
	classes : string
		string descibing how many classes should have training dataset
		examples:
			classes = '=2;', classes = '<3;', classes = '>2;', classes = '>2;<11;'
	owner : string
		owner's user name
	tags : list
		list of tags, all should be strings
	regex : string
		regex for models' names

	Returns
	-------
	list
		Returns a list of models' names that satisfies given restrictions
	"""

	if language is not None and not isinstance(language, str):
		raise ValueError("language must be a string")
	if language_version is not None and not isinstance(language_version, str):
		raise ValueError("language_version must be a string")
	if row is not None and not isinstance(row, str):
		raise ValueError("row must be a string")
	if column is not None and not isinstance(column, str):
		raise ValueError("column must be a string")
	if missing is not None and not isinstance(missing, str):
		raise ValueError("missing must be a string")
	if classes is not None and not isinstance(classes, str):
		raise ValueError("classes must be a string")
	if owner is not None and not isinstance(owner, str):
		raise ValueError("owner must be a string")
	if tags is not None and not isinstance(tags, list):
		raise ValueError("tags must be a list")
	if regex is not None and not isinstance(regex, str):
		raise ValueError("regex must be a string")

	data = {'language': language, 'language_version': language_version, 'row': row, 'column': column, 'missing': missing, 'classes': classes, 'owner': owner, 'tags': tags, 'regex': regex}
	r = requests.get('http://192.168.137.64/models/search', data=data)
	return r.json()['models']

def audit(model_name, measure, user, password, data, target, data_name=None, data_desc=None):
	"""Audit the model

	Parameters
	----------
	model_name : string
		name of the model in the **weles** base to make an audit of
	measure : string
		name of the measure used on model, must be one of supported
	user : string
		your user name
	password : string
		your password
	data : array-like/string
		data frame to make an audit on or hash of already uploaded data in the **weles** or path to the dataset
	target : string
		name of the column in the dataset that should be used as the target
	data_name : string
		optional, name of the dataset that will be visible in the **weles**, unnecessary if data is a hash
	data_desc : string
		optional, description of the dataset, unnecessary if data is a hash

	Returns
	-------
	string/float
		return the result of the audit or information if something went wrong
	"""

	if not isinstance(model_name, str):
		raise ValueError("model_name must be a string")
	if not isinstance(measure, str):
		raise ValueError("measure must be a string")
	if not isinstance(user, str):
		raise ValueError("user must be a string")
	if not isinstance(password, str):
		raise ValueError("password must be a string")
	if not isinstance(data, (pd.DataFrame, str)):
		raise ValueError("data must be a string or pd.DataFrame")
	if not isinstance(target, str):
		raise ValueError("target must be a string")
	if data_name is not None and not isinstance(data_name, str):
		raise ValueError("data_name must be a str")
	if data_desc is not None and not isinstance(data_desc, str):
		raise ValueError("data_name must be a str")

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

	return pd.read_csv(StringIO(r.text), header=None)

def requirements(model):
	"""Get the list of package requirements

	Parameters
	----------
	model : string
		name of the model

	Returns
	-------
	dict
		listed requirements
	"""

	if not isinstance(model, str):
		raise ValueError("model must be a string")

	r = requests.get('http://192.168.137.64/models/' + model + '/requirements')
	return r.json()
