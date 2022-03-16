import os
#import urllib.request, urllib.parse, urllib.error, re
#import ssl
import json
import time
import sys
#import pyperclip

#returns True if index is in a list
def index_in_list(a_list, index):
    if index + 1 < len(a_list):
        return True
    else:
        return False
fh = open("testFile.txt","a+")
while True:
    uh = open('sampleJson.txt')
    #getting and interpreting data
    data = uh.read()
    try:
        js = json.loads(data)
        #print(json.dumps(js, indent=4, ensure_ascii=False))
    except:
        js = None
        #checks status of website, if not 'ok' goes back to word input
    if not js or "status" not in js["meta"] or js["meta"]["status"] != 200:
        print('==== Failure To Retrieve ====')
        print('==== Dumping Data ====')
        #print("===Pretty JSON===")
        #print(json.dumps(js, indent=4, ensure_ascii=False))
        break
    toPrint = list()
    iter = 0
    if not js['data']:
        print("Sorry, no results")
        print(url)
        break
    elif index_in_list(js["data"],1):
        #print("Retrieving word - 2")
        #writes to previously opened txt file
        #lst = []
        #print("====Definition 1")
        #print("====Definition 1",js["data"][0]["senses"][0]["english_definitions"])
        #print("====Definition 2",js["data"][1]["japanese"],js["data"][1]["senses"][0]["english_definitions"])
        fh.write("===========\n")
        for item in js["data"]:#[0]["japanese"]:
            if iter == 3:
                break
            word = item["slug"]
            reading = item["japanese"][0]["reading"]
            fh.write("Word: ")
            fh.write(word+'\n')
            fh.write("Reading: ")
            fh.write(reading+'\n')
            fh.write("Definition: ")
            for item in js["data"][0]["senses"][0]["english_definitions"]:
                definition = item
                fh.write(definition + "|")
            fh.write('\n')
            iter +=1
        fh.write("===========\n")
        fh.close()

        #    print("word",item['word'],
        #    "reading",item['reading'])

        #print(json.dumps(js, indent=4, ensure_ascii=False))

        #for result in (js["data"][0]["japanese"]["word"]):
        #    print(result)
        #print(js["data"][0]["japanese"]["word"])
        #print(js["data"][0]["japanese"]["reading"])
        #print(js["data"][0]["senses"][0]["english_definitions"])
        #fh.writelines(lst)
        '''
        fh.writelines("====Definition 1",js["data"][0]["japanese"],js["data"][0]["senses"][0]["english_definitions"])
        fh.writelines("====Definition 2",js["data"][1]["japanese"],js["data"][1]["senses"][0]["english_definitions"])
        '''
        #fh.write(str(url))
        break
    else:
        print("Retrieving word - 1")
        print("====Definition 1",js["data"][0]["japanese"])#,js["data"][0]["senses"][0]["english_definitions"])
        '''
        fh.writelines("====Definition 1",js["data"][0]["japanese"],js["data"][0]["senses"][0]["english_definitions"])
        fh.write(str(url))'''
        break
time.sleep(1.0)
