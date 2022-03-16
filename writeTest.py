import os
import urllib.request, urllib.parse, urllib.error, re
import ssl
import json
import time
import sys
import pyperclip

print("===Initiating translationAssistant===")
files = os.listdir()
lowerfiles = []
for file in files[1:]:
    print(file)
    #makes new list of lowercase file names
    lowerfiles.append(file.lower())
fName = input("===Choose a file from the existing files or input a new filename: ")
#compares the inputted file name to lowercase versions of exisiting file names. Ergo, this is not case sensitive
if fName.lower() in lowerfiles:
    fh = open(fName,"a")
    print("===File opened")
else:
    fh = open(fName,"a+")
    print("===File created")

#returns True if index is in a list
def index_in_list(a_list, index):
    if index + 1 < len(a_list):
        return True
    else:
        return False

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#no idea what this does, pasted from https://stackoverflow.com/questions/14685999/trigger-an-event-when-clipboard-content-changes
sys.path.append(os.path.abspath("SO_site-packages"))

"""input file interface selection code here"""

print("copy a word to your clipboard to begin")
word = pyperclip.paste()
while True:
    #watches clipboard for any changes and brings them in
    tmp_value = pyperclip.paste()
    if tmp_value != word:
        word = tmp_value
        print("Looking up: %s" % str(word)[:20])
    #Setting up to concatenate word to api endpoint url (at least I believe that's what it's called)
        words = dict()
        words['keyword'] = word
        print('making url')
        url = 'https://jisho.org/api/v1/search/words?' + urllib.parse.urlencode(words) #urlencode takes dictionary and formats enteries to be in url
        uh = urllib.request.urlopen(url)
        #getting and interpreting data
        data = uh.read().decode()
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
            continue
        if not js['data']:
            print("Sorry, no results")
            print(url)
            continue
        elif index_in_list(js["data"],1):
            print("Retrieving word - 2")
            #writes to previously opened txt file
            #lst = []
            print("====Definition 1")
            print("====Definition 1",js["data"][0]["japanese"])#,js["data"][0]["senses"][0]["english_definitions"])
            #print("====Definition 2",js["data"][1]["japanese"],js["data"][1]["senses"][0]["english_definitions"])

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
            continue
        else:
            print("Retrieving word - 1")
            print("====Definition 1",js["data"][0]["japanese"])#,js["data"][0]["senses"][0]["english_definitions"])
            '''
            fh.writelines("====Definition 1",js["data"][0]["japanese"],js["data"][0]["senses"][0]["english_definitions"])
            fh.write(str(url))'''
            continue

    else:
        time.sleep(1.0)
        continue
    time.sleep(1.0)
fh.close()
#NEEDS TESTING - '死傷者'
#print(json.dumps(js, indent=4, ensure_ascii=False))
