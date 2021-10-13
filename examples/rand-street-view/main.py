import borders.coordinates
import borders.continents as continents
import random
import streetview.panorama
from webbrowser import open_new_tab
import threading

# streetview.panorama.download_panorama("L2rQfz_mcsmGyaZ_Ae2ogg")

def find_pan(country=random.choice(random.choice(continents.CCC))):
    for i in range(15):
        try:
            c = borders.coordinates.generate_random_coordinates(country)
            a = streetview.panorama.getpanoID(c[0], c[1])
            print(a)
            print(c[2])
            print(a['pano_id'])
            open_new_tab(f"https://www.google.nl/maps/@58.6502986,11.2959174,3a,90y,12.9h,88.82t/data=!3m5!1e1!3m3!1s{a['pano_id']}!2e0!3e11")
            # open_new_tab(f"https://streetviewpixels-pa.googleapis.com/v1/thumbnail?cb_client=maps_sv.tactile&it=1%3A1&rank=closest&panoid={a['pano_id']}&w=3072&h=2048&radius=10000&thumbfov=120")
            # streetview.panorama.download_panorama(a['pano_id'])
            break
        except IndexError:
            print(f"none {(c[2])} {i}")

def rand_coord(width=12000, height=7500):
    # pixelX = random.randrange(1, 12000)
    # pixelY = random.randrange(1, 7500)
    pixelX = 3202
    pixelY = 3285
    # latitude = (pixelY / (height / 180) - 90) /-1
    # longitude = pixelX / (width / 360) - 180
    
    latitude = (pixelY / (height / 237.4) - 70)/1
    longitude = pixelX / (width / 360) - 180
    open_new_tab(f"https://maps.google.com/?q={latitude},{longitude}")
    # latitude = parseFloat((((pixelY / (height / 180)) - 90) / -1).toFixed(1)),
    # longitude: parseFloat(((pixelX / (width / 360)) - 180).toFixed(1)),

# for i in range(30):
rand_coord()
    # country = random.choice(random.choice(continents.CCC))
    # find_pan(country)