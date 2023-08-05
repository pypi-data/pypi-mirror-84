#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.v1.classes.config import * 
import os, sys, requests, ast, json, pathlib, glob, string, getpass, django

# init a default response.
def __default_response__():
	return {
		"success":False,
		"error":None,
		"message":None,
	}
	
# check parameters.
def __check_parameter__(parameter=None, name="parameter", empty_value=None, response=None):
	if response == None: response = __default_response__()
	if parameter == empty_value: 
		response["error"] = f"Define parameter [{name}]."
		return False, response
	else: return True, response
def __check_parameters__(parameters={"parameter":None}, empty_value=None, response=None):
	response = __default_response__()
	for id, value in parameters.items():
		success, response = __check_parameter__(value, id, empty_value=empty_value, response=response)
		if not success: return False, response
	return True, response

# get the size of an file / directory.
def __get_file_path_size__(path=None, mode="auto", options=["auto", "bytes", "kb", "mb", "gb", "tb"], type="string"):
	def get_size(directory):
		total = 0
		try:
			# print("[+] Getting the size of", directory)
			for entry in os.scandir(directory):
				if entry.is_file():
					# if it's a file, use stat() function
					total += entry.stat().st_size
				elif entry.is_dir():
					# if it's a directory, recursively call this function
					total += get_size(entry.path)
		except NotADirectoryError:
			# if `directory` isn't a directory, get the file size then
			return os.path.getsize(directory)
		except PermissionError:
			# if for whatever reason we can't open the folder, return 0
			return 0
		return total
	total_size = get_size(path)
	if mode == "auto":
		if int(total_size/1024**4) >= 10:
			total_size = '{:,} TB'.format(int(round(total_size/1024**4,2))).replace(',', '.')
		elif int(total_size/1024**3) >= 10:
			total_size = '{:,} GB'.format(int(round(total_size/1024**3,2))).replace(',', '.')
		elif int(total_size/1024**2) >= 10:
			total_size = '{:,} MB'.format(int(round(total_size/1024**2,2))).replace(',', '.')
		elif int(total_size/1024) >= 10:
			total_size = '{:,} KB'.format(int(round(total_size/1024,2))).replace(',', '.')
		else:
			total_size = '{:,} Bytes'.format(int(int(total_size))).replace(',', '.')
	elif mode == "bytes" or mode == "bytes".upper(): total_size = '{:,} Bytes'.format(int(total_size)).replace(',', '.') 
	elif mode == "kb" or mode == "kb".upper(): total_size = '{:,} KB'.format(int(round(total_size/1024,2))).replace(',', '.') 
	elif mode == "mb" or mode == "mb".upper(): total_size = '{:,} MB'.format(int(round(total_size/1024**2,2))).replace(',', '.') 
	elif mode == "gb" or mode == "gb".upper(): total_size = '{:,} GB'.format(int(round(total_size/1024**3,2))).replace(',', '.') 
	elif mode == "tb" or mode == "tb".upper(): total_size = '{:,} TB'.format(int(round(total_size/1024**4,2))).replace(',', '.') 
	else: __error__("selected an invalid size mode [{}], options {}.".format(mode, options))
	if type == "integer":
		return int(total_size.split(" ")[0])
	else: return total_size 
# get an file paths name.
def __get_file_path_name__(file):
	if file[len(file)-1] == "/": file = file[:-1]
	return file.split("/")[len(file.split("/"))-1]
# set a file path permission.
def __set_file_path_permission__(path, permission=755, sudo=False, recursive=False):
	if recursive: recursive = "-R "
	else: recursive = ""
	if sudo: sudo = "sudo "
	else: sudo = ""
	os.system(f"{sudo}chmod {recursive}{permission} {path}")
# set a file path ownership.
def __set_file_path_ownership__(path, owner=os.environ.get("USER"), group=None, sudo=False, recursive=False):
	if recursive: recursive = "-R "
	else: recursive = ""
	if sudo: sudo = "sudo "
	else: sudo = ""
	if group == None: group = __get_empty_group__()
	os.system(f"{sudo}chown {recursive}{owner}:{group} {path}")
