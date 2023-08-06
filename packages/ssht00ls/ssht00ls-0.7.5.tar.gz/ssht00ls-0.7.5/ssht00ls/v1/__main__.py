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

# testing.
os.system("clear")
"""
response = agent.add(
	path=smart_cards.path,
	smart_card=True,
	pin=606233,)
print("Add to agent response:", json.dumps(response, indent=4))
if response["error"] != None: quit()
response = config.create_alias( 
		# the servers name.
		server="testserver", 
		# the username.
		username="administrator", 
		# the ip of the server.
		ip="192.168.1.203",
		# the port of the server.
		port=22,
		# the path to the private key.
		key=smart_cards.path,
		# smart card.
		smart_card=True,)
print("Create alias response:", json.dumps(response, indent=4))
if response["error"] != None: quit()
"""
os.system("rm -fr /tmp/storages.json")
response = scp.download(
		server_path="/nas.info/storages.json",
		client_path="/tmp/storages.json",
		alias="administrator.testserver",)
print("Download (scp) response:", json.dumps(response, indent=4))
quit()

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"-h / --help":"Show the documentation.",
			},
			options={},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		
		# help.
		if self.arguments_present(['-h', '--help']):
			print(self.documentation)

		# check create alias.
		if self.argument_present('--check-alias'):
			self.check_alias()

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
