#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.v1.classes.config import *
from ssht00ls.v1.classes import utils

def __check_os__(supported=[]):
	response = utils.__default_response__()
	if OS not in supported:
		response["error"] = "Unsupported operating system [{}].".format(OS)
		return False,response
	return True,response

# the manager class.
class SmartCards(object):
	def __init__(self):	
		a=1
		#
	def scan(self, silent=False):
		
		# initialize response.
		response = utils.__default_response__()

		# list.
		output = utils.__execute__(["ykman", "list"], shell=False, return_format="array")

		# iterate.
		count, smart_cards = 0, {}
		for card in output:
			if card not in [""]:
				try: 
					serial_number = card.split("Serial: ")[1].replace(" ", "")
					text = card.split(" Serial:")[0]
					smart_cards[serial_number] = SmartCard(serial_number=serial_number)
				except IndexError: 
					response["error"] = "Unrecognized smart card detected. Remove the smart card and plug it back in."
					return response

		# response.
		response["success"] = True
		response["message"] = f"Successfully scanned & detected {len(smart_cards)} smart card(s)."
		response["smart_cards"] = smart_cards
		return response

		#
	def __single_key_plugged_in__(self):

		# scan.
		response = utils.__default_response__()
		l_response = self.scan()
		if l_response["error"] != None: return l_response

		# check one.
		if len(l_response["smart_cards"]) > 1:
			response["error"] = "There are multiple smart cards plugged in."
			return response

		# check zero.
		if len(l_response["smart_cards"]) == 0:
			response["error"] = "There are no smart cards plugged in / detected."
			return response

		# success.
		response["success"] = True
		response["message"] = "There is only one smart cards plugged in."
		return response

