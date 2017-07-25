
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import csv,sys
import re
import codecs
import math

one = []
two = []
three = []
four = []
five = []
six = []
seven = []
eight = []
nine = []
ten = []


# one = ""
# two = ""
# three = ""
# four = ""
# five = ""
# six = ""
# seven = ""
# eight = ""
# nine = ""
# ten = ""


class numberTuple:
    def __init__(self, content, start,end):
        self.content = content
        self.start = start
        self.end = end

    def __str__(self):
        return '[%s, %d,%d],' % (self.content, self.start,self.end)

def get_spelled_out_num(text):
    #print text
    my_list=[one,two,three,four,five,six,seven,eight,nine]
    for count,name in enumerate(my_list):
        #if text.encode("utf-8") in name:
        if text.lower() in name:
            print "num: %s, %d" %(text,count+1)
            return str(count+1)
    return text

def isIntegre(i):

    # if not hasattr(isIntegre, '_re'):
    #     isIntegre._re = re.compile(r"[-+]?\d+(\.0*)?$")
    # return isIntegre._re.match(str(i)) is not None
    try:
        float (i)
        return True
    except ValueError:
        return False



def read_digit_lib():
    d={}
    filename  = "lib/unicode_digit.txt"
    with open (filename) as file:
        for line in file:
            code,name = line.split("\t")
            hex_code = int(code,16)+int("0x200", 16)

            d[int(code,16)] = name
    return d

def exchange_comma(number):
    number = number.replace(",","@@")
    number = number.replace(".",",")
    number = number.replace ("@@", ".")
    return number


def english2digit():
    d={}
    filename  = "lib/english_digit.txt"
    with open (filename) as file:
        for line in file:
            number,name = line.split("\t")
            d[name] =number

    return d


