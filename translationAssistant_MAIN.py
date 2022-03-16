import urllib.request, urllib.parse, urllib.error, re
import ssl
import json
import time
import sys
import os
import pyperclip
#returns True if index is in a list
def index_in_list(a_list, index):
    if index + 1 < len(a_list):
        return True
    else:
        return False
#checks to see if string has numbers in it
def containNum(string):
    return any(char.isdigit() for char in string)
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#no idea what that does, pasted from https://stackoverflow.com/questions/14685999/trigger-an-event-when-clipboard-content-changes
sys.path.append(os.path.abspath("SO_site-packages"))

#file selection interface
print("===Initiating translationAssistant===")
files = os.listdir("Output/")
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

print("copy a word to your clipboard to begin")
word = pyperclip.paste()
while True:
    #watches clipboard for any changes and brings them in
    tmp_value = pyperclip.paste()
    if tmp_value == word:
        time.sleep(1.0)
        continue
    else:
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
            print('loading json')
            js = json.loads(data)
        except:
            print('no json')
            js = None
            #checks status of website, if not 'ok' goes back to word input
        if not js or "status" not in js["meta"] or js["meta"]["status"] != 200:
            print('==== Failure To Retrieve ====')
            print('==== Dumping Data ====')
            #print("===Pretty JSON===")
            print(json.dumps(js, indent=4, ensure_ascii=False))
            continue


        print('writing to file')
        #print(json.dumps(js, indent=4, ensure_ascii=False))
        iter = 0
        if not js["data"]:
            print('js["data"] is empty')
            fh.write("Sorry, no results\n")
        for item in js["data"]:
            if iter == 3:
                break
            if containNum(item['slug']):
                continue
            slug = item["slug"]
            #print('slug found')
            reading = item["japanese"][0]["reading"]
            #print('reading found')
            fh.write("Word: ")
            #print('word written')
            fh.write(slug+'\n')
            #print('slug written')
            fh.write("Reading: ")
            fh.write(reading+'\n')
            #print('reading written')
            fh.write("Definition: ")
            for item in js["data"][iter]["senses"][0]["english_definitions"]:
                fh.write(item + "|")
                #print('definition written')
            fh.write('\n')
            iter +=1
            #print(iter)
        fh.write(url + "\n")
        fh.write("===========\n")
        #skips buffer and writes to file immediately
        fh.flush()
        os.fsync(fh.fileno())
        print("copy a word to your clipboard to continue")
    time.sleep(1.0)
fh.close()

'''
        if index_in_list(js["data"],1):
            print("Retrieving word - 2")
            print("====Definition 1",js["data"][0]["japanese"],js["data"][0]["senses"][0]["english_definitions"])
            print("====Definition 2",js["data"][1]["japanese"],js["data"][1]["senses"][0]["english_definitions"])
            print(url)
            continue
        else:
            print("Retrieving word - 1")
            #print(json.dumps(js, indent=4, ensure_ascii=False))
            print("====Definition 1",js["data"][0]["japanese"],js["data"][0]["senses"][0]["english_definitions"])
            print(url)
            continue
            '''
#NEEDS TESTING - '死傷者'
'''Looking up: 開かれ
making url
loading json
writing to file
Traceback (most recent call last):
  File "translationAssistant_MAIN.py", line 79, in <module>
    reading = item["japanese"][0]["reading"]
KeyError: 'reading'

KeyError: ’word' on なり


'''
