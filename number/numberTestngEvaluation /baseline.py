# -*- coding: utf-8 -*-
import csv,sys
import re
import codecs




class numberTuple:
    def __init__(self, content, start,end):
        self.content = content
        self.start = start
        self.end = end

    def __str__(self):
        return '[%s, %d,%d],' % (self.content, self.start,self.end)



def isIntegre(i):

    # if not hasattr(isIntegre, '_re'):
    #     isIntegre._re = re.compile(r"[-+]?\d+(\.0*)?$")
    # return isIntegre._re.match(str(i)) is not None
    try:
        float (i)
        return True
    except ValueError:
        return False

def checkDigitArabic (char):
        # arabicdict = {}
        # for n in range (0x600, 0x700):
        #     c = chr (n)
        #     try:
        #         id = unicodedata.name (c).lower ()
        #         if 'arabic letter' in id:
        #             arabicdict[c] = id[14:]
        #     except ValueError:
        #         pass
        # d ={}
        # with open ("arabic.txt") as f:
        #     for line in f:
        #         items = line.split("::")
        #         d[items[0]] = items[1]
        #
        # if char in d :
        #     return d[char]
        # else:
        #     return char

        # return ''.join ([eastern_to_western[c] for c in char])
        # table = {0660: 0030,  # 0
        #          0661: 0031,  # 1
        #          0662: 0032,  # 2
        #          0663: 0033,  # 3
        #          0664: 0034,  # 4
        #          0665: 0035,  # 5
        #          0666: 0036,  # 6
        #          0667: 0037,  # 7
        #          1784: 38,  # 8
        #          1785: 39}
        # eastern_to_western = {"٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4", "٥": "5", "٦": "6", "٧": "7", "٨": "8",
        #                       "٩": "9"}
        # print char
        # print u'٠'
        ans = map(int,re.findall(ur'\d+', char, re.U))
        if len(ans)==0:
            return char
        else:
            return str(ans[0])


def checkDigitChinese(text,numString):
     #print "???"+text +"\n"
     chineseNum = False
     chineseDictionary={'零':0,
                        '一':1,
                        '二':2,
                        '两': 2,
                        '三':3,
                        '四':4,
                        '五':5,
                        '六':6,
                        '七':7,
                        '八':8,
                        '九':9,
                        '十':10,
                        '百':100,
                        '千':1000,
                        '万':10000,
                        '亿':100000000,
                        '正':'+',
                        '负':'-',
                        '点':'.'
     }

     if text.encode('utf8') in chineseDictionary:
         chineseNum = True
         #print "?~~~~ " + numString
         numString += text

         #print "what %s" %(numString)

     return text,numString,chineseNum


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def processChinese(text):
    #print "text: " +text
    if is_number(text):
        return text
    num =0
    ans=''
    basic = 0
    method = '*'
    textArray =text.split('点'.decode('utf8'))

    chineseDictionary = {'零': 0,
                         '一': 1,
                         '二': 2,
                         '两': 2,
                         '三': 3,
                         '四': 4,
                         '五': 5,
                         '六': 6,
                         '七': 7,
                         '八': 8,
                         '九': 9,
                         '十': 10,
                         '百': 100,
                         '千': 1000,
                         '万': 10000,
                         '亿': 100000000
                         }
    for index,textPart in enumerate(textArray):
        num = 0
        digit_number=""
        for letter in textPart:
            letter =letter.encode('utf8')

            if letter.isdigit()==False:
                if digit_number != "":
                    basic = int(digit_number)
                    digit_number=""

                if letter=='点':
                    continue
                curNum = chineseDictionary[letter]

                if curNum<10:

                    if curNum == 0:
                        method='+'
                    else:
                        basic = curNum
                else:
                    #print "ok: " + str(basic)+" "+ str(curNum)
                    if basic !=0:
                        num += basic*int(curNum)
                        basic =0
                    elif num!=0:
                        num += basic * int (curNum)
                    else:
                        num = num*curNum
                    #print "num: " + str(num)
            else:
                digit_number+=letter

        if basic != 0:
            num += basic
        ans+=str(num)
        if index!=len(textArray)-1:
            ans+='.'

    #print "ans: "   +ans
    return ans



