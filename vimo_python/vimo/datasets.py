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
	"""

	url = 'http://192.168.137.64/datasets/post'

	timestamp = str(datetime.now().timestamp())

	# uploading data
	info = {'user_name': user_name, 'password': password, 'data_name': data_name, 'data_desc': data_desc}
	if type(X) == str:
		# case when data is a path

		files = {'data': open(data, 'rb')}

		# request
		r = requests.post(url, files=files, data=info)
	else:
		# case when data is an object

		# conversion to pandas data frame
		X = pd.DataFrame(X)


		# creating temporary file
		data.to_csv('.tmp_data_' + timestamp + '.csv', index = False)

		files = {'data': open('.tmp_data_' + timestamp + '.csv', 'rb')}

		# request
		r = requests.post(url, files=files, data = info)

		# removing temporary file
		os.remove('.tmp_data_' + timestamp + '.csv')

def head_data(dataset_id, n=5):
	r = requests.get('http://192.168.137.64/datasets/' + dataset_id + '/head', data = {'n': n})
	return pd.DataFrame(r.json())

def get_data(dataset_id):
	r = requests.get('http://192.168.137.64/datasets/' + dataset_id)
	return pd.DataFrame(r.json())
