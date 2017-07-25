import re
# import numpy
# #from difflib import SequenceMatcher
# import difflib
import baselineSystem

one = {}
two = {}
three = {}
four = {}
five = {}
six = {}
seven = {}
eight = {}
nine = {}
ten = {}


def isIntegre(i):

    # if not hasattr(isIntegre, '_re'):
    #     isIntegre._re = re.compile(r"[-+]?\d+(\.0*)?$")
    # return isIntegre._re.match(str(i)) is not None
    try:
        float (i)
        return True
    except ValueError:
        return False


def read_numbers():
    matrix = []
    cur =0
    myArr = []
    numbers = []
    nameArry =[]
    with open ("lib/numbers/numbers.txt") as f:
        for line in f:
            myArr = []
            if "@" in line:
                continue
            if line.isspace():
                continue
            if '#' in line:
                for word in line.split ("\t"):
                    if '#' in word:
                        continue
                    word = word.replace("\n","")
                    myArr.append (word)
            else:
                for word in line.split("\t"):
                    if not isIntegre(word):
                        myArr.append(word)
                    else:
                        if word not in numbers:
                            numbers.append(word)

            if "#" in line:
                nameArry = myArr


            else:
                myArr = filter (None, myArr)
                matrix.append(myArr)
                #print len (myArr)




    f.close()

    fname = "lib/numbers/14languages.txt"
    open (fname, 'w').close ()

    # print len(matrix)
    # print len (matrix[0])
    for j in range(0,len(matrix[0]),1):
         name = "#"+ "\t" +nameArry[j]
         write_to_file (name, fname)
         for i in range(0,len(matrix),1):

             name="::::" +"\t" +str(i)+"\t"+"::::" +"\t"+ matrix[i][j]
             print name
             write_to_file (name, fname)

    #
    #
    # write_to_file (numberStr, fname)

def read_1_to_100():

    one2hundred ={}
    fname = "lib/numbers/14languages.txt"
    hundredNum =[]
    name = ""
    with open (fname) as f:
        for line in f:
            line =line.strip("\n")
            if line.isspace():
                continue
            if not line:
                continue
            if "#" in line:
                line = line.strip ("#")
                line = line.strip ("\t")
                line=line.lower()

                if name == "":
                    name = line
                    continue


                one2hundred[name] =hundredNum
                name = line
                hundredNum = []
            else:
                line = line.replace("\t","")
                arr = line.split("::::")
                hundredNum.append(arr[2])
    return one2hundred
#
#
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

def LevenshteinDistance(s,len_s,t,len_t):

  cost = 0
  if len_s == 0 :
    return len_t
  if len_t ==0:

    return len_s

  if (s[len_s-1] == t[len_t-1]):
      cost = 0
  else:
      cost = 1


  return min(LevenshteinDistance(s, len_s - 1, t, len_t    ) + 1,
                 LevenshteinDistance(s, len_s , t, len_t - 1) + 1,
                 LevenshteinDistance(s, len_s - 1, t, len_t - 1) + cost)



def read_dictionary_and_check(numberStr,language):

    get_spelled_out_dic()
    filename = "lib/numbers/1000.txt"
    thousand = read_over100(filename)
    filename = "lib/numbers/million.txt"
    million  = read_over100(filename)
    filename = "lib/numbers/billion.txt"
    billion  = read_over100(filename)
    filename = "lib/numbers/hundred.txt"
    hundred  = read_over100(filename)
    one2hunderd = read_1_to_100()
    lang = language.strip("\n").lower()

    print lang
    my_list = [one, two, three, four, five, six, seven, eight, nine,hundred,thousand,million,billion]
    digit_list = [1,2,3,4,5,6,7,8,9,100,1000,1000000,1000000000]

    if one2hunderd.has_key(lang):
        numberList = one2hunderd[lang]
        #print numberList

        for count,number in enumerate(numberList):
            if numberStr == number:
                print numberStr
                return count


    for count in range(len(my_list)-1,-1,-1):
        nameDic = my_list[count]
        for key, value in nameDic.items():
            if lang in key.lower():
                #print "key: %s value: %s, num:%s " %(key,value,digit_list[count])
                # print numberStr.decode('utf-8')
                # print value.decode('utf-8')
                if numberStr.lower().decode('utf-8') == value.lower().decode('utf-8'):
                    print 182
                    return digit_list[count]
    print 184
    return None


