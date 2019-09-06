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

def create(user_name, password, mail):
	"""
	Function create_userFunction creates new user in the **weles** base.

	Parameters
	----------
	user_name : string
		your user name, has to be unique, if such user already exists you will get such information in response
	password : string
		your password, passwords are hashed
	mail : string
		your mail

	Returns
	-------
	string
		Information if creating account was successful.
	"""

	if not isinstance(user_name, str):
		raise ValueError("user_name must be a string")
	if not isinstance(password, str):
		raise ValueError("password must be a string")
	if not isinstance(mail, str):
		raise ValueError("mail must be a string")

	r = requests.post('http://192.168.137.64/users/create_user', data = {'user_name': user_name, 'password': password, 'mail': mail})

	return r.text