# def find_number(text):
#     ans = []
#     bytePosition = 0;
#     startPosition = 0;
#     endPosition = 0;
#     isContinue = 0
#     number = ""
#     #check = False
#     #mystring = ""
#
#     for letter in text:
#
#         letter=letter.encode('utf8')
#         letter = checkDigitArabic(letter)
#         letter = checkDigitChinese(letter,'')
#         if letter.isdigit(): # if the char is int
#             number += letter # append to the buffer string
#
#             if isContinue == 0: #starting position of the number
#                 startPosition = bytePosition
#
#             isContinue = True
#
#         elif (letter ==".") or (letter==","):
#                 if number != "":
#                     number+=letter
#                     isContinue = 1
#                 else:
#                     isContinue =0
#
#
#         else:
#             if isContinue == 1:
#                 endPosition = bytePosition
#                 if "," in number:
#                     saparateNum = number.split(",")
#                     buffer=""
#                     for i in range(0, len(saparateNum)-1, 1):
#                         buffer += saparateNum[i]
#                     if len(saparateNum[len(saparateNum)-1]) <3:
#
#                         buffer+="."
#                     buffer+=saparateNum[len(saparateNum)-1]
#                     number = buffer
#
#                 if (isIntegre(number)):
#                     newTuple = numberTuple(number, startPosition, endPosition)
#                     ans.append (newTuple)
#
#                 number = ""
#                 startPosition = 0
#                 endPosition = 0
#             isContinue = 0
#
#         bytePosition += 1
#
#     #print mystring
#     if number != "":
#         newTuple = numberTuple (number, startPosition, endPosition)
#         ans.append (newTuple)
#
#     return ans


def check_vietnamese(text):
    ans=""
    arr =text.split(".")
    ans+=arr[0]
    for text in arr[1:]:
        if text=="000":
            ans+=","
        else:
            ans+="."
        ans+=text
    return ans



def check_Punjabi(text):

    if text.encode("utf-8") == '٬':
        return ','
    else:
        return text


def check_end_poing(text,endposition):
    if text.endswith('.'):
        text = text[:-1]
        endposition-=1
    return text,endposition




def get_letter_arabic(text):
    ans = []
    bytePosition = 0;
    startPosition = 0;
    endPosition = 0;
    isContinue = 0
    number = ""
    numString = ''
    chineseNum = False
    for letter in unicode(text,"utf-8"):


        letter = checkDigitArabic(letter)
        numString = number
        letter,numString,chineseNum = checkDigitChinese(letter,numString)
        letter = check_Punjabi(letter)
        if letter.isdigit() or chineseNum : # if the char is int
            number += letter # append to the buffer string

            if isContinue == 0: #starting position of the number
                startPosition = bytePosition

            isContinue = True

        elif (letter ==".") or (letter==","):

                if number != "":
                    number+=letter
                    isContinue = 1
                else:
                    isContinue =0


        else:
            if isContinue == 1:
                endPosition = bytePosition
                if "," in number:
                    saparateNum = number.split(",")
                    buffer=""
                    for i in range(0, len(saparateNum)-1, 1):
                        buffer += saparateNum[i]
                    if len(saparateNum[len(saparateNum)-1]) <3:

                        buffer+="."
                    buffer+=saparateNum[len(saparateNum)-1]
                    number = buffer
                #print number
                number=processChinese(number)
                if (isIntegre(number)):
                    number,endPosition=check_end_poing(number,endPosition)
                    #print number
                    newTuple = numberTuple(number, startPosition, endPosition)
                    ans.append (newTuple)

                number = ""
                startPosition = 0
                endPosition = 0
                numString=''
            isContinue = 0

        bytePosition += 1

    #print mystring
    print "len: " + str(len(ans))
    if number != "":
        newTuple = numberTuple(number, startPosition, endPosition)
        ans.append(newTuple)

    return ans






if __name__ == '__main__':

        #filename = sys.argv[1]
        filename = "ar.txt"

        #filename = "input.txt"
        text = open (filename, 'r').read()
        #text= codecs.open (filename, 'r', encoding="utf-8")

        #ans = find_number(text)
        #ans = get_letter_arabic(text)
        for letter in unicode(text,"utf-8"):
            print letter
            print letter.encode("utf-8")
        #unicodeValue = int(text)
        #print unicodeValue

        # f = open('output.txt', 'w')
        #
        # for tuple in ans:
        #     print tuple
        #     f.write(str(tuple.content)+"\t"+str(tuple.start)+"\t"+str(tuple.end))





