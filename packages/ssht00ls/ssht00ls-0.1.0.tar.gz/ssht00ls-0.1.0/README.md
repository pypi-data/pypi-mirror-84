# ssht00ls
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: ubuntu.
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## WARNING!
THIS REPO IS UNSTABLE AND UNDER DEVELOPMENT.

## Installation
	pip3 install ssht00ls --upgrade

## Python Examples.


### The Key() object class.
The Key() object class.  
```python

# import the package.
import ssht00ls

# generate a key.
response = ssht00ls.key.generate(directory="/path/to/mykey/", passphrase="passphrase123!", comment="my key")

# edit the passphrase of a key.
response = ssht00ls.key.edit_passphrase(path="/path/to/mykey/private_key", new="Passphrase123!", old="passphrase123!")

# create an ssh alias for the key.
response = ssht00ls.key.create_config(self, 
	# the servers name.
	server="myserver", 
	# the username.
	username="administrator", 
	# the ip of the server.
	ip="0.0.0.0",
	# the port of the server.
	port=22,
	# the path to the private key.
	key="/path/to/mykey/private_key",
)
# if successfull you can use the ssh alias <username>.<server>
# $ ssh <username>.<server>

```

### The Agent() object class.
The Agent() object class. 
```python

# import the package.
import ssht00ls

# initialize the ssh agent.
response = ssht00ls.agent.initialize()

# delete all keys from the agent.
response = ssht00ls.agent.delete()

# add a key to the agent.
response = ssht00ls.agent.add("/path/to/mykey/private_key", passphrase="TestPass!")

# check if a key is added to the agent.
response = ssht00ls.agent.check("/path/to/mykey/private_key")

# list all agent keys.
response = ssht00ls.agent.list()

```

### The SSH() object class.
The SSH() object class. 
<br>Make sure the key you are using is added to the ssh agent.
```python

# import the package.
import ssht00ls

# start a ssh session in the terminal console.
ssht00ls.ssh.session(alias="username.server")

# execute a command on the server over ssh.
response = ssht00ls.ssh.command(command=["echo", "$HOME"], alias="username.server")
# or without a created alias.
response = ssht00ls.ssh.command(
	# the command.
	command=["echo", "$HOME"], 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

```

### The SSHFS() object class.
The SSHFS() object class. 
<br>Make sure the key you are using is added to the ssh agent.
```python

# import the package.
import ssht00ls

# mount a remote server directory.
response = ssht00ls.sshfs.mount(
	# the directory paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/", 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

# unmount a mounted directory.
response = ssht00ls.sshfs.unmount(
	client_path="/path/to/directory/", 
	forced=False,
	sudo=False,)

```

### The SCP() object class.
The SCP() object class. 
<br>Make sure the key you are using is added to the ssh agent.
```python

# import the package.
import ssht00ls

# download a server file or directory from a server.
response = ssht00ls.scp.download(
	# the file paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/",
	directory=True, 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

# upload a file or directory to a server.
response = ssht00ls.scp.upload(
	# the file paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/",
	directory=True, 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

```


### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}