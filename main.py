import borders.coordinates
import streetview.panorama
from webbrowser import open_new_tab

while True:
    try:
        c = borders.coordinates.generate_random_coordinates()
        a = streetview.panorama.getpanoID(c[0], c[1])
        print(a)
        print(c[2])
        open_new_tab(f"https://www.google.nl/maps/@58.6502986,11.2959174,3a,90y,12.9h,88.82t/data=!3m5!1e1!3m3!1s{a['pano_id']}!2e0!3e11")
    except IndexError:
        print("none " + (c[2]))
        continue