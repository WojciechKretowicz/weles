"""@package docstring
The module with functions related to datasets in the **weles**
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

def upload(data, data_name, data_desc, user_name, password):
	"""Upload data to **weles**.

	Parameters
	----------
	data : array-like/string
		data to upload or path to this data
	data_name : string
		name of the dataset that will be visible in the **weles** base
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

	if not isinstance(data, (str, pd.DataFrame)):
		raise ValueError("data must be a string or a data frame")
	if not isinstance(data_name, str):
		raise ValueError("data_name must be a string")
	if not isinstance(data_desc, str):
		raise ValueError("data_desc must be a string")
	if not isinstance(user_name, str):
		raise ValueError("user_name must be a string")
	if not isinstance(password):
		raise ValueError("password must be a string")

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

def head(dataset_id, n=5):
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

	if not isinstance(dataset_id, str):
		raise ValueError("dataset_id must be a string")
	if not len(dataset_id) == 64:
		raise ValueError("dataset_id must be 64 character long")
	if not isinstance(n, int):
		raise ValueError("n must be an integer")

	r = requests.get('http://192.168.137.64/datasets/' + dataset_id + '/head', data = {'n': n})
	return pd.DataFrame(r.json())

def get(dataset_id):
	"""Get dataset from the **weles** as dataframe.

	Parameters
	----------
	dataset_id : string
		hash of the dataset

	Returns
	-------
	pandas.DataFrame
		pandas Data Frame containing the requested dataset
	"""

	if not isinstance(dataset_id, str):
		raise ValueError("dataset_id must be a string")
	if not len(dataset_id) == 64:
		raise ValueError("dataset_id must be 64 character long")

	r = requests.get('http://192.168.137.64/datasets/' + dataset_id)

	return pd.DataFrame(r.json())

def info(dataset_id):
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

	if not isinstance(dataset_id, str):
		raise ValueError("dataset_id must be a string")
	if not len(dataset_id) == 64:
		raise ValueError("dataset_id must be 64 character long")

	r = requests.get('http://192.168.137.64/datasets/' + dataset_id + '/info')
	r = r.json()
	r['columns'] = pd.DataFrame(r['columns'])

	return r
