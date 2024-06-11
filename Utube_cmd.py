from pytube import Playlist, YouTube
from tqdm import tqdm
import os

def download_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(output_path=output_path)
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Failed to download {video_url}. Error: {str(e)}")

def download_playlist(playlist_url, output_path):
    playlist = Playlist(playlist_url)
    print(f'Downloading playlist: {playlist.title}')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for video_url in tqdm(playlist.video_urls, desc="Downloading videos"):
        download_video(video_url, output_path)

def start_download(url, output_path):
    if 'playlist' in url:
        download_playlist(url, output_path)
    else:
        download_video(url, output_path)

if __name__ == "__main__":
    url = input("Enter the YouTube playlist or video URL: ")
    output_path = input("Enter the directory where you want to save the videos: ")
    start_download(url, output_path)
