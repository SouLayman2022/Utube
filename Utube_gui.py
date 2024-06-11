import os
import sys
import webbrowser
from tkinter import Tk, Label, Button, filedialog, Entry, StringVar, PhotoImage, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from pytube import Playlist, YouTube
import threading

CONFIG_FILE = 'config.txt'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

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
    url = url_entry.get()
    output_path = folder_path.get()
    if url and output_path:
        progress_bar['value'] = 0
        progress_label.config(text="")
        if 'list=' in url:  # Check if the URL is a playlist
            try:
                playlist = Playlist(url)
                threading.Thread(target=download_playlist, args=(url, output_path)).start()
            except Exception as e:
                messagebox.showerror("Input Error", f"Failed to recognize playlist URL. Error: {str(e)}")
        else:  # Treat it as a video
            try:
                yt = YouTube(url)
                threading.Thread(target=download_video, args=(url, output_path, lambda title: update_progress(1, 1, title))).start()
            except Exception as e:
                messagebox.showerror("Input Error", f"Failed to recognize video URL. Error: {str(e)}")
    else:
        if not url:
            messagebox.showerror("Input Error", "Please provide a playlist or video URL.")
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

def change_user_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        save_user_image_path(file_path)
        load_user_image(file_path)

def save_user_image_path(path):
    with open(CONFIG_FILE, 'w') as file:
        file.write(path)

def load_user_image(path):
    new_image = Image.open(path)
    new_image = new_image.resize((120, 120))
    new_photo = ImageTk.PhotoImage(new_image)
    user_label.config(image=new_photo)
    user_label.image = new_photo  # Keep a reference to avoid garbage collection

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            path = file.readline().strip()
            if os.path.exists(path):
                load_user_image(path)
            else:
                load_user_image(resource_path("Assets/SoSo.png"))
    else:
        load_user_image(resource_path("Assets/SoSo.png"))

# Initialize the main window
root = Tk()
root.title("YouTube Playlist Downloader")
root.geometry("500x400")  # Increased height to accommodate links

# Set the window icon (favicon)
icon_image = ImageTk.PhotoImage(file=resource_path("Assets/Fave_icon.ico"))
root.iconphoto(False, icon_image)

# Placeholder for user image
user_label = Label(root)
user_label.grid(row=0, column=0, padx=10, pady=10)

# Load the user image from config or default
load_config()

# Button to change user image
change_image_button = Button(root, text="Change User Image", command=change_user_image)
change_image_button.grid(row=1, column=0, padx=10, pady=10)

# Placeholder for program logo
program_logo = Image.open(resource_path("Assets/Logo.png"))
program_logo = program_logo.resize((280, 120))
logo_photo = ImageTk.PhotoImage(program_logo)

logo_label = Label(root, image=logo_photo)
logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
logo_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

# Folder selection button
folder_path = StringVar()
folder_button = Button(root, text="Select Folder", command=browse_folder)
folder_button.grid(row=2, column=0, padx=10, pady=10)

# URL entry and download button
url_entry = Entry(root, width=50)
url_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

download_button = Button(root, text="Download", command=start_download)
download_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

# Progress bar and label
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

progress_label = Label(root, text="")
progress_label.grid(row=4, column=0, columnspan=2)

# Add links
github_label = Label(root, text="My GitHub", fg="blue", cursor="hand2")
github_label.grid(row=5, column=0, padx=10, pady=5)
github_label.bind("<Button-1>", lambda e: open_link("https://github.com/SouLayman2022"))

linkedin_label = Label(root, text="My LinkedIn", fg="blue", cursor="hand2")
linkedin_label.grid(row=5, column=1, padx=10, pady=5)
linkedin_label.bind("<Button-1>", lambda e: open_link("https://www.linkedin.com/in/soulayman-el-guasmi-13b890240/"))

# Start the GUI loop
root.mainloop()
