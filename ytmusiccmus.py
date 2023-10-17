#!/usr/bin/env python3
import subprocess
import random
import os
from ytmusicapi import YTMusic



def play_songs_with_mpv(urls, titles):
    """Play multiple songs using mpv with MPRIS support and customized output."""
    
    # Create a temporary playlist file
    playlist = "\n".join(urls)
    with open("temp_playlist.txt", "w") as f:
        f.write(playlist)
    
    print(f"\033[92mNow Playing: {titles[0]}\033[0m")  # Display the first title in green color
    args = [
        "mpv",
        "--no-video",
        "--no-resume-playback",
        "--msg-level=cplayer=error",
        "--msg-level=ao=error",
        "--playlist=temp_playlist.txt"  # Play songs from the temporary playlist
    ]
    subprocess.run(args)
    
    # Clean up the temporary playlist file
    os.remove("temp_playlist.txt")

def main():
    # Initialize YTMusic with your authentication file
    yt = YTMusic('oauth.json')
    
    # Fetch user's saved playlists
    playlists = yt.get_library_playlists(limit=20)
    
    # Display the top 10 playlists to the user in two columns of 5
    print("Your top 10 playlists:")
    for i in range(5):
        print(f"{i+1}. {playlists[i]['title']} \t {i+6}. {playlists[i+5]['title'] if i+5 < len(playlists) else ''}")
    
    # Ask the user to select a playlist or search for a song/artist
    choice = input("\nEnter playlist number (1-10) or song/artist name: ")
    
    if choice.isdigit() and 1 <= int(choice) <= 20:
        # User selected a playlist
        playlist_id = playlists[int(choice) - 1]['playlistId']
        tracks = yt.get_playlist(playlist_id, limit=100)['tracks']
        video_urls = [f"https://www.youtube.com/watch?v={track['videoId']}" for track in tracks]
        titles = [f"{track['title']} - {track['artists'][0]['name']}" for track in tracks]
    else:
        # User searched for a song/artist
        search_results = yt.search(choice)
        
        # Extract video URLs and titles for the first few results with a 'videoId' key
        video_urls = []
        titles = []
        for result in search_results:
            if 'videoId' in result:
                video_url = f"https://www.youtube.com/watch?v={result['videoId']}"
                title = result.get('title', 'Unknown Title')
                artist = result.get('artists', [{'name': 'Unknown Artist'}])[0]['name']
                display_title = f"{title} - {artist}"
                
                video_urls.append(video_url)
                titles.append(display_title)
    
    # Ask the user if they want to shuffle the songs
    shuffle_choice = input("Press 's' to shuffle or any other key to continue: ")
    if shuffle_choice.lower() == 's':
        combined = list(zip(video_urls, titles))
        random.shuffle(combined)
        video_urls, titles = zip(*combined)
    
    if video_urls:
        play_songs_with_mpv(video_urls, titles)
    else:
        print("No videos found in the search results or playlist.")

if __name__ == "__main__":
    main()
