import spotify_auth
import pandas as pd
from multiprocessing.pool import ThreadPool 

def main(userID):
    # Take in spotipy object and user object
    sp, user = spotify_auth.spotifyAuth(userID)

    # Find top 10 songs of user
    top_songs = sp.current_user_top_tracks(limit=10, time_range="long_term")
    # Create set to determine top artists potential songs
    top_related_artists = set()
    # Create set to prevent top 10 songs from being placed in potential recommended songs
    top_ten_songs = set()

    # Create dictionary for track vectors for pd.DataFrame conversion
    track_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 
                      'instrumentalness', 'liveness', 'loudness', 'mode', 'speechiness',
                      'tempo', 'time_signature', 'valence', 'analysis_url']
    track_vectors = dict()
    track_vectors['name'] = []
    track_vectors['artist'] = []
    track_vectors['artist_id'] = []
    for feature in track_features:
        track_vectors[feature] = []
    track_vectors['genre'] = []

    # Iterate through top songs of user
    for track in top_songs['items']:
        top_ten_songs.add(track['id'])
        related_artists = sp.artist_related_artists(track['artists'][0]['id'])['artists']

        for artist in related_artists[:5]:
            top_related_artists.add(artist['id'])
        track_audio_features = sp.audio_features(track['id'])[0]
        track_vectors['name'].append(track['name'])
        track_vectors['artist'].append(track['artists'][0]['name'])
        track_vectors['artist_id'].append(track['artists'][0]['id'])
        for feature in track_features:
            track_vectors[feature].append(track_audio_features[feature])
        track_vectors['genre'].append(set(sp.artists([track['artists'][0]['id']])['artists'][0]['genres']))
    track_history = pd.DataFrame(track_vectors)
    related_artist_list = list(top_related_artists)
    # Function for potential recommended songs to allow multi-threading
    def potential_recommended_songs(artist_list, top_ten_songs = top_ten_songs):
        potential_track_vectors = dict()
        potential_track_vectors['name'] = []
        potential_track_vectors['artist'] = []
        potential_track_vectors['artist_id'] = []
        for feature in track_features:
            potential_track_vectors[feature] = []
        potential_track_vectors['genre'] = []
        for artist in artist_list:
            artist_tracks = sp.artist_top_tracks(artist)['tracks']
            for track in artist_tracks:
                if track['id'] in top_ten_songs:
                    continue
                track_audio_features = sp.audio_features(track['id'])[0]
                potential_track_vectors['name'].append(track['name'])
                potential_track_vectors['artist'].append(track['artists'][0]['name'])
                potential_track_vectors['artist_id'].append(track['artists'][0]['id'])
                for feature in track_features:
                    potential_track_vectors[feature].append(track_audio_features[feature])
                potential_track_vectors['genre'].append(set(sp.artists([track['artists'][0]['id']])['artists'][0]['genres']))
        return pd.DataFrame(potential_track_vectors)
    # Multi-threading for faster API calling
    # with ThreadPool(3) as p:
    #     vec = p.map(potential_recommended_songs, related_artist_list)
    # potential_recommended = pd.concat(vec)
    potential_recommended = potential_recommended_songs(related_artist_list)
    track_history.to_csv("sampleCSVs/track_history2csv")
    potential_recommended.to_csv("sampleCSVs/potential_recommended2.csv")


if __name__ == "__main__":
    while(True):
        print("Enter Spotify user ID:")
        userID = input()
        print(f"Type YES if this is your userID:{userID}")
        if input() == "YES":
            break
    main(userID)