def process_num(numberStr,language):
    wholeWord = read_dictionary_and_check (numberStr, language)
    if wholeWord != None:
        return wholeWord

    numArr = numberStr.split()
    process_numArr = []
    for num in numArr:
        number = read_dictionary_and_check(num,language)
        if number != None:
            process_numArr.append(number)
            continue
        number = process_single_num(num,language)
        process_numArr.append(number)
    print numArr
    print process_numArr
    returnValue =0
    bufferValue = process_numArr[0]
    #i = 1
    for i in range(1,len(process_numArr),1):
    #while (i< len(process_numArr)):
        if process_numArr[i] == "connect":
            returnValue += bufferValue
            bufferValue = 0
            continue
        #print "bv: %d rv:%d" %(bufferValue,returnValue)

        if process_numArr[i] < process_numArr[i-1]:
            returnValue += bufferValue
            bufferValue = process_numArr[i]
        else:
            bufferValue *=process_numArr[i]

        #print "bv: %d rv:%d" % (bufferValue, returnValue)

    returnValue += bufferValue
    print returnValue
    return  returnValue











def process_single_num(numberStr,language):

    if len(numberStr) ==1:
        return "connect"
    numStr = numberStr
    get_spelled_out_dic()
    filename = "lib/numbers/1000.txt"
    thousand = read_over100(filename)
    filename = "lib/numbers/million.txt"
    million  = read_over100(filename)
    filename = "lib/numbers/billion.txt"
    billion  = read_over100(filename)
    filename = "lib/numbers/hundred.txt"
    hundred  = read_over100(filename)
    one2hunderd = read_1_to_100()
    lang = language.strip("\n").lower()

    my_list = [billion,million,thousand,hundred,nine,eight,seven,six,five,four,three,two,one]
    #my_list = [one, two, three, four, five, six, seven, eight, nine,hundred,thousand,million,billion]
    #digit_list = [1,2,3,4,5,6,7,8,9,100,1000,1000000,1000000000]
    digit_list = [1000000000,1000000,1000,100,9,8,7,6,5,4,3,2,1]
    if one2hunderd.has_key(lang):
        numberList = one2hunderd[lang]
        #print numberList

        for count,number in enumerate(numberList):
            if numberStr == number:
                return count

    similarity = 100
    potentialDigit = 1
    potentialZeros = 1
    fixedCount = False
    arr=[]
    fixedPotentialZero=-1
    #for count,nameDic in enumerate(my_list):
    for count in range(0,13,1):
    #for count in range(len(my_list)-1,-1,-1):
        nameDic = my_list[count]
        for key, value in nameDic.items():
            if lang in key.lower():
                #print "key: %s value: %s, num:%s numstr:%s" % (key, value, digit_list[count],numStr)
                if numStr.decode('utf-8') == value.decode('utf-8'):
                    return digit_list[count]
                else:
                    if count >3:
                        if count == 4:
                            fixedCount = False
                            similarity = 100
                        if fixedCount:
                            continue

                        if (numStr in value) or (value in numStr):
                            potentialDigit = digit_list[count]
                            fixedCount = True
                            continue
                        cur = LevenshteinDistance(numStr,len(numStr),value,len(value))
                        # ld =LevenshteinDistance(numberStr,len(numberStr),value,len(value))
                        #print "key: %s value: %s, num:%s " % (key, value, digit_list[count])
                        #print "cur: %d numStr: %s" %(cur,numberStr)
                        if cur < similarity:

                            similarity = cur
                            potentialDigit = digit_list[count]
                    else:
                        # if count==9:
                        #     fixedCount = False
                        if fixedCount:
                            continue
                        if (numStr in value) or (value in numStr):
                            potentialZeros = digit_list[count]
                            print "?"

                            if numStr in value or LevenshteinDistance(numStr,len(numberStr),value,len(value)) ==1:
                                print "value: %s" %(value)
                                potentialZeros = digit_list[count]
                                fixedPotentialZero = potentialZeros
                            fixedCount = True
                            #numStr = numberStr.split(value, 1)[0]
                            #print numStr
                            continue
                        cur = LevenshteinDistance(numberStr,len(numberStr),value,len(value))
                        # print "key: %s value: %s, num:%s " % (key, value, digit_list[count])
                        # print numberStr.decode ('utf-8')
                        # print "cur: %d numStr: %s" %(cur,numberStr)
                        if cur < similarity:
                            similarity = cur
                            potentialDigit = digit_list[count]

    if fixedPotentialZero !=-1:
        potentialZeros =fixedPotentialZero
        potentialDigit=1
    print "pd: %d" %(potentialDigit)
    print "pz: %d" % (potentialZeros)
    return potentialDigit * potentialZeros