# the smart card class.
class SmartCard(object):
	# the smart card is by default a YubiKey 5 NFC
	# main docs: https://support.yubico.com/support/solutions/articles/15000012643-yubikey-manager-cli-ykman-user-manual#ykman_piv_change-management-key1suvy
	# piv: https://developers.yubico.com/PIV/Guides/SSH_with_PIV_and_PKCS11.html
	# docs : https://support.yubico.com/support/solutions/articles/15000011059-yubikey-fips-series-technical-manual#2.3.4_Recommended_PIV_Settings11ale3
	# ssh : https://github.com/fredxinfan/ykman-piv-ssh
	# another ssh : https://somm15.github.io/yubikey/macos/ssh/2018/11/20/welcome-to-jekyll.html
	def __init__(self, serial_number=None):	

		# arguments.
		self.serial_number = serial_number

		# key path.
		if OS in ["linux"]: 
			self.path = None
			for path in [
				"/usr/lib/x86_64-linux-gnu//opensc-pkcs11.so",
				"/usr/lib/x86_64-linux-gnu//opensc-pkcs11.so",
				"/usr/lib/arm-linux-gnueabihf/opensc-pkcs11.so",
				"/usr/local/lib/libykcs11",
			]:
				if os.path.exists(self.path):
					self.path = path
					break
			if self.path == None: raise ValueError("Unable to locate opensc-pkcs11.so path.")
					
		elif OS in ["osx"]: 
			self.path = "/usr/local/lib/libykcs11.dylib"

		# variables.
		self.puk = None
		self.pin = None


		#
	
	# multiple keys plugged in compatible:
	def get_info(self):

		# initialize response.
		response = utils.__default_response__()

		# get info.
		try: 
			output = subprocess.check_output(f"ykman --device {self.serial_number} piv info", shell=True).decode().replace('  ',' ').replace('  ',' ').replace('  ',' ').lower().split('\n')
		except: 
			response["error"] = "failed to retrieve yubikey info."
			return response

		# iterate.
		info = {}
		for x in output:
			if x not in ["", " "]:
				if 'piv version: ' in x:
					info["pin_version"] = x.split("piv version: ")[1]
				elif 'pin tries remaining: ' in x:
					info["pin_attempts"] = x.split("pin tries remaining: ")[1]
		info["serial_number"] = self.serial_number
		response["info"] = info

		# success.
		response["success"] = True
		response["message"] = f"Successfully retrieved the information from smart card [{self.serial_number}]."
		return response

		#
	def unblock_pin(self, 
		# the new pin code.
		pin=None, 
		# the smart cards puk code
		puk=None,
	):
		
		# check params.
		success, response = utils.__check_parameters__(
			empty_value=None,
			parameters={
				"pin":pin,
				"puk":puk,
			})
		if not success: return response

		# initialize response.
		response = utils.__default_response__()

		# unblock.
		output = utils.__execute_script__(f"ykman --device {self.serial_number} piv unblock-pin --puk {puk} --new-pin {pin}", shell=True)

		# handle defaults.
		success, response = self.__handle_default_output__(output)
		if not success: return response

		# handle error.
		if output != "":
			response["error"] = f"Unknown error pin unblocking, output: [{output}]."
			return response

		# handle success.
		response["message"] = f"Successfully unblocked the pin code of smart card [{self.serial_number}]."
		response["success"] = True
		return response

		#
	def change_pin(self, 
		# the smart cards new pin code.
		new=None, 
		# the smart cards old pin code.
		old=123456,
	):

		# check params.
		success, response = utils.__check_parameters__(
			empty_value=None,
			parameters={
				"new":new,
				"old":old,
			})
		if not success: return response

		# initialize response.
		response = utils.__default_response__()

		# do.
		command = f"ykman --device {self.serial_number} piv change-pin -P{old} -n{new}"
		output = utils.__execute_script__(command, shell=True)

		# handle defaults.
		success, response = self.__handle_default_output__(output)
		if not success: return response

		# handle success.
		elif "New PIN set." in output: 
			response["message"] = f"Successfully changed the pin of smart card [{self.serial_number}]."
			response["success"] = True
			return response

		# unknown error.
		else:
			response["error"] = f"Unknown error while changing pin, output: [{output}]."
			return response

		#
	def change_puk(self, 
		# the smart cards new puk code.
		new=None, 
		# the smart cards old puk code.
		old=12345678,
	):

		# check params.
		success, response = utils.__check_parameters__(
			empty_value=None,
			parameters={
				"new":new,
				"old":old,
			})
		if not success: return response

		# initialize response.
		response = utils.__default_response__()

		# do.
		command = f"ykman --device {self.serial_number} piv change-puk -p{old} -n{new}"
		output = utils.__execute_script__(command, shell=True)

		# handle defaults.
		success, response = self.__handle_default_output__(output)
		if not success: return response


		# handle success.
		elif "New PUK set." in output: 
			response["message"] = f"Successfully changed the puk of smart card [{self.serial_number}]."
			response["success"] = True
			return response

		# unknown error.
		else:
			response["error"] = f"Unknown error while changing puk, output: [{output}]."
			return response

		#
	def generate_key(self, 
		# the smart cards pin code.
		pin=None,
	):

		# check params.
		success, response = utils.__check_parameters__(
			empty_value=None,
			parameters={
				"pin":pin,
			})
		if not success: return response

		# initialize response.
		response = utils.__default_response__()

		# do.
		command = f"printf '\\n\\n' | ykman --device {self.serial_number} piv generate-key 9a public.pem --pin-policy ALWAYS  --pin {pin} --management-key 010203040506070801020304050607080102030405060708"
		output = utils.__execute_script__(command, shell=True)
		
		# handle error.
		success, response = self.__handle_default_output__(output)
		if not success: return response
		elif output != "":
			response["error"] = f"Unknown error during key generation, output: [{output}]."
			return response

		# do.
		command = f'ykman --device {self.serial_number} piv generate-certificate -s "/CN=SSH-key/" 9a public.pem --pin {pin} --management-key 010203040506070801020304050607080102030405060708'
		output = utils.__execute_script__(command, shell=True)
		
		# handle error.
		success, response = self.__handle_default_output__(output)
		if not success: return response
		elif output != "":
			response["error"] = f"Unknown error during certificate generation, output: [{output}]."
			return response

		# handle success.
		response["message"] = f"Successfully generated a signed certificate & key for smart card [{self.serial_number}]."
		response["success"] = True
		return response

		#
	def generate_management_key(self, 
		# the smart cards pin code.
		pin=None,
	):

		# check params.
		success, response = utils.__check_parameters__(
			empty_value=None,
			parameters={
				"pin":pin,
			})
		if not success: return response

		# initialize response.
		response = utils.__default_response__()

		# do.
		command = f'ykman --device {self.serial_number} piv change-management-key --generate --protect --pin {pin} --management-key "010203040506070801020304050607080102030405060708"'
		output = utils.__execute_script__(command, shell=True)

		# handle success.
		success, response = self.__handle_default_output__(output)
		if not success: return response
		elif output != "":
			response["error"] = f"Unknown error during management key generation, output: [{output}]."
			return response
		else:
			response["message"] = f"Successfully generated a management key for smart card [{self.serial_number}]."
			response["success"] = True
			return response

		#
	def reset_piv(self): # for when both pin & puk codes are blocked.
		
		# initialize response.
		response = utils.__default_response__()

		# do.
		#output = utils.__execute_script__(f"printf 'y\\n' | ykman --device {self.serial_number} piv reset", shell=True)
		output = utils.__execute_script__(f"printf 'y\\n' | ykman --device {self.serial_number} piv reset", shell=True)
		
		# handle success.
		if "Success!" in output:
			response["success"] = True
			response["message"] = "Successfully resetted the smart card."
			return response

		# handle error.
		else:
			response["error"] = "Failed to reset the smart card."
			return response

	# single key plugged in compatible:
	def export_keys(self, 
		# optionally save the keys to a file.
		path=None, 
	):

		# output.
		response = utils.__default_response__()
		command = f"ssh-keygen -D {self.path} -e"
		output = utils.__execute_script__(command, shell=True, return_format="array")
		
		# error.
		if len(output) == 0 or "ssh-rsa " not in output[0]:
			response["error"] = f"Failed to export smart card [{self.serial_number}]."
			return response
		else:

			# write out.
			if path != None:
				try:
					utils.__save_file__(path, utils.__array_to_string__(output, joiner="\n"))
				except:
					response["error"] = f"Failed to write out the exported key from smart card [{self.serial_number}]."
					return response

			# success.
			response["success"] = True
			response["message"] = f"Successfully exported smart card [{self.serial_number}]."
			response["public_keys"] = output
			return response

		#
	def check_smart_card(self):

		# check.
		response = utils.__default_response__()
		try:
			output = subprocess.check_output("yubico-piv-tool -aversion", shell=True).decode()
		except:
			response["message"] = "Failed to check for yubikey smart cards."
			return response

		# success.
		if "Application version " in output: 
			response["success"] = True
			response["smart_card"] = True
			response["message"] = "Yubikey smart card detected."
			return response
		else: 
			response["success"] = True
			response["smart_card"] = False
			response["message"] = "No yubikey smart card detected."
			return response

		#
	def convert_to_smart_card(self):
		"""
			Option 1:
			should also bring into OTP+U2F+CCID mode.
			$ echo -e '\x06\x00\x00\x00' | u2f-host -d -a sendrecv -c c0

			Option 2:
			Plug in the key.
			$ ykpersonalize -m86
			Unplug the key & in a new terminal.
			$ doas pcscd --foreground --debug
			
		"""

		# check aready converted.
		response = utils.__default_response__()

		l_response = self.check_smart_card()
		if l_response["error"] != None: return l_response
		if l_response["smart_card"]:
			response["success"] = True
			response["message"] = "The plugged in yubikey is already a smart cards."
			return response

		# check os.
		success, response = __check_os__(["linux"])
		if not success: return response



		##################








		
		#output = utils.__execute__("ykpersonalize -m86".split(" "))
		#print(f"CONVERT 2 SMARRT CARD; kpersonalize OUTPUT [{output}]")

		#output = utils.__execute__("doas pcscd --foreground --debug".split(" "))
		#print(f"CONVERT 2 SMARRT CARD; oas pcscd OUTPUT [{output}]")
		print("Key must be plugged in.")
		proc1 = subprocess.Popen(["ykpersonalize", "-m86"], shell=True)
		print("Plug out the key.")
		proc2 = subprocess.Popen(["doas", "pcscd", "--foreground", "--debug"], shell=True)
		print("Plug the key back in.")
		#proc.wait()
		#proc.terminate()
		proc1.wait()
		proc2.wait()
		"""
		# Key must be plugged in.
		# Bring the key into OTP+U2F+CCID mode.
		self.console.execute("ykpersonalize -m86")


		# Unplug the key.
		self.console.log("Unplug the smart key.", self.indent_increaser+2)
		while True:
			if self.console.input("Have you unplugged the smart key?", are_you_sure_enabled=True): break

		# Run in seperate terminal.
		proc = subprocess.Popen(["doas", "pcscd", "--foreground", "--debug"], shell=True)
		#proc.wait()
		#proc.terminate()

		# Plug the key back in.
		self.console.log("Plug the key back in.", self.indent_increaser+2)

		"""
	def install(self):

		# initialize.
		response = utils.__default_response__()
		info = {
			"pin":utils.__generate_pincode__(characters=6),
			"puk":utils.__generate_pincode__(characters=8),
			"public_key":None,
		}

		# check single key plugged in.
		print("__single_key_plugged_in__")
		l_response = smart_cards.__single_key_plugged_in__()
		if l_response["error"] != None: return l_response

		# reset piv.
		print("reset_piv")
		l_response = self.reset_piv()
		if l_response["error"] != None: return l_response

		# convert to smart card.
		print("convert_to_smart_card")
		l_response = self.convert_to_smart_card()
		if l_response["error"] != None: return l_response

		# convert to smart card.
		print("change_pin")
		l_response = self.change_pin(new=info["pin"], old=123456)
		if l_response["error"] != None: return l_response

		# convert to smart card.
		print("change_puk")
		l_response = self.change_puk(new=info["puk"], old=12345678)
		if l_response["error"] != None: return l_response

		# convert to smart card.
		print("generate_key")
		l_response = self.generate_key(pin=info["pin"])
		if l_response["error"] != None: return l_response

		# convert to smart card.
		print("generate_management_key")
		l_response = self.generate_management_key(pin=info["pin"])
		if l_response["error"] != None: return l_response

		# success.
		response["success"] = True
		response["message"] = f"Successfully installed smart card [{self.serial_number}]."
		response["pin"] = info["pin"]
		response["puk"] = info["puk"]
		return response

		#

	# system functions.
	def __handle_default_output__(self, output):

		# defaults.
		response = utils.__default_response__()
		if isinstance(output, list): output = utils.__array_to_string__(output, joiner="\n")

		# handle.
		if "Incorrect PUK" in output:
			response["error"] = f"Provided an incorrect puk code."
			return False, response
		elif "Incorrect PIN" in output:
			info = self.get_info()
			if info['success']: response["error"] = f"Provided an incorrect pin code, {info['pin_attempts']} attempts left."
			else: response["error"] = f"Provided an incorrect pin code."
			return False, response
		elif "PUK is blocked" in output:
			response["error"] = f"The puk code of smart card [{self.serial_number}] is blocked."
			return False, response
		elif "Error: " in output:
			response["error"] = output.split("Error: ")[1].replace('.\n', '. ').replace('\n', '')
			return False, response

		# success.
		return True, response


