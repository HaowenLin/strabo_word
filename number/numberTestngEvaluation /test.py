#!/usr/bin/env python
# -*- coding: utf-8 -*-


from googleapiclient.discovery import build
import inflect
import codecs
from random import randint


def write_to_file(filename):
    f = open (filename, 'w')



def english2other(lang,word):

    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.

    service = build('translate', 'v2',
    developerKey='AIzaSyBkcch0NhQm-misclNx7Suc2AMc__8ikug')


    translation= service.translations().list(
    source='en',
    target=lang,
    q=[word]
    ).execute()['translations'][0]['translatedText']
    print word, translation
    return translation

def generate_random_numbers():
    for i in range(0,100,1):
        print(randint (1, 5000000000))

def number2English():
    p = inflect.engine ()
    filename = "lib/translation_google/random_numbers.txt"
    with open (filename) as f:
        for line in f:

            ans = p.number_to_words(line)
            print ans


def get_supported_lang():
    filename = "lib/translation_google/supported_lang.txt"
    lang = []
    abb = []
    with open (filename) as f:
        for line in f:
            arr = line.split()
            lang.append(arr[0])
            if len(arr) ==2:
                abb.append(arr[1])
            else:
                abb.append(arr[2])
    return lang,abb


def get_translated_numbers():
    numbers_eng  = []
    numbers_digit = []
    filename = "lib/translation_google/numbers_eng.txt"
    with open (filename) as f:
        for line in f:
            line  = line.replace("\n","")
            numbers_eng.append(line)
    f.close()
    filename = "lib/translation_google/random_numbers.txt"


    with open (filename) as f2:
        for line in f2:
            line  = line.replace("\n","")
            numbers_digit.append(line)

    f2.close()


    filename = "lib/translation_google/numberFile.txt"
    language,abb = get_supported_lang()
    f = codecs.open (filename, 'w', encoding='utf-8')
    for i in range(71,72,1): #language
        #len(language)
        for j in range(0,1,1): #numbers
            #len(numbers_digit)
            lang = abb[i]
            lang_all = language[i]
            word = numbers_eng[j]
            ans = numbers_digit[j]
            trans = english2other(lang,word)
            #trans = "???"
            print "lang is : %s word is: %s numbers: %s trans: %s" %(lang,word,ans,trans)
            f.write("#language:" + "\t"+lang_all+"\t"+lang+"\n")
            f.write ("translation:" +"\t" +trans+"\n")
            f.write ("english:" + "\t" + word+"\n")
            f.write ("ans:" + "\t" + ans+"\n")
            f.write("\n")
    f.close()




if __name__ == '__main__':
    #generate_random_numbers()
    #get_supported_lang ()
    #word = 'one'
    #lang = 'zh-CN'
    #english2other(lang,word)
    #number2English ()
    get_translated_numbers()
