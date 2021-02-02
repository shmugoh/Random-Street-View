import os, random, sys, svDB
import shapefile, googlemaps, requests
import tweepy, configparser
from time import sleep 
from datetime import datetime
import pprint

import hashlib
import hmac
import base64
import urllib.parse as urlparse

ABB = ["AUS", "JPN", "KHM", "KOR", "MYS", "NZL", "PHL", "RUS", "SGP", "THA", "TUR", "TWN"]

EEE = ["ALB", "AUT", "BEL", "BGR", "CHE", "CZE", "DNK", "ESP", "EST" "FIN", "FRA", "GBR", "GRC", "HRV", "HUN", 
"IRL", "ISL", "ITA", "LTU", "LVA", "MNE", "NLD", "NOR", "POL", "PRT", "ROU", "SRB", "SVK", "SVN", "SWE", "UKR", "VAT"]

FFF = ["ARE", "ISR", "LSO", "SWZ", "ZAF"]

NNN = ["CAN", "MEX", "PRI", "USA"]
SRR = ["ARG", "BRA", "CHL", "COL", "ECU", "GTM", "MEX", "PER", "URY"]

## NATO Continents ISO 3166-1 alpha-3 Reserved Codes
## Countries with low presence/unofficial Street View presence are excluded; based on tests, some countries have also been excluded.
## TODO: Store the countries in a database instead

# Config file setup
config = configparser.ConfigParser()
configFile = ('config.cfg')
config.read(configFile)

# Api Keys
twtAPI_KEY = config['Twitter API Keys']['api_key']
twtAPI_SECRET = config['Twitter API Keys']['api_secret']
twtTOKEN_ACCESS = config['Twitter API Keys']['token_access']
twtSECRET_TOKEN = config['Twitter API Keys']['secret_token']
twtAuth = tweepy.OAuthHandler(twtAPI_KEY, twtAPI_SECRET)
twtAuth.set_access_token(twtTOKEN_ACCESS, twtSECRET_TOKEN)
twtAPI = tweepy.API(twtAuth)

gmapsAPI_KEY = config['Google API Keys']['api_key']
gmapsSIGNING_KEY = config['Google API Keys']['signing_key']
gmaps = googlemaps.Client(gmapsAPI_KEY)

CurrentTry = int(config['Tries']['CurrentTry'])
MaximumTries = int(config['Tries']['MaximumTries'])

class c:
    okGreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    olors = '\033[0m'

def sumCount(c, a, b):
    c += 1
    config[a][b] = str(c)
    with open(configFile, 'w') as configfile:
        config.write(configfile)
    # Used to sum the current tries if an error occurrs.

def resetCount(a, b):
    c = 1
    config[a][b] = str(c)
    with open(configFile, 'w') as configfile:
        config.write(configfile)
    # Used to reset the tries if no error is found

def getTime():
    now = datetime.now()
    return now.strftime("%d/%m/%y %H:%M:%S")

def tweet(panorama, info):
    twtAPI.update_with_media(panorama, info)

def SavePanorama(url):
    response = requests.get(url)
    f = open("panorama.png", "wb")
    f.write(response.content)
    f.close()
    
def point_inside_polygon(x, y, poly):
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
# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
# http://www.ariel.com.au/a/python-point-int-poly.html

def hasStreetView(lat, lon):
    global gmapsAPI_KEY
    url = ("https://maps.googleapis.com/maps/api/streetview/metadata?location={},{}&radius=2000&key={}".format(lat, lon, gmapsAPI_KEY))

    metadata = requests.get(url).json()
    if metadata['status'] == "ZERO_RESULTS":
        return False, None
    elif metadata['status'] == "OK":
        if 'Google' not in metadata['copyright']:
            return False, None
        else:
            coords = (metadata['location']['lat'], metadata['location']['lng'])
            return True, metadata['pano_id'], coords
    else:
        return False, None
    # 0 = Boolean Expression; 1 = Panorama ID; 2 = Coordinates

def getCoords(coords):
    coordsArr = []
    reverse_geocodeJSON = gmaps.reverse_geocode((coords))
    y = len(coords)
    for x in range(y):
        try:
            coordsArr.append([reverse_geocodeJSON[x]['geometry']['bounds']['northeast']['lat'], reverse_geocodeJSON[x]['geometry']['bounds']['northeast']['lng']])
            coordsArr.append([reverse_geocodeJSON[x]['geometry']['bounds']['southwest']['lat'], reverse_geocodeJSON[x]['geometry']['bounds']['southwest']['lng']])
        except KeyError:
            return False
        except IndexError:
            return False
        
    return coordsArr, reverse_geocodeJSON
    # To get the latitude and longitude, please use 0; otherwise, to get more details such as unused coordinates and addreses, use 1.

