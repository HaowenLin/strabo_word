from Evaluation.database import connect_db
from Geometry.GroundTruthPolygon import GroundTruthPolygon
from Geometry import GeoPolygon
import operator
import itertools
from operator import itemgetter
import json, math, sys
import itertools

def load_json_file(filename):
    plain_text = open(filename).read()

    # Make the plain text can be recognized by the json module.
    plain_text = plain_text.replace(',}', '}')
    plain_text = plain_text.replace(',]', ']')
    plain_text = plain_text.replace('}]}]}', '}]}')
    plain_text = " ".join(plain_text.split("\n"))
    plain_text = plain_text.replace("\\", "")

    # print ("text " + plain_text)
    data = json.loads(plain_text)
    return data


def get_ground_truth_list(gt_obj):
    gt_list = []

    for feature in gt_obj['features']:
        new_gt_rect = GroundTruthPolygon(feature['properties']['id'], feature['properties']['txt_loc'],
                                         feature['properties']['text'],
                                         feature['properties']['phrase'], feature['geometry']['coordinates'][0])

        gt_list.append(new_gt_rect)

    print "this file totaly has %d polygons\n" % (len(gt_list))

    return gt_list


# get all unique word phrases text in one shapfile
def get_all_phrases(gt_obj):
    word_list = set()

    for feature in gt_obj['features']:
        word_list.add(feature['properties']['Text'].lower())

    print len(word_list)
    file = open("phrases.txt", "w")

    for word in word_list:
        file.write(word)
        file.write("\n")

    file.close()


def process_letter_size(gt_list):
    gt_dictionary = {}

    for gt in gt_list:
        key = gt.phrase
        if key not in gt_dictionary:
            gt_dictionary[key] = []
        gt_dictionary[key].append(gt)

    max_word_pairs = []

    for key in gt_dictionary:
        gt_arr = gt_dictionary[key]
        print 'Key: {} Numer: "{}!"'.format(key, len(gt_arr))
        max_diff = 0.0
        max1 = gt_arr[0]
        max2 = gt_arr[0]

        for gt1, gt2 in itertools.combinations(gt_arr, 2):
            gt1_area = gt1.get_area_per_letter()
            gt2_area = gt2.get_area_per_letter()
            if max_diff < abs(gt1_area - gt2_area):
                max_diff = abs(gt1_area - gt2_area)
                max1 = gt1
                max2 = gt2
        cur_tuple = (max1, max2, max_diff)
        if max1 != max2:
            print max1.word + " " + max2.word + " " + str(max1.get_area_per_letter()) + " " + str(
                max2.get_area_per_letter()) + " " + str(max_diff)
        max_word_pairs.append(cur_tuple)



        # print 'Word1:{} Word2: {} Size: {} Diff:{}'.format(gt1.word, gt2.word, gt1.get_area_per_letter(), abs(gt1.get_area_per_letter() - gt2.get_area_per_letter()))
        # for pair in max_word_pairs:

        # print 'Word1:{} Word2: {} Size: {} Diff:{}'.format(pair[0].word, pair[1].word, pair[0].get_area_per_letter(), pair[3])


def filter_coordinates(text):

    if not text.endswith("'"):
        return False
    text=text.strip("'")
    arr = text.split("°")
    if len(arr) != 2:
        return False
    if arr[0].isdigit() and arr[1].isdigit():
        return True
    else:
        return False



def filter_function(gt_list):
    filtered_list = []
    for gt in gt_list:
        #if "." in gt.word:
            #continue
        filtered_list.append(gt)
    return filtered_list


