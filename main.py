from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "9a372cc4d1d5470aade097578cffb54c"
CLIENT_SECRET = "66436d0e0bd744a881fff018af585899"
REDIRECT_URL = "https://www.spotify.com/in-en/account/overview/"
USERNAME = "voe332xfcwkt349naw5dx2k8p"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username= USERNAME,
    )
)

user_id = sp.current_user()["id"]

ask_user = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{ask_user}/"

response = requests.get(URL)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")
song_title_list = soup.select("li ul li h3")
song_title = [song.getText().strip() for song in song_title_list]


song_urls = []
year = ask_user.split("-")[0]
for song in song_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_urls.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped")


playlist = sp.user_playlist_create(user=USERNAME, name=f"{ask_user} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"],items=song_urls, position=None)