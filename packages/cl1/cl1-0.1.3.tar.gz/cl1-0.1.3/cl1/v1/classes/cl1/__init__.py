#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from cl1.v1.classes.config import *

# argument functions.
def argument_present(arguments):
	if isinstance(arguments, str):
		if arguments in sys.argv: return True
		else: return False
	elif isinstance(arguments, list):
		for argument in arguments:
			if argument in sys.argv: return True
		return False
	else: raise ValueError("Invalid usage, arguments must either be a list or string.")
def get_argument(argument, required=True, index=1, empty=None):

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

# a default cli object
class CLI(object):
	def __init__(self, alias=None, modes={}, options={}, executable=__file__):

		# arguments.
		self.alias = alias
		self.modes = modes
		self.options = options
		self.documentation = self.__create_docs__()

		#
	# system functions.
	def __create_docs__(self):
		m = str(json.dumps(self.modes, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		o = str(json.dumps(self.options, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		c = "\nAuthor: Daan van den Bergh \nCopyright: © Daan van den Bergh 2020. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		doc += c
		return doc
	def __argument_present__(self, argument):
		return __argument_present__(argument)
	def __get_argument__(self, argument, required=True, retrieve=False, index=1, return_format="string", empty=None):
		return __get_argument__(argument, required=required, retrieve=retrieve, index=index, return_format=return_format, empty=empty)
	def __check_alias__(self):
		alias = self.alias
		executable = self.executable
		if '__main__.py' in executable: executable = executable.replace("__main__.py", "")
		path = f"/usr/local/bin/{alias}"
		if not os.path.exists(path):
			file = f"""package={executable}\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
			os.system(f"sudo touch {path}")
			os.system(f"sudo chmod 755 {path}")
			if OS in ["osx"]:
				os.system(f"sudo chown {os.environ.get('USER')}:wheel {path}")
			elif OS in ["linux"]:
				os.system(f"sudo chown {os.environ.get('USER')}:root {path}")
			utils.__save_file__(f"{path}", file)
			os.system(f"sudo chmod 755 {path}")
			if '--silent' not in sys.argv:
				print(f'Successfully created alias: {alias}.')
				print(f"Check out the docs for more info $: {alias} -h")


#