
from Geometry import GeoPolygon

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class GroundTruthPolygon(GeoPolygon.GeoPolygon):

    def __init__(self, id,location, word, phrase, points):
            self.id = id
            self.location = location
            self.phrase = phrase
            GeoPolygon.GeoPolygon.__init__(self, points, word)
            self.related_words = []
            self.test = []
            self.associated_polygon=[]

    def __str__(self):
        string = "The text is : " +self.word + "\n"
        # coordinates = self.polygon.exterior.coords
        # string  += ",".join("(%s,%s)" % tup for tup in coordinates)

        return string

    def add_related_word(self,gt):
        self.related_words.append(gt)

    def get_area_per_letter(self):
        num = len(self.word)
        #print str(self.id) +" " + self.word
        #print self.get_area()
        area = self.get_area() /num

        return area
        #print self.get_area()


    def same_captial(self,gt):

        if self.word.islower():
            mode_1 = "lowercase"
        elif self.word.isupper():
            mode_1 = "uppercase"
        else:
            mode_1 = "mix"


        if gt.word.islower():
            mode_2 = "lowercase"
        elif gt.word.isupper():
            mode_2 = "uppercase"
        else:
            mode_2 = "mix"

        if mode_1 == mode_2:
            return True
        elif is_number(self.word) or is_number(gt.word):
            return True
        else:
            return False