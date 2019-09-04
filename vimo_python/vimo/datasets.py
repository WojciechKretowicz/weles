import sys
import requests
import pickle
import os
import pandas as pd
import platform
import re
from io import StringIO
from datetime import datetime

def upload_data(data, data_name, data_desc, user_name, password):
	"""Upload data to vimo.

	Parameters
	----------
	data : array-like/string
		data to upload or path to this data
	data_name : string
		name of the dataset that will be visible in the vimo base
	data_desc : string
		desciprtion of the data
	user_name : string
		your user name
	password : string
		your password

	Returns
	-------
	string
		information if uploading data was successful
	"""

	# url to post
	url = 'http://192.168.137.64/datasets/post'

	# timestamp for temporary files
	timestamp = str(datetime.now().timestamp())

	# uploading data
	info = {'user_name': user_name, 'password': password, 'data_name': data_name, 'data_desc': data_desc}
	if type(data) == str:
		# case when data is a path

		files = {'data': open(data, 'rb')}

		# request
		r = requests.post(url, files=files, data=info)
	else:
		# case when data is an object

		# conversion to pandas data frame
		data = pd.DataFrame(data)

		# creating temporary file
		data.to_csv('.tmp_data_' + timestamp + '.csv', index = False)

		files = {'data': open('.tmp_data_' + timestamp + '.csv', 'rb')}

		# request
		r = requests.post(url, files=files, data = info)

		# removing temporary file
		os.remove('.tmp_data_' + timestamp + '.csv')

	return r.text

def head_data(dataset_id, n=5):
	"""View the head of the dataset.

	Parameters
	----------
	dataset_id : string
		hash of the dataset
	n : int
		number of rows to show

	Returns
	-------
	pandas.DataFrame
		pandas DataFrame with top n rows
	"""

	r = requests.get('http://192.168.137.64/datasets/' + dataset_id + '/head', data = {'n': n})
	return pd.DataFrame(r.json())

def get_data(dataset_id):
	"""Get dataset from the vimo as dataframe.

	Parameters
	----------
	dataset_id : string
		hash of the dataset

	Returns
	-------
	pandas.DataFrame
		pandas Data Frame containing the requested dataset
	"""

	r = requests.get('http://192.168.137.64/datasets/' + dataset_id)
	return pd.DataFrame(r.json())

def data_info(dataset_id):
	"""Get all metadata about dataset

	Parameters
	----------
	dataset_id : string
		hash of the dataset

	Returns
	-------
	dict
		dictionary contating all metadata about the dataset
	"""

	r = request.get('http://192.168.137.64/datasets/' + dataset_id + '/info')
	return r.json()
