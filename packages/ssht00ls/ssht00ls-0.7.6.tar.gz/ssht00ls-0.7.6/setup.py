#!/usr/bin/env python3

# Note!
# ' are required, do not use any ".

# setup.
from setuptools import setup, find_packages
setup(
	name='ssht00ls',
	version='0.7.6',
	description='Some description.',
	url="http://github.com/vandenberghinc/ssht00ls",
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		"asgiref==3.3.0",
		"certifi==2020.6.20",
		"chardet==3.0.4",
		"cl1==0.1.6",
		"Django==3.1.3",
		"fil3s==0.6.7",
		"idna==2.10",
		"pexpect==4.8.0",
		"ptyprocess==0.6.0",
		"pytz==2020.4",
		"r3sponse==0.1.5",
		"requests==2.24.0",
		"sqlparse==0.4.1",
		"urllib3==1.25.11",
	],)