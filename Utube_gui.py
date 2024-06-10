import os
import webbrowser
from tkinter import Tk, Label, Button, filedialog, Entry, StringVar, PhotoImage, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from pytube import Playlist, YouTube
import threading

def open_link(url):
    webbrowser.open_new(url)

def download_video(video_url, output_path, progress_callback):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(output_path=output_path)
        progress_callback(yt.title)
    except Exception as e:
        update_progress(-1, 0, f"Failed to download {video_url}. Error: {str(e)}")

def download_playlist(playlist_url, output_path):
    playlist = Playlist(playlist_url)
    update_progress(0, len(playlist.video_urls), f'Downloading playlist: {playlist.title}')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    total_videos = len(playlist.video_urls)
    for index, video_url in enumerate(playlist.video_urls):
        download_video(video_url, output_path, lambda title: update_progress(index + 1, total_videos, title))

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def start_download():
    playlist_url = url_entry.get()
    output_path = folder_path.get()
    if playlist_url and output_path:
        progress_bar['value'] = 0
        progress_label.config(text="")
        threading.Thread(target=download_playlist, args=(playlist_url, output_path)).start()
    else:
        if not playlist_url:
            messagebox.showerror("Input Error", "Please provide a playlist URL.")
        if not output_path:
            messagebox.showerror("Input Error", "Please select a folder to save the downloaded videos.")

def update_progress(current, total, message):
    if current == -1:
        progress_label.config(text=message)
        root.update_idletasks()
        return

    progress = (current / total) * 100
    progress_bar['value'] = progress
    progress_label.config(text=f"{message}\nDownloaded {current} of {total} videos")
    root.update_idletasks()

# Initialize the main window
root = Tk()
root.title("YouTube Playlist Downloader")
root.geometry("500x400")  # Increased height to accommodate links

# Set the window icon (favicon)
icon_image = ImageTk.PhotoImage(file="./Assets/Fave_icon.ico")  # Replace with the actual path to your icon
root.iconphoto(False, icon_image)

# Placeholder for user image
user_image = Image.open("./Assets/SoSo.png")  # Replace with the actual path
user_image = user_image.resize((120, 120))
user_photo = ImageTk.PhotoImage(user_image)

user_label = Label(root, image=user_photo)
user_label.image = user_photo  # Keep a reference to avoid garbage collection
user_label.grid(row=0, column=0, padx=10, pady=10)

# Placeholder for program logo
program_logo = Image.open("./Assets/Logo.png")  # Replace with the actual path
program_logo = program_logo.resize((280, 120))
logo_photo = ImageTk.PhotoImage(program_logo)

logo_label = Label(root, image=logo_photo)
logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
logo_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

# Folder selection button
folder_path = StringVar()
folder_button = Button(root, text="Select Folder", command=browse_folder)
folder_button.grid(row=1, column=0, padx=10, pady=10)

# URL entry and download button
url_entry = Entry(root, width=50)
url_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

download_button = Button(root, text="Download Playlist", command=start_download)
download_button.grid(row=1, column=1, padx=10, pady=10, sticky='e')

# Progress bar and label
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

progress_label = Label(root, text="")
progress_label.grid(row=3, column=0, columnspan=2)

# Add links
github_label = Label(root, text="My GitHub", fg="blue", cursor="hand2")
github_label.grid(row=4, column=0, padx=10, pady=5)
github_label.bind("<Button-1>", lambda e: open_link("https://github.com/SouLayman2022"))

linkedin_label = Label(root, text="My LinkedIn", fg="blue", cursor="hand2")
linkedin_label.grid(row=4, column=1, padx=10, pady=5)
linkedin_label.bind("<Button-1>", lambda e: open_link("https://www.linkedin.com/in/soulayman-el-guasmi-13b890240/"))

# Start the GUI loop
root.mainloop()