def read_file():
    name=""
    with open ("lib/digits.txt") as f:
        for line in f:
            #print "??" + line
            if line == "":
                #print "1"
                continue
            if len(line.split())==1:
                name = line
                continue
            if line == '\n':
                continue
            numberStr=""
            numArr =line.split("\t")
            for count,word in enumerate(line.split("\t")):
                #print "3"
                if count==0:
                    if word=="written":
                        write_to_file("# "+name+" "+word,'lib/scripts.txt')
                    else:
                        write_to_file ("# "+ word,'lib/scripts.txt')
                    name = word
                elif word == "":
                    numberStr+=" :::: NONE"
                else:

                    word=replace_notation(word,numArr)
                    word=get_special_character(word)
                    numberStr+=" :::: " +word
            print numberStr
            write_to_file(numberStr,'lib/scripts.txt')

def replace_notation(word,numArr):
    ans=word
    if "[1]" in ans:
        ans = ans.replace("[1]",numArr[1])
    if "[2]" in ans:
        ans = ans.replace ("[2]", numArr[2])
    if "[3]" in ans:
        ans = ans.replace ("[3]", numArr[3])
    if "[4]" in ans:
        ans = ans.replace ("[4]", numArr[4])
    if "[5]" in ans:
        ans = ans.replace ("[5]", numArr[5])
    if "[6]" in ans:
        ans = ans.replace ("[6]", numArr[6])
    if "[7]" in ans:
        ans = ans.replace ("[7]", numArr[7])
    if "[8]" in ans:
        ans = ans.replace ("[8]", numArr[8])
    if "[9]" in ans:
        ans = ans.replace ("[9]", numArr[9])
    if "[10]" in ans:
        ans = ans.replace ("[10]", numArr[10])
    return ans



def get_special_character(word):
    ans = word
    ans = re.sub("[\(\[].*?[\)\]]", "", ans)
    return ans

def write_to_file(text,filename):
    f = open(filename, 'a+')
    f.write(text+"\n")
    f.close()

def read_over100(filename):
    dic = {}

    with open (filename) as f:
        for line in f:
            line = line.replace ("\n", "")
            if "@" in line:
                continue
            if line.isspace():
                continue
            if not line:
                continue
            arr = line.split("\t")
            dic[arr[0].lower()] =arr[1]
    return dic

def get_spelled_out_num(text):
    #print text
    my_list=[one,two,three,four,five,six,seven,eight,nine]
    for count,name in enumerate(my_list):
        #if text.encode("utf-8") in name:
        if text.lower() in name:
            print "num: %s, %d" %(text,count+1)
            return str(count+1)
    return text

def get_spelled_out_dic():

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
                #line =re.sub(r'\# .*?\# ','',line)
                arr = line.split("#")
                if len(arr) != 3:
                    continue
                my_lists[name][arr[1].lower()]= arr[2].strip(" ")
                #my_lists[name].append(line)
            #my_lists[name] = f.read().replace('\n', '')

def get_digit():
    name = ""
    dicName = ["one","two","three","four","five","six","seven","eight","nine","ten"]
    with open ("lib/scripts.txt") as f:
        for line in f:

            if "#" in line:
                name= line.strip('\n')
                continue
            if line == "":
                continue
            if line == '\n':
                continue
            for count,word in enumerate(line.split(" :::: ")):
                if count == 0:
                    continue
                if count > 10:
                    print line +" error !!!!"
                    continue
                if word != "NONE" or "":
                    filename = "lib/digits/"+dicName[count-1]+".txt"
                    print filename
                    wordStr = word
                    write_to_file(wordStr,filename)


def read_numberStr(filename):
    with open (filename) as f:
         language = f.readline().strip("\n")
         spelledOutNum = f.readline().strip("\n")

         correct_ans = f.readline().strip("\n")
    ans = process_num (spelledOutNum, language)
    print ans
    print correct_ans
    if ans == int(correct_ans):
        print "correct"
    else:
        print "wrong"






if __name__ == '__main__':
    #read_1_to_100()
    #get_digit()
    #read_numbers()

    filename = "lib/test.txt"

    read_numberStr (filename)

    # numberStr ="cent"
    # language = "french"
    # print read_dictionary_and_check(numberStr,language)
    #print process_single_num (numberStr, language.lower())
    # s = "tress"
    # t = "tres"
    # len_s = len(s)
    # len_t = len(t)
    # print LevenshteinDistance(s,len_s,t,len_t)
