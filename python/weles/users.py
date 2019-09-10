"""@package docstring
The module related to users in the **weles**
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

def create(mail):
	"""
	Function create_userFunction creates new user in the **weles** base.

	Parameters
	----------
	mail : string
		your mail

	Returns
	-------
	string
		Information if creating account was successful.
	"""

	user_name = input('user: ')
	password = input('password: ')

	if not isinstance(user_name, str):
		raise ValueError("user_name must be a string")
	if not isinstance(password, str):
		raise ValueError("password must be a string")
	if not isinstance(mail, str):
		raise ValueError("mail must be a string")

	r = requests.post('http://192.168.137.64/users/create_user', data = {'user_name': user_name, 'password': password, 'mail': mail})

	return r.text
