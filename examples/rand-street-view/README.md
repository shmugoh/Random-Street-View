# Random Street View (Bot) 

Archvived repository because I am moving on from Twitter. Expect bugs. Feel free to edit it, host it, whatever you want to do with it (by following the license's guidelines of course).

**Please be aware that this sends a lot of requests to Google's API thus it may be pricey. if you want an estimation on how much it'll cost monthly and has Google Cloud's $200 credit promotion, monitor the requests and the billing and make your own conclusions.** 

**I am not responsible if Google charges you a million dollars, that's your problem for not monitoring billing or calculating.**

##

Twitter Bot **(doesn't necessary have to be a Twitter Bot; refer to the next line)** that generates a random coordinate which gets reverse geocoded, translates it to a Street View image (by getting the panorama ID via the coordinates) then tweets it.

**You can also use this if you don't have intentions for a Twitter Bot as long as you credit me and remove the Twitter-related lines on the script**

## Before you begin...

- You need a Google Cloud account to get access to Google Maps' API. After you get it, create a project, enable following APIs (and get the API Key via credentials):

  - Geocoding API

  - Street View Static API

- **Optional if not using it for a Twitter Bot:** You also need a Twitter Developer Account; apply for access [here](https://developer.twitter.com/en/apply-for-access).

- And finally, you need Python **3**;  NOT 2, but **3**. If you're on Windows, I recommend you to get it [on Python's official website](https://www.python.org/downloads/) instead of downloading it on the Microsoft Store.

## Setup

**1.** Clone the repository via git clone

```git
git clone https://github.com/juanpisuribe13/Random-Street-View-Bot.git
```

**2.** Add your Twitter and Google API keys to the `config_barebones.cfg` file, then rename it to `config.cfg`.

**3.** To not clutter your Python installation, create a virtual environment by typing this line:
```bash
python3 -m venv env

# if above command opens windows store, try this one
python -m venv env
 ``` 
**3.1** After creating the virtual environment, access it by:

```bash
# For UNIX users:
source env/bin/activate

# For Windows users:
.\env\Scripts\activate.bat
```
**4.** Install the required libraries found in the `requirements.txt` file.
```bash
pip install -r requirements.txt

# if above command doesn't work, try this
python3 -m pip install -r requirements.txt

## if above command STILL doesn't work because it 
## opened a windows store tab, try this one
python3 -m pip install -r requirements.txt
```
**5.** You're done! All you have to do is run `python3 main.py` (or `python main.py` if it opens Windows Store) 


## FAQ

### Are the images panoramic/360?

**Short Answer:** No.

**Long Answer:** Still no. Google Maps API hasn't implemented that ~~yet~~ and only way to get it is via "undocumented interfaces" which is [against Google's TOS](https://developers.google.com/maps/terms-20180207#10.-license-restrictions.). So if you end up implementing it and Google bans you, that's your problem.

### Why are the images low-res?
That's Google's problem. Even if you give it the highest resolution, the quality of the image is still low-res. 

### What APIs does this script use?

  - Geocoding API (Reverse Geocode)

  - Street View Static API (SV Image Metadata to get the Panorama ID and SV Static API to download the Street View Image)

### I want to use this, but I don't plan doing it as a Twitter Bot. Can I?

Sure! As long as you credit me; if you have knowledge of Python (which you should), you could easily remove the Twitter-related lines. Also refer to the next question

### Can I use this for my project/twitter bot?
Sure! As long as you link the source code of this (or credit me if you fork this repository and edit your own code). Keep in mind though I won't be responsible if the billing comes expensive; refer to the start of this README.md for more information.


### If Google Maps' API is pricey, why are you using it?
I'm using it because it's the easiest way to reverse geocoordinates that are compatible with Street View, and it's the **only** way to get panoramic IDs. 

## Contributing
If you see that the code's messy, something doesn't work, or I left something dumb there accidentally then feel free to send a pull request and I'll review it!

## License
[MIT](https://raw.githubusercontent.com/juanpisuribe13/Random-Street-View/master/LICENSE)
