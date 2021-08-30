import requests
import re
import os
import numpy as np
import streetview.tiles as tiles

def _panoid_url(lat, lon):
    """
    Builds the URL that gives the closest
    panorama ID to the given coordinates.
    
    _panoid_url() DOES NOT GIVE the panorama ID.
    """
    url = "https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{0:}!4d{1:}!2d50!3m18!2m2!1sen!2sUS!9m1!1e2!11m12!1m3!1e2!2b1!3e2!1m3!1e3!2b1!3e2!1m3!1e10!2b1!3e2!4m6!1e1!1e2!1e3!1e4!1e8!1e6&callback=_xdc_._clm717"
    return url.format(lat, lon)

def getpanoID(lat, lon):
    """
    Returns the closest panorama ID alongside with the coordinates.
    """
    json = requests.get(_panoid_url(lat, lon)).text
    pans = re.findall(r'\[[0-9]-?,"(.+?)"].+?\[\[null,null,([0-9]+.[0-9]+),(-?[0-9]+.[0-9]+)', json) # i swear this is gonna break at some point
    pan = {                                                                                        # buuut it works for now so whatever
        "pano_id": pans[0][0],
        "lat": pans[0][1],
        "lon": pans[0][2]
    }                                                                                  
    return pan
    
def download_panorama(panoID, zoom=4, keep_tiles=False): 
    
    # Downloads the tiles
    current_tile = 0
    max_x, current_x = 13, 0
    max_y, current_y = 5, 0
    tile_array=np.full([max_y, max_x], None)
    # print(tile_array)

    while True:
        for i in range(current_y, max_y):
            # print(current_y)
            for i in range(current_x, max_x):
                tiles.download_tile(panoID, current_x, current_y, current_tile, zoom)
                # print(current_x, current_y)
                tile_array[current_y, current_x] = (f"tile{current_tile}.png")
                # print(tile_array)
                current_tile += 1
                current_x += 1
            current_x = 0
            current_y += 1
        break
    
    # Merges the tiles
    tiles._stichTiles(tile_array)
    
    if keep_tiles is False:
        for i in range(len(tile_array)):
            for f in tile_array[i]:
                os.remove(f)
    else:
        pass

if __name__ == "__main__":
    import tiles
    lat = 6.237965431428744
    lon = -75.6095178872445
    pan = getpanoID(lat, lon)
    print(pan['pano_id'])