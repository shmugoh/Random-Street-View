import requests
import os

from PIL import Image
from io import BytesIO
import streetview.panorama as panorama

def _stichTiles(tile_array):

    print("pain")
    print(tile_array)
    # First phase
    rows_arr = []
    for i in range(len(tile_array)):
        try:
            images = [Image.open(x) for x in tile_array[i]]
        except AttributeError: # this is gonna kill the script at some point
            continue
        widths, heights = zip(*(i.size for i in images))
        total_width, max_height = sum(widths), max(heights)  
        new_im = Image.new('RGB', (total_width, max_height))

        y = 0
        for m in images:
            print(m.filename)
            if m == images[0]:
                new_im.paste(m, (0, 0))
            else:
                new_im.paste(m, (last_image.width*y, 0))
            last_image = m
            y += 1
            new_im.save(f'tilerow{i}.png')
        rows_arr.append(f'tilerow{i}.png')
        print("--------")

    # Second phase
    y = 0
    images = [Image.open(x) for x in rows_arr]
    print(len(images))
    height = images[0].height * len(images)
    merged_im = Image.new('RGB', (images[0].width, height))

    for r in images:
        if r == images[0]:
            # m.show()
            merged_im.paste(r, (0, 0))
        else:
            merged_im.paste(r, (0, last_image.height*y))
        last_image = r
        y += 1
    merged_im.save("full_pano.png",optimize=True, quality=95)

    for f in rows_arr:
        os.remove(f)
    
    # merged_im.sh

def download_tile(panoID, x, y, i, zoom):
    url = "https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={}&x={}&y={}&zoom={}&nbt=1&fover=2"
    url = url.format(panoID, x, y, zoom)
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    im.save(f"tile{i}.png")

if __name__ == "__main__":
    panorama.download_panorama("R5CMjP6w-l8q6aqt4wSyTA")
    
    # https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid=-xXXTLmT8HnuH2BpwkY3wQ&x=12&y=6&zoom=4&nbt=1&fover=2