#!/usr/bin/env python3
import subprocess
from ytmusicapi import YTMusic

def play_songs_with_mpv(urls, titles):
    """Play multiple songs using mpv with MPRIS support and customized output."""
    args = [
        "mpv",
        "--no-video",
        "--no-resume-playback",  # Suppress the "Resuming playback" message
        "--msg-level=cplayer=error",  # Suppress cplayer messages below error level
        "--msg-level=ao=fatal",  # Suppress audio output messages below fatal level
    ]
    
    # Add each URL and its corresponding title
    for url, title in zip(urls, titles):
        args.extend([f"--force-media-title={title}", url])
    
    # Run mpv and capture the output
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    # Iterate through each line of the output
    for line in process.stdout:
        # Only print lines containing "Playing:" or the title
        if "Playing:" in line:
            # Extract the video ID from the URL
            video_id = line.split("https://www.youtube.com/watch?v=")[-1].strip()
            # Find the corresponding title for the video ID
            for url, title in zip(urls, titles):
                if video_id in url:
                    print("\033[92mPlaying:", title, "\033[0m")  # Green color
                    break
        elif any(title in line for title in titles):
            print(line.strip())

    process.communicate()


def main():
    # Initialize YTMusic with your authentication file
    yt = YTMusic('oauth.json')
    
    # Search for a song or artist
    query = input("Enter song or artist name: ")
    search_results = yt.search(query)
    
    # Check if there are any results
    if not search_results:
        print("No results found!")
        return
    
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
    
    if video_urls:
        play_songs_with_mpv(video_urls, titles)
    else:
        print("No videos found in the search results.")

if __name__ == "__main__":
    main()