"""

# initialized classes.
smart_cards = SmartCards()

# scan for connected smart cards.
response = smart_cards.scan()

# select an initialized smart card object.
smart_card = response["smart_cards"]["10968447"]

# get information.
response = smart_card.get_info()

# install a new smart card.
# (warning: resets the smart card!)
response = smart_card.install()

# export the public keys.
response = smart_card.export_keys(
	# optionally save the keys to a file.
	path="/tmp/public_keys",)

# reset the smart card.
response = smart_card.reset_piv()

# change the pin code.
response = smart_card.change_pin(
	# the smart cards new puk code.
	new=123456, 
	# the smart cards old puk code.
	old=123456,)

# change the puk code.
response = smart_card.change_puk(
	# the smart cards new puk code.
	new=12345678, 
	# the smart cards old puk code.
	old=12345678,)

# unblock the pin code.
response = smart_card.unblock_pin(
	# the new pin code.
	pin=123456, 
	# the smart cards puk code
	puk=12345678,)

# generate a new key inside the smart card.
response = smart_card.generate_key(
	# the smart cards pin code.
	pin=123456, )

# generate a new management key inside the smart card.
response = smart_card.generate_management_key(
	# the smart cards pin code.
	pin=123456, )

# check if the yubikey is in the correct mode.
response = smart_card.check_smart_card()

# convert a yubikey into a piv smart card.
# (experimental)
response = smart_card.convert_to_smart_card()

"""