def get_gold_data_phrases(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    return content


def get_nearest_neighboar(gt_list):

    for i in range(0, len(gt_list), 1):
        for j in range(i + 1, len(gt_list), 1):
            num = gt_list[i].calculate_polygon_distabce(gt_list[j])
            tuple1 = (num, gt_list[j])
            tuple2 = (num, gt_list[i])
            gt_list[i].test.append(tuple1)
            gt_list[j].test.append(tuple2)

        gt_list[i].test.sort(key=lambda tup: tup[0])
    return gt_list


def get_associated_polygon(gt_list):

    for gt in gt_list:
        #if "." in gt.word:
            #continue
        if gt.word == gt.phrase:
            continue
        potential_array = itertools.islice(gt.test, 10)
        for candidate in potential_array:
            letter_size = max(candidate[1].get_area_per_letter() / gt.get_area_per_letter(),
                              gt.get_area_per_letter() / candidate[1].get_area_per_letter())
            if letter_size < 1.8 :
                if gt.same_captial(candidate[1]) and (not filter_coordinates(candidate[1])):
                    #if candidate[0]<min(gt.find_longest_line().length,candidate[1].find_longest_line().length)*5:
                        gt.associated_polygon.append(candidate[1])

    return gt_list


def print_difference(list1,list2):
    for i in range(1,len(list1),1):
        if len(list1[i].associated_polygon) ==len(list2[i].associated_polygon):
            continue
        print "the word is:%s" %list1[i].word
        #print diff(list1[i].associated_polygon,list2[i].associated_polygon)
        print diff(list2[i].associated_polygon, list1[i].associated_polygon)

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


def evaluation_result(gt_list):
    detected_polygon = 0
    correct_polygon = 0
    detected_correct = 0
    for gt in gt_list:
        print "the word is:%s   and the phrase is: " % gt.word, gt.phrase
        if gt.word == gt.phrase:
            correct_polygon += 0
        else:
            correct_polygon += len(gt.phrase.split(" "))-1

        detected_polygon += len(gt.associated_polygon)

        for polygon in gt.associated_polygon:

            if polygon.phrase == gt.phrase:
                detected_correct += 1
                print polygon.word + "     c"

            else:
                print polygon.word
        #print "detec_correct: %d   correct_polygon: %d" %(detected_correct, correct_polygon)
        print "\n"
    print "precision is: %f" % (float (detected_correct)/detected_polygon)
    print "recall is: %f" % (float (detected_correct)/correct_polygon)



if __name__ == '__main__':
    # groundTruthFile = sys.argv[1]
    groundTruthFile = '../usgs15_pa.geojson'
    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)



    gt_list=get_nearest_neighboar(gt_list)
    list1= get_associated_polygon(gt_list)

    #list2 = same_cap(gt_list)
    #print print_difference(list1,list2)
    evaluation_result(list1)







    # count = 0
    # c2=0
    # for gt in gt_list:
    #     index = 0
    #     index2=0
    #     gt.test.sort(key=lambda tup: tup[0])
    #     print "The word:  %s  The phrase: %s" % (gt.word,gt.phrase)
    #
    #     top = itertools.islice(gt.test, 10)
    #     for tuple in top:
    #         #print tuple[1].word + " "
    #         if tuple[1].phrase == gt.phrase:
    #             index+=1
    #         letter_size = max(tuple[1].get_area_per_letter()/gt.get_area_per_letter(),gt.get_area_per_letter()/tuple[1].get_area_per_letter())
    #         #print "the letter size is : %s" %(letter_size)
    #         if letter_size < 1.8:
    #             if gt.same_captial(tuple[1]) and tuple[0]<gt.find_longest_line().length*2:
    #             #if (gt.find_orientation(tuple[1])<15 or abs(gt.find_orientation(tuple[1])-180)<15) :
    #             #print tuple[1].word + " "+str(gt.find_orientation(tuple[1]))+"? "+str(abs(gt.find_orientation(tuple[1])-180))+"    "
    #                 print tuple[1].word
    #                 if tuple[1].phrase == gt.phrase:
    #                     index2 += 1
    #
    #     if index != len(gt.phrase.split())-1 and (len(gt.word.split())==1):
    #         #print "index: %d  word len: %d" %(index,len(gt.phrase.split())-1)
    #         print "not matching: %s  %s" %(gt.word,gt.phrase)
    #         count+=1
    #
    #     if index == len(gt.phrase.split())-1 and index2 != len(gt.phrase.split())-1 and (len(gt.word.split())==1):
    #         #print "index: %d  word len: %d" %(index,len(gt.phrase.split())-1)
    #         #print "letter size: %s  %s" %(gt.word,gt.phrase)
    #         c2 += 1
    #
    #     print "\n"
    #
    # print count
    # print c2

        # sorted_gt_list  =sorted(gt_list, key=lambda gt:gt.get_center_location())

















        # phrase_set=set()
        # phrase_dic={}
        # for index,gt in enumerate(sorted_gt_list):
        #     print gt.word +": " +gt.phrase +":  "+str(gt.get_center_location())
        #     if gt.phrase not in phrase_set:
        #         phrase_dic[gt.phrase]=index
        #         #print gt.word+" " +str(index)
        #     phrase_set.add(gt.phrase)
        #
        # num=0
        # for element in phrase_set:
        #     count =0;
        #     loc = phrase_dic[element]
        #     if sorted_gt_list[loc].word == sorted_gt_list[loc].phrase:
        #         continue
        #     i= loc
        #     while i< loc+30:
        #         if i< len(sorted_gt_list) and sorted_gt_list[i].phrase == element :
        #             count+=1
        #             loc =i
        #         i+=1
        #     if count < len(element.split()):
        #         print element
        #         num+=1
        #
        # print num
        # get_all_phrases(result_obj)



# soda spring TWO soda spring
