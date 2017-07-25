import psycopg2
from shapely import wkb
from shapely.geometry import LineString
from shapely.geometry import Polygon
from Geometry import GeoPolygon

def connect_db(gt_list):
    DBname = 'postgres'
    my_user = 'postgres'
    pw = 'root'

    conn = psycopg2.connect(dbname=DBname, user=my_user, password=pw)
    curs = conn.cursor()


    curs.execute("CREATE TABLE IF NOT EXISTS USGS60("
                 "id INT PRIMARY KEY NOT NULL,"
                 "word CHAR(300) NOT NULL,"
                 "phrase CHAR(300) NOT NULL, "
                 "polygon geometry(Polygon,4326) "
                 ")")

    for gt in gt_list:
        poly  = gt.polygon
        curs.execute(
            'INSERT INTO USGS60(word, phrase,polygon)'
            'VALUES (%(word)s,%(phrase)s,ST_SetSRID(%(geom)s::geometry))',
            {'word': gt.word, 'phrase': gt.phrase,'geom':poly.wkb_hex, 'srid': 4326})

    conn.commit()

    curs.execute('SELECT word, geom FROM USGS60')
    for word, geom_wkb in curs:
        geom = wkb.loads(geom_wkb, hex=True)
        print('{0}: {1}'.format(name, geom.wkt))

if __name__ == '__main__':

    conn = psycopg2.connect("dbname=postgres user=postgres password=root")
    curs = conn.cursor()

    # Make a Shapely geometry
    ls = LineString([(2.2, 4.4, 10.2), (3.3, 5.5, 8.4)])
    ls.wkt  # LINESTRING Z (2.2 4.4 10.2, 3.3 5.5 8.4)
    ls.wkb_hex  # 0102000080020000009A999999999901409A999999999911406666666666662440666666...

    # Send it to PostGIS
    curs.execute('CREATE TEMP TABLE my_lines(geom geometry, name text)')
    curs.execute(
        'INSERT INTO my_lines(geom, name)'
        'VALUES (ST_SetSRID(%(geom)s::geometry, %(srid)s), %(name)s)',
        {'geom': ls.wkb_hex, 'srid': 4326, 'name': 'First Line'})

    conn.commit()  # save data

    # Fetch the data from PostGIS, reading hex-encoded WKB into a Shapely geometry
    curs.execute('SELECT name, geom FROM my_lines')
    for name, geom_wkb in curs:
        geom = wkb.loads(geom_wkb, hex=True)
        print('{0}: {1}'.format(name, geom.wkt))