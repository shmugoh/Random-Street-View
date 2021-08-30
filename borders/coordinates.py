import shapefile 
import random
import borders.continents as continents

def _point_inside_polygon(x, y, poly):
    """
    Determines if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.
    http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def generate_random_coordinates():
    """
    Picks a random continent and country, then generates
    a random coordinate inside the country.
    """
    ShapeFile = "TM_WORLD_BORDERS-0.3.shp"
    sf = shapefile.Reader(ShapeFile, encoding="latin1")
    shapes = sf.shapes()
    while True:
        continent = random.choice([continents.ABB, continents.EEE, continents.FFF, continents.NNN, continents.SRR])
        nation = random.choice(continent)
        for i, record in enumerate(sf.records()):
            if record[2] == nation:
                # print(record[2], record[4])
                # print(shapes[i].bbox)
                min_lon, min_lat = shapes[i].bbox[0], shapes[i].bbox[1]
                max_lon, max_lat = shapes[i].bbox[2], shapes[i].bbox[3]
                borders = shapes[i].points
                break
        rand_lat = random.uniform(min_lat, max_lat)
        rand_lon = random.uniform(min_lon, max_lon) 

        # Checks if coordinate 
        # is inside polygon
        if _point_inside_polygon(rand_lon, rand_lat, borders):
            return rand_lat, rand_lon, nation
        else:
            continue

if __name__ == "__main__":
    generate_random_coordinates()