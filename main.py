import random
import flag
import tweepy
import configparser
import json
import sv_dlp
from shapely.geometry import shape, Point
import sys, os

ABB = ["AU", "JP", "KH", "KR", "MY", "NZ", "PH", "RU", "SG", "TH", "TR", "TW"]
EEE = ["AL", "AT", "BE", "BG", "CH", "CZ", "DK", "ES", "EE", "FI", "FR", "GB", "GR", "HR", "HU", "IE", "IS", "IT", "LT", "LV", "ME", "NL", "NO", "PL", "PT", "RO", "RS", "SK", "SI", "SE", "UA", "VA"]
FFF = ["AE", "IL", "LS", "SZ", "ZA"]
NNN = ["CA", "MX", "US", "GT"]
SRR = ["AR", "BR", "CL", "CO", "EC", "PE", "UY"]

# Config file setup
config = configparser.ConfigParser()
ConfigFile = ('config.cfg')
config.read(ConfigFile)

# Api Keys
twtAPI_KEY = config['Twitter API Keys']['api_key']
twtAPI_SECRET = config['Twitter API Keys']['api_secret']
twtTOKEN_ACCESS = config['Twitter API Keys']['token_access']
twtSECRET_TOKEN = config['Twitter API Keys']['secret_token']
twtAuth = tweepy.OAuthHandler(twtAPI_KEY, twtAPI_SECRET)
twtAuth.set_access_token(twtTOKEN_ACCESS, twtSECRET_TOKEN)
twtAPI = tweepy.API(twtAuth)

def tweet(img, content):
    twtAPI.update_status_with_media(status=content, filename=img)

def readBorderFile(file):
    with open(file, "r") as file:
        data = json.loads(file.read())
    return data
    
def getCountryData(COUNTRY_CODE, GEO_JSON):
    for COUNTRY in GEO_JSON['features']:
        if COUNTRY['properties'].get('country') is not None:
            continue
        
        if COUNTRY['properties']['code'] == COUNTRY_CODE:
            return {
                "Country": COUNTRY['properties']['name'],
                "Geometry": COUNTRY['geometry']
            }
    return None

def generateRandomPointInPolygon(polygon):
    # Get the bounding box of the polygon
    bounds = polygon.bounds
    while True:
        # Generate random longitude and latitude values within the polygon bounding box
        lon, lat = bounds[0] + random.random()*(bounds[2]-bounds[0]), bounds[1] + random.random()*(bounds[3]-bounds[1])
        point = Point(lon, lat)
        # Check if the point is within the polygon
        if polygon.contains(point):
            return [round(lat, 6), round(lon, 6)]

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

if __name__ == '__main__':
    sv_dlp = sv_dlp.sv_dlp()
    GEO_JSON = readBorderFile("borders.json")

    while True:
        COUNTRY_CODE = random.choice(random.choice([ABB, EEE, FFF, NNN, SRR]))
        print(COUNTRY_CODE)
        COUNTRY_DATA = getCountryData(COUNTRY_CODE, GEO_JSON)
        if COUNTRY_DATA == None: continue
        else: break
    
    print(f"Finding {COUNTRY_DATA['Country']}...")      
    while True:
        try:
            with HiddenPrints():
                lat, lng = generateRandomPointInPolygon(shape(COUNTRY_DATA["Geometry"]))
                pano_id = sv_dlp.get_pano_id(lat=lat, lng=lng)
            break
        except Exception:
            pass
    
    flag_emoji = flag.flag(COUNTRY_CODE)
    panorama_url = sv_dlp.short_url(sv_dlp.pano_id)
    tweet_content = f"{flag_emoji} {COUNTRY_DATA['Country']} - {sv_dlp.metadata.date.year}/{sv_dlp.metadata.date.month}\n{panorama_url}"
    
    img, tile_imgs = sv_dlp.download_panorama(pano_id, zoom=2)
    sv_dlp.postdownload.save_panorama(img=img, metadata=sv_dlp.metadata)
    
    print("Tweeting...")
    tweet(f"{sv_dlp.pano_id}.png", tweet_content)