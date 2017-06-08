
from Geometry import GeoPolygon

class GroundTruthPolygon(GeoPolygon.GeoPolygon):

    def __init__(self, id,location, word, phrase, points):
            self.id = id
            self.location = location
            self.phrase = phrase
            GeoPolygon.GeoPolygon.__init__(self, points, word)
            self.related_words = []
            self.test = []

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