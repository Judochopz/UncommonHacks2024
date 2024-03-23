import spotify_auth


def main(userID):
    sp, user = spotify_auth.spotifyAuth(userID)
    sp_user = sp.current_user()
    user_id = user["id"]

    top_songs = sp.current_user_top_tracks(limit=10)
    for idx, item in enumerate(top_songs['items']):
        track = item
        print(idx, track['artists'][0]['name'], " – ", track['name'])

if __name__ == "__main__":
    while(True):
        print("Enter Spotify user ID:")
        userID = input()
        print(f"Type YES if this is your userID:{userID}")
        if input() == "YES":
            break
    main(userID)