print("Loading World Borders shape file...", end = '\r')
shape_file = "TM_WORLD_BORDERS-0.3.shp"
if not os.path.exists(shape_file):
    print(
        "Cannot find " + shape_file + ". Please download it from "
        "http://thematicmapping.org/downloads/world_borders.php and try again."
    )
    sys.exit()

sf = shapefile.Reader(shape_file, encoding="latin1")
shapes = sf.shapes()
## Loads the World Borders Shape Folder

if __name__=="__main__":
    while True:
        continent = random.choice([ABB, EEE, FFF, NNN, SRR])
        while True:
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
            ## Obtains a continent, then a nation and generates a random coordinate on that nation.
            ## Credit to hugovk for the portion of this code; learned a lot about this!

            ## Checks if coordinate is inside polygon
            if point_inside_polygon(rand_lon, rand_lat, borders):
                coords = (rand_lat, rand_lon)
                locations = gmaps.reverse_geocode((coords))
                place = getCoords(coords)

                if place is False:
                    print(f"{c.fail}%s - Cannot reverse geocode; repeating...{c.olors}" % (getTime()))
                    continue
                
                for i in range(len(place[0])):
                    if i > len(place[0]) or i == len(place[0]):
                        hasPamID = False
                        break

                    pamID = hasStreetView(place[0][i][0], place[0][i][1])
                    hasPamID = pamID[0]
                    if hasPamID is True:
                        print("%s - Found panoramic ID; tweeting..." % (getTime()))
                        coords = place[0][i][0], place[0][i][1], i
                        # Gets the coordinates of the panoramic ID (coords[0] and coords[1]) and the JSON variable (coords[2])
                        JSON = place[1][i]
                        address = JSON['formatted_address']
                        lat = pamID[2][0]
                        lon = pamID[2][1]
                        coords = lat, lon
                        break
                    else:
                        print("Doesn't have panoramic ID, repeating...", end ='\r')
                        continue
            
                # try:
                #     print("%s - Got address %s; getting panorama ID and coordinates..." % (getTime(), place))
                # except IndexError:
                #     print(f"{c.fail}%s - No address found; repeating{c.olors}" % (getTime()))
                #     continue

                if hasPamID is True:
                    if svDB.FindPamID(pamID[1]):
                        print(f"{c.warning}%s - Pam ID already in DB; repeating...{c.olors}" % (getTime()))
                        continue
                        # sys.exit()
                    else:
                        print(f"{c.okGreen}%s - Got panorama ID %s, address %s, and coordinates %s; downloading image...{c.olors}" % (getTime(), pamID[1], address, (lat, lon)))
                        SavePanorama("https://maps.googleapis.com/maps/api/streetview?size=600x640&pano={}&fov=75&key={}".format(pamID[1], gmapsAPI_KEY))
                        print(f"{c.okGreen}%s - Got image; tweeting...{c.olors}" % (getTime()))
                        x = random.randrange(3, 5) # defines last digits to round coordinates
                        TweetContent = ("%s (%s, %s)" % (address, (round(lat, x)), (round(lon, x))))
                        # TweetContent = address, (round(lat, x)), (round(lon, x))
                        break
                elif hasPamID is False:
                    print("Generating new coordinate...")
                    print(f"{c.warning}%s - Coordinate doesn't have street view; repeating...{c.olors}" % (getTime()), end="\r")
                    continue
                break
            else:
                print(f"{c.warning}%s - Coordinate not in point; trying again...{c.olors}" % (getTime()), end="\r")
                continue
        
        while True:
            try:
                print("panorama.png", TweetContent)
                # tweet("panorama.png", TweetContent)
                resetCount('Tries', 'CurrentTry')
                break
            except tweepy.error.TweepError:
                if CurrentTry > MaximumTries or CurrentTry == MaximumTries:
                    print(f"{c.fail}%s - Cannot tweet anymore. Trying again in 15 minutes{c.olors}" % (getTime()))
                    sleep(60 * 15) 
                    break
                else:
                    sumCount(CurrentTry, 'Tries', 'CurrentTry')
                    CurrentTry = int(config['Tries']['CurrentTry'])
                    print(f"{c.fail}%s - Could not tweet. Trying again...{c.olors}" % (getTime()))
                    print(f"{c.fail}%s{c.olors}" % (TweepError))

        print(coords)
        svDB.createRow(pamID[1], address, str(coords))
        print("------------------------------------------------------------------------------",
        f"\n{c.okGreen} %s - Tweeted: Address = %s. Coordinates = %s. Panorama ID = %s{c.olors}" % (getTime(), address, coords, pamID[1]),
            "\n------------------------------------------------------------------------------")
        TimeToSleep = random.randrange(60, 75)
        print("%s - Next Tweet in %i minutes" % (getTime(), TimeToSleep))
        sleep(TimeToSleep * 60)
        continue

    # print("{}, {}".format(rand_lat, rand_lon))