def __get_empty_group__():
	if OS in ["osx"]: return "wheel"
	elif OS in ["linux"]: return "root"
def __delete_file_path__(path, sudo=False, forced=False):
	if sudo: sudo = "sudo "
	options = ""
	if forced: 
		options = " -f "
		if os.path.isdir(path): options = " -fr "
	elif os.path.isdir(path): options = " -r "
	os.system(f"{sudo}rm{options}{path}")

# converting variables.
def __array_to_string__(array, joiner=" "):
	string = ""
	for i in array:
		if string == "": string = str(i)
		else: string += joiner+str(i)
	return string
def __string_to_array__(string, split_char=","):
	array = []
	for i in string.split(split_char):
		for x in range(11):
			if i[0] == " ": i = i[1:]
			elif i[len(i)-1] == " ": i = i[:-1]
			else: break
		array.append(i)
	return array
def __string_to_boolean__(string):
	if string in ["true", "True", True]: return True
	elif string in ["false", "False", False]: return False
	else: raise ValueError(f"Could not convert string [{string}] to a boolean.")
def __string_to_bash__(string):
	a = string.replace('(','\(').replace(')','\)').replace("'","\'").replace(" ","\ ").replace("$","\$").replace("!","\!").replace("?","\?").replace("@","\@").replace("$","\$").replace("%","\%").replace("^","\^").replace("&","\&").replace("*","\*").replace("'","\'").replace('"','\"')       
	return a

# generation.
def __generate_pincode__(characters=6, charset=string.digits):
		return ''.join(random.choice(charset) for x in range(characters))
		#
def __generate_shell_string__(characters=6, numerical_characters=False, special_characters=False):
	charset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	for x in ast.literal_eval(str(charset)): charset.append(x.upper())
	if numerical_characters:
		for x in [
			'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
		]: charset.append(x)
	if special_characters:
		for x in [
			'-', '+', '_'
		]: charset.append(x)
	return ''.join(random.choice(charset) for x in range(characters))
	#

# execute a shell command.
def __execute__(
	# the command in array.
	command=[],
	# wait till the command is pinished. 
	wait=False,
	# the commands timeout, [timeout] overwrites parameter [wait].
	timeout=None, 
	# the commands output return format: string / array.
	return_format="string", 
	# the subprocess.Popen.shell argument.
	shell=False,
	# pass a input string to the process.
	input=None,
):
	def __convert__(byte_array, return_format=return_format):
		if return_format == "string":
			lines = ""
			for line in byte_array:
				lines += line.decode()
			return lines
		elif return_format == "array":
			lines = []
			for line in byte_array:
				lines.append(line.decode().replace("\n","").replace("\\n",""))
			return lines

	# create process.
	p = subprocess.Popen(
		command, 
		shell=shell,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=subprocess.PIPE,)
	
	# send input.
	if input != None:
		if isinstance(input, list):
			for s in input:
				p.stdin.write(f'{s}\n'.encode())
		elif isinstance(input, str):
			p.stdin.write(f'{input}\n'.encode())
		else: raise ValueError("Invalid format for parameter [input] required format: [string, array].")
		p.stdin.flush()
	
	# timeout.
	if timeout != None:
		time.sleep(timeout)
		p.terminate()
	
	# await.
	elif wait:
		p.wait()

	# get output.
	output = __convert__(p.stdout.readlines(), return_format=return_format)
	if return_format == "string" and output == "":
		output = __convert__(p.stderr.readlines(), return_format=return_format)
	elif return_format == "array" and output == []:
		output = __convert__(p.stderr.readlines(), return_format=return_format)
	return output

# execute a shell script.
def __execute_script__(script=""):
	path = "/tmp/shell_script.sh"
	__save_file__(path, script)
	__set_file_path_permission__(path,permission=755)
	output = __execute__(command=["sh", path])
	__delete_file_path__(path, forced=True)
	return output

# save & load jsons.
def __load_json__(path):
	data = None
	with open(path, "r") as json_file:
		data = json.load(json_file)
	return data
def __save_json__(path, data):
	with open(path, "w") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)

# save & load files.
def __load_file__(path):
	file = open(path,mode='rb')
	data = file.read().decode()
	file.close()
	return data
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()
