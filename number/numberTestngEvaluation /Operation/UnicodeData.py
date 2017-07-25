# -*- coding: utf-8 -*-
import string

def check_hex_value(line):

    arr = line.split("\t")
    if arr[0]!="" and all (c in string.hexdigits for c in arr[0]):

        return arr[0]
    else:
        return -1
    #if line[0].isdigit() or line[0] in 'ABCDEF':

        #return line.split("\t")[0]



def store_category(category,start,end):
    if category != "":
        print category+" " +start+" " +end

        f= open("../lib/unicode_category.txt", 'a')
        f.write("::s " + start+ "::e "+end +"::c "+category)
        f.close()


def process_original_unicode():

    filename = "../lib/unicode.txt"

    hexValue=-1
    control=False
    start=-1
    end=-1
    category=""
    with open(filename) as f:
        for line in f:
            if control and check_hex_value(line) != -1:
                start = check_hex_value(line)
                control = False
            if check_hex_value(line) != -1:
                hexValue = check_hex_value(line)
            if line.startswith("@\t\t"):
                end = hexValue
                store_category(category,start,end)
                category =line.replace("@\t\t","")
                control=True


def get_code_and_name():
    filename = "../lib/unicode.txt"
    digit_list=['digit','numeral','number']
    f = open ("../lib/unicode_digit.txt", 'w')
    with open(filename) as file:
        for line in file:
            if check_hex_value (line) != -1:
                if "EGYPTIAN HIEROGLYPH" in line :
                    nextLine = nextLine = next(file)
                    if check_hex_value(nextLine)==-1:
                        line = line.replace("\n"," ")
                        nextLine = nextLine.replace("\t* ","")
                        nextLine = nextLine.replace (",", "")
                        if not any(c.isalpha() for c in nextLine):
                            line += nextLine
                            f.write (line)
                            print line
                            continue
                if "thousands separator" in line.lower():
                    f.write (line)
                for word in digit_list:
                    if word in line.lower():
                        print line
                        f.write (line)



    f.close ()
    file.close()


def get_english_digit():
    filename = "../lib/english_digit_ori.txt"
    f = open ("../lib/english_digit.txt", 'w')
    with open (filename) as file:
        for line in file:
            arr = line.split("\t")
            f.write (arr[0]+"\t"+arr[1]+"\n")


def test():
    s="𓆿"
    for l in unicode(s,"utf-8"):
        print hex(ord(l))


if __name__ == '__main__':
    get_code_and_name ()
    #test()


