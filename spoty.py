from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import webbrowser as web
import pyautogui
from time import sleep

# Personal Spotify credentials
#client_id = 'aea3fbf1f0554dc598dd77b88f30a012'
#client_secret = 'c58898c782d14880802b46d32fc81e64'

# Song information
#song = 'normal'
#author = ''

def play(client_id, client_secret, song, author = ''):
    flag = 0
    song = song.upper()

    if len(author) > 0:
        # authenticate
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        result = sp.search(author)

        for i in range(0, len(result["tracks"]["items"])):
            # songs by artist
            name_song = result["tracks"]["items"][i]["name"].upper()

            if song in name_song:
                flag = 1
                web.open(result["tracks"]["items"][i]["uri"])
                sleep(5)
                #pyautogui.press("enter")
                break

    # if song by artist not found
    if flag == 0:
        song = song.replace(" ", "%20")
        web.open(f'spotify:search:{song}')
        sleep(4)
        for i in range(4):
            pyautogui.press("tab")

        for i in range(1):
            pyautogui.press("enter")
            sleep(1)

#play(client_id, client_secret, song, author)