def is_digit(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def check_end_poing(text,endposition):
    if text.endswith('.') or text.endswith(','):
        text = text[:-1]
        endposition-=1
    return text,endposition


def char2number(letter):
    #print hex(ord(letter))
    formCode = 0
    name="digit"



    if ord (letter) in digit_dic:

        number = 1

        nameStr = digit_dic[ord (letter)]
        #print nameStr
        if "number" in nameStr.lower():
            formCode = 1
        if "thousands separator" in nameStr.lower():
            nameStr = "thousands separator"
            return english_digit_dic[nameStr],formCode
        nameStr = nameStr.lower()
        name_arr = nameStr.split(" ")

        for name in name_arr:
            if name in english_digit_dic:
                number *= int(english_digit_dic[name])

        return str(number),formCode
    else:
        return letter,formCode

def process_comma(number):
    if "," in number:
        saparateNum = number.split(",")
        for i in range (1, len (saparateNum) - 1, 1):
            if len(saparateNum[i])!=3:
                return number

        buffer = ""
        for i in range (0, len(saparateNum) - 1, 1):
            buffer += saparateNum[i]

        arr = []
        if "." in saparateNum[len(saparateNum) - 1]:
            arr = saparateNum[len(saparateNum) - 1].split(".")
            if not arr or len(arr[0]) != 3:
            #print "what %s " %(saparateNum)
                buffer += "."
        else:
            if len(saparateNum[len(saparateNum) - 1])!=3:
                buffer += "."
        buffer += saparateNum[len (saparateNum) - 1]
        number = buffer
    return number





#
# def check_multiple_digit(text):




def get_letter(text,ans,bytePosition):
    #ans = []
    #bytePosition = 0
    startPosition = bytePosition
    endPosition = bytePosition
    isContinue = 0
    number = ""
    number2=0
    curNum=0
    count = 0
    digitStr = ""
    formCode=0
    ori=""
    for letter in unicode(text,"utf-8"):

        #numString = number

        letter, code= char2number(letter)
        #letter = get_spelled_out_num(letter)





        #print "letter %s" %(letter)
        if code==1:
            formCode=1
        if is_digit(letter): # if the char is int
            #number += letter # append to the buffer string
            if code==0 or number == "":
                if number == "" and int(letter)==10:
                    number+="1"
                else:
                    number += letter
            else :
                if int(letter)<100 and int(letter)!=10:
                    number+=letter

            #print "number2: %d letter: %d curnum: %d number:%s"%(number2,int(letter),curNum,number)
            if isContinue == 0: #starting position of the number
                startPosition = bytePosition

            isContinue = 1

        elif (letter ==".") or (letter==",") or (letter==" "):
                if curNum!=0:
                    number2=curNum
                if number != "":
                    number+=letter
                    isContinue = 1
                else:
                    isContinue =0


        else:
            if curNum != 0:
                number2 += curNum
            if isContinue == 1:
                endPosition = bytePosition
                ori = number
                number =number.replace(" ","")
                number_changed = exchange_comma(number)
                #print "ok %s %s" % (number, number_changed)
                number=process_comma(number)
                number,endPosition=check_end_poing(number,endPosition)
                number_changed=process_comma(number_changed)
                number_changed, endPosition = check_end_poing (number_changed, endPosition)
                #print number
                #print number_changed
                #print number_changed
                print "ok %s %s"%(number,number_changed)
                # if formCode == 1:
                #     number = str(number2)
                #     number_changed= str(number2)
                if (ori.count(".") >1 or " " in ori) and isIntegre(number_changed):
                    number=number_changed

                if isIntegre(number) :

                    number,endPosition=check_end_poing(number,endPosition)
                    newTuple = numberTuple(number, startPosition, endPosition)
                    print 252
                    ans.append (newTuple)
                else:
                    number=ori
                    newTuple = numberTuple(number, startPosition, endPosition)
                    print 257
                    ans.append (newTuple)
                number = ""
                number2=0
                curNum=0
                startPosition = 0
                endPosition = 0
                ori=""
                formCode=0
                #numString=''
            isContinue = 0

        bytePosition += 1
    #print mystring
    if number != "":
        endPosition = bytePosition
        number, endPosition = check_end_poing (number, endPosition)
        newTuple = numberTuple(number, startPosition, endPosition)
        #print 273
        ans.append(newTuple)

    return ans


def get_spelled_out_dic():
    # one = []
    # two = []
    # three =[]
    # four =[]
    # five =[]
    # six = []
    # seven =[]
    # eight =[]
    # nine =[]
    # ten =[]
    my_lists = {}
    my_lists["one"] = one
    my_lists["two"] = two
    my_lists["three"] = three
    my_lists["four"] = four
    my_lists["five"] = five
    my_lists["six"] =six
    my_lists["seven"] =seven
    my_lists["eight"] = eight
    my_lists["nine"] = nine
    my_lists["ten"] = ten

    dicName = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    #dicName = ["one"]
    for name in dicName:
        filename = "lib/digits/" + name + ".txt"
        with open (filename) as f:
            for line in f:
                line = line.replace("\n","")
                line =re.sub(r'\# .*?\# ','',line)
                my_lists[name].append(line)
            #my_lists[name] = f.read().replace('\n', '')



def get_word(text):

    ans = []
    bytePosition = 0
    startPosition = 0
    endPosition = 0
    isContinue = 0
    number = ""

    for word in text.split():
        #print word
        word =get_spelled_out_num(word)
        #print word
        if is_digit (word):
            #print "1"
            startPosition = bytePosition
            endPosition = startPosition+len(word)
            word, endPosition = check_end_poing (word, endPosition)
            newTuple = numberTuple(word, startPosition, endPosition)
            #print 334
            ans.append(newTuple)
        else:
            #print "2"
            ans= get_letter(word,ans,bytePosition)
        bytePosition+=len(word)
        bytePosition+=1
    return ans










if __name__ == '__main__':

    get_spelled_out_dic()

    digit_dic = read_digit_lib()
    english_digit_dic = english2digit()

    #filename = sys.argv[1]
    #filename = "data/text/nep.txt"
    filename="data/ar.txt"
    text = open(filename, 'r').read()
    # ans=get_letter(text)
    #
    #
    ans = get_word(text)
    f = open('output.txt', 'w')
    #

    for word in ans:
        print word
        f.write(str(word.content)+"\t"+str(word.start)+"\t"+str(word.end))
    get_word(text)
