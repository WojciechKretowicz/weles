import sys
import requests
import pickle
import os
import pandas as pd
import platform
import re
from io import StringIO

def upload(model, model_name, requirements_file, train_dataset, train_dataset_name, test_dataset = None, test_dataset_name = None):
	"""
	Function uploads model, the training set and optionally test_dataset to the base.

	model - model object or path to model pickle
	model_name - name of the model, string
	requirements_file - python style requirements, can be easily obtained by running: "pip freeze > requirements.txt" at your command line
	train_dataset - matrix or path to csv file (must contain '/') or hash of already uploaded data, structure X|Y is required
	test_dataset - optional argument, matrix or path to csv file (must contain '/') or hash of already uploaded data, structure X|Y is required
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

	# flag if test_dataset was provided
	if test_dataset is None:
		info['is_test_dataset'] = 0
		info['test_data_name'] = '0'
	else:
		info['is_test_dataset'] = 1
		info['test_data_name'] = test_dataset_name

	# init of flag if train_dataset is a hash
	info['train_dataset_hash'] = 0

	# init of flags what temporary file should be removed at the end of function
	del_model = False
	del_train_data = False
	del_test_data = False

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

	# creating regexp to findout if the train_dataset and test_dataset are paths or ids 
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

	# uploading train_dataset
	if test_dataset is None:
		# case when test_dataset is not provided

		info['is_test_dataset'] = 0
		info['test_dataset_hash'] = 0

	elif type(test_dataset) == str and reg.search(test_dataset) is None:
		# case when test_dataset is a hash of already uploaded dataset

		info['test_dataset_hash'] = test_dataset
		info['is_test_dataset'] = 1

	elif type(test_dataset) == str:
		# case when test_dataset is a path to csv file

		files['test_dataset'] = open(test_dataset, 'rb')
		info['is_test_dataset'] = 1
	else:
		# case when test_dataset is a matrix

		# convertion to pandas data frame
		test_dataset = pd.DataFrame(test_dataset)

		# creating temporary file
		test_dataset.to_csv('./tmp_test_data_csv')

		# uploading dataset
		files['test_dataset'] = open('./tmp_test_data_csv', 'rb')

		# setting flag
		del_test_data = True

	# uploading requirements file
	files['requirements'] = open(requirements_file, 'rb')

	# setting session info flag
	info['is_sessionInfo'] = 0

	# creating request
	r = requests.post(url, files = files, data = info)

	# removing temporary files
	if del_model:
		os.remove('.tmp_model.pkl')
	if del_train_data:
		os.remove('./tmp_train_data_csv')
	if del_test_data:
		os.remove('./tmp_test_data_csv')

def predict(model_name, X, pred_type = 'exact'):
	"""
	Function uses model in the database to make a prediction on X.

	model_name - name of the model in the database
	X - numpy array or path to csv file (must containt '/') or hash of already uploaded dataset
	pred_type - type of the prediction: exact/prob
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
