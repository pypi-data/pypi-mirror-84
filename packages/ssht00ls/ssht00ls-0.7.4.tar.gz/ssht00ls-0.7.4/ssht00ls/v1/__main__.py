#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, pathlib

# functions.
def __get_file_path_base__(path, back=1):
	path = path.replace('//','/')
	if path[len(path)-1] == "/": path = path[:-1]
	string, items, c = "", path.split("/"), 0
	for item in items:
		if c == len(items)-(1+back):
			string += "/"+item
			break
		else:
			string += "/"+item
		c += 1
	return string+"/"

# settings.
SOURCE_NAME = "ssht00ls"
VERSION = "v1"
SOURCE_PATH = __get_file_path_base__(__file__, back=2)
BASE = __get_file_path_base__(SOURCE_PATH)
sys.path.insert(1, BASE)

# imports.
from ssht00ls.v1.classes.config import *
from ssht00ls.v1.classes import *

# the cli object class.
class CLI(object):
	def __init__(self, alias=None):
		
		# variables.
		self.modes={
			"-h / --help":"Show the documentation.",
		},
		self.options={
		}
		self.alias = ALIAS
		self.documentation = self.__create_docs__()

		#
	def start(self):
		
		# help.
		if self.__argument_present__('-h') or self.__argument_present__('--help'):
			print(self.documentation)

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	# system functions.
	def __create_docs__(self):
		m = str(json.dumps(self.modes, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		#o = str(json.dumps(self.options, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		o = str(json.dumps(self.options, indent=4)).replace('{\n','').replace('}\n','').replace('    "','    ').replace('": "',' : ').replace('",\n','\n').replace('"\n','\n')[:-2]
		c = "\nAuthor: Daan van den Bergh \nCopyright: © Daan van den Bergh 2020. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		doc += c
		return doc
	def __argument_present__(self, argument):
		if argument in sys.argv: return True
		else: return False
	def __get_argument__(self, argument, required=True, index=1, empty=None):

		# check presence.
		if argument not in sys.argv:
			if required:
				raise ValueError(f"Define parameter [{argument}].")
			else: return empty

		# retrieve.
		y = 0
		for x in sys.argv:
			try:
				if x == argument: return sys.argv[y+index]
			except IndexError:
				if required:
					raise ValueError(f"Define parameter [{argument}].")
				else: return empty
			y += 1

		# should not happen.
		return empty
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
