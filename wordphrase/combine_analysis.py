

def get_gold_data_phrases(fname):

    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    print content
    return content



if __name__ == '__main__':

        get_gold_data_phrases("Evaluation/phrases.txt")