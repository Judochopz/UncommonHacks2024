import spotify_auth
import pandas as pd

def main(userID):
    sp, user = spotify_auth.spotifyAuth(userID)

    top_songs = sp.current_user_top_tracks(limit=10, time_range="long_term")
    top_related_artists = set()

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
    potential_track_vectors = dict()
    potential_track_vectors['name'] = []
    potential_track_vectors['artist'] = []
    potential_track_vectors['artist_id'] = []
    for feature in track_features:
        potential_track_vectors[feature] = []
    potential_track_vectors['genre'] = []
    while top_related_artists:
        artist_tracks = sp.artist_top_tracks(top_related_artists.pop())['tracks']
        for track in artist_tracks:
            track_audio_features = sp.audio_features(track['id'])[0]
            potential_track_vectors['name'].append(track['name'])
            potential_track_vectors['artist'].append(track['artists'][0]['name'])
            potential_track_vectors['artist_id'].append(track['artists'][0]['id'])
            for feature in track_features:
                potential_track_vectors[feature].append(track_audio_features[feature])
            potential_track_vectors['genre'].append(set(sp.artists([track['artists'][0]['id']])['artists'][0]['genres']))
    potential_recommended = pd.DataFrame(potential_track_vectors)

    track_history.to_csv("track_history.csv")
    potential_recommended.to_csv("potential_recommended.csv")


if __name__ == "__main__":
    while(True):
        print("Enter Spotify user ID:")
        userID = input()
        print(f"Type YES if this is your userID:{userID}")
        if input() == "YES":
            break
    main(userID)