from distutils.core import setup

setup(name='vimo',
	version='0.1',
	description='The Python client package for communication with model governance base "vimo".',
	url='https://github.com/WojciechKretowicz/vimo',
	author='Wojciech Kretowicz',
	author_email='wojtekkretowicz@gmail.com',
	packages=['vimo'],
	install_requires=[
		'requests',
		'pandas',
	],
      zip_safe=False)
