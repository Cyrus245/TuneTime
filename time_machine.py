import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from datetime import date


class Time_machine:

    def __init__(self, config, u_input, billboard_data):
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.user_input = u_input
        self.all_song_titles = None
        self.data = billboard_data
        self.user_id = None
        self.song_uri_list = []
        self.sp = self.authentication()
        self.data_extraction()
        self.get_song_uri()
        self.playlist_id = self.create_playlist()
        self.add_tracks()

    def authentication(self):
        """This method authenticate oAuth2 spotify api"""
        sp = spotipy.Spotify(
            # Authenticating using spotipy OAuth
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-public",
                redirect_uri="http://example.com",
                client_id=self.client_id,
                client_secret=self.client_secret,
                show_dialog=True,
                cache_path="token.txt",
            )
        )
        self.user_id = sp.current_user()['id']
        return sp

    def data_extraction(self):
        """This method extract tracks name using beautiful soup"""
        # scraping the track's name
        soup = BeautifulSoup(self.data, "html.parser")
        all_songs_title = soup.select(".o-chart-results-list__item h3")
        self.all_song_titles = [title.get_text().strip() for title in all_songs_title]

    def get_song_uri(self):
        """This method generate extracted song's URI"""
        for song_uri in self.all_song_titles:
            result = self.sp.search(q=song_uri)
            try:
                # extracting song URI
                uri = result['tracks']['items'][0]['uri']
                self.song_uri_list.append(uri)
            except IndexError:
                print("track isn't found")

    def create_playlist(self):
        """This method creates a spotify playlist"""
        # turning user input to a date
        year, month, day = map(int, self.user_input.split('-'))
        date1 = date(year, month, day)

        playlist_id = \
            self.sp.user_playlist_create(user=self.user_id, name=f"Top tracks of {day} {date1.strftime('%B')},{year}",
                                         description="best playlist",
                                         )['id']

        return playlist_id

    def add_tracks(self):
        """This method add tracks to the playlist"""
        self.sp.playlist_add_items(playlist_id=self.playlist_id, items=self.song_uri_list)
