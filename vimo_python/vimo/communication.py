import sys
import requests
import pickle
import os
import pandas as pd
import platform
import re
from io import StringIO

def upload(model, model_name, requirements_file, train_dataset, train_dataset_name, model_desc, dataset_desc, user_name, password):
	"""
	Function uploads model, the training set.

	model - model object or path to model pickle
	model_name - name of the model, string
	requirements_file - python style requirements, can be easily obtained by running: "pip freeze > requirements.txt" at your command line
	train_dataset - matrix or path to csv file (must contain '/') or hash of already uploaded data, structure X|Y is required
	"""

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
		with open('.tmp_model.pkl', 'wb') as fd:
			pickle.dump(model, fd)

		# uploading model
		files = {'model': open('.tmp_model.pkl', 'rb')}

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
		train_dataset.to_csv('./tmp_train_data_csv', index = False)

		# uploading dataset
		files['train_dataset'] = open('./tmp_train_data_csv', 'rb')

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

	# creating request
	r = requests.post(url, files = files, data = info)

	# removing temporary files
	if del_model:
		os.remove('.tmp_model.pkl')
	if del_train_data:
		os.remove('./tmp_train_data_csv')

def predict(model_name, X, pred_type = 'exact', prepare_columns = True):
	"""
	Function uses model in the database to make a prediction on X.

	model_name - name of the model in the database
	X - numpy array or path to csv file (must containt '/') or hash of already uploaded dataset
	pred_type - type of the prediction: exact/prob
	prepare_columns - if true and if X is an object then take exact columns from model in database
	"""

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
		X.to_csv('./tmp_data_csv-' + model_name, index = False)

		info = {'is_hash': 0}
		files = {'data': open('./tmp_data_csv-' + model_name, 'rb')}

		# request
		r = requests.get(url, files=files, data = info)

		# removing temporary file
		os.remove('./tmp_data_csv-' + model_name)

	return pd.read_csv(StringIO(r.text), header=None)

def model_info(model_name):
	r = requests.get('http://192.168.137.64/models/' + model_name + '/info')
	return r.json()

def create_user(user_name, password, mail):
	requests.post('http://192.168.137.64/users/create_user', data = {'user_name': user_name, 'password': password, 'mail': mail})
