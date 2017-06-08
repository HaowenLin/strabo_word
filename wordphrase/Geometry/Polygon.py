from Geometry import Line, Point
#from Geometry import GeoOperations
from shapely.geometry import LineString
import math, sys



class Polygon:
    def __init__(self, points):
        self.points = []
        self.lines = []

        x = y = 0


        if len(points) < 4: # add original point in the end, so the minimum point =4
            print "This polygon has less than 3 points"

        if points[0] != points[-1]:
            print  "This polygon end point != starting point"

        for count,point in enumerate(points):
            self.points.append(point)
            if len(self.points) > 1:
                self.lines.append(Line.Line(self.points[count-1], self.points[count]))


        #print len(self.lines)





    def __str__(self):
        string = ''
        for point in self.points:
            string = string + point.__str__() + "\n"
        return string

    def get_point_list(self):
        point_list = []
        for point in self.points:
            temp = [point.x, point.y]
            point_list.append(temp)
        return [point_list]

    def get_area(self):
        k = 0
        area = 0.0
        for i in xrange(len(self.points)-1):
            k += abs((self.points[i].x * self.points[i+1].y) - \
                (self.points[i].y * self.points[i+1].x))
        area = k / 2.0
        return area

    def scale(self, factor_w, factor_h):
        for point in self.points:
            point.x *= factor_w
            point.y *= factor_h

        self.lines = []

        for i in range(0, 3):
            self.lines.append(Line.Line(self.points[i], self.points[i+1]))

        self.lines.append(Line.Line(self.points[-1], self.points[0]))

    def get_xywh(self):
        xs = []
        ys = []

        for point in self.points:
            xs.append(math.fabs(point.x))
            ys.append(math.fabs(point.y))

            x = min(xs)
            y = min(ys)
            w = max(xs) - x
            h = max(ys) - y

        return (x, y, w, h)

    # def get_polygon_distance(self, poly2):
    #     # dist = sys.maxsize
    #     # [x1, y1, w1, h1] = self.get_xywh()
    #     # [x2, y2, w2, h2] = poly2.get_xywh()
    #     #
    #     # dist = math.fabs(x1 - x2)
    #     # dist = min(dist, math.fabs(x1 + w1 - x2))
    #     # dist = min(dist, math.fabs(x1 - x2 - w2))
    #     # dist = min(dist, math.fabs(x1 + w1 - x2 - w2))
    #     #
    #     # dist = min(dist, math.fabs(y1 - y2))
    #     # dist = min(dist, math.fabs(y1 + h1 - y2))
    #     # dist = min(dist, math.fabs(y1 - y2 - h2))
    #     # dist = min(dist, math.fabs(y1 + h1 - y2 - h2))
    #     dist = self.center.get_point_dist(poly2.center)
    #
    #     return dist


if __name__ == '__main__':

    p1 = Point.Point(0, 0)
    p2 = Point.Point(3, 0)
    p3 = Point.Point(1, 2)
    p4 = Point.Point(0.5, 2)


    p5 =Point.Point(1,1)
    #t1=[p1,p3,p2,p4,p1]

    t1=[p1,p2,p3,p4,p1]
    pol1 = Polygon(t1)
    #print pol1
    area = pol1.get_area()
    print area