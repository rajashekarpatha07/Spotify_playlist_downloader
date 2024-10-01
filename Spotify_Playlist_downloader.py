import os
import pandas as pd
import yt_dlp
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time

# Set up logging
logging.basicConfig(filename='download_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Playlist Downloader")
        self.root.geometry('500x500')  # Increased height for new buttons
        self.root.configure(bg='#282c34')  # Dark background

        # Variables for managing downloads
        self.cancel_download = False
        self.pause_download = False
        self.file_path = None
        self.download_path = None  # Added variable for download path
        self.current_speed = 0  # Variable to hold current download speed
        self.speed_lock = threading.Lock()  # Lock for thread safety

        # Styling the GUI
        style = ttk.Style()
        style.configure("TLabel", foreground="#ffffff", background="#282c34", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 10), padding=6)
        style.configure("TProgressbar", thickness=20)

        # File selection label and button
        self.file_label = ttk.Label(root, text="No file selected", anchor="center")
        self.file_label.pack(pady=10)

        self.select_file_button = ttk.Button(root, text="Select Excel or TXT File", command=self.select_file)
        self.select_file_button.pack(pady=5)

        # Download location button
        self.select_download_button = ttk.Button(root, text="Select Download Location", command=self.select_download_location)
        self.select_download_button.pack(pady=5)

        # Format selection (MP3/MP4)
        self.format_var = tk.StringVar(value="mp3")
        ttk.Radiobutton(root, text="MP3", variable=self.format_var, value="mp3").pack(anchor=tk.W)
        ttk.Radiobutton(root, text="MP4", variable=self.format_var, value="mp4").pack(anchor=tk.W)

        # Progress Bar and labels
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=10)

        self.progress_label = ttk.Label(root, text="Progress: 0%", anchor="center")
        self.progress_label.pack()

        # Time remaining label
        self.time_remaining_label = ttk.Label(root, text="Estimated Time Remaining: Calculating...", anchor="center")
        self.time_remaining_label.pack()

        # Download speed label
        self.speed_label = ttk.Label(root, text="Download Speed: 0 KB/s", anchor="center")
        self.speed_label.pack()

        # Currently downloading song label
        self.current_song_label = ttk.Label(root, text="", anchor="center", foreground="#00ff00")
        self.current_song_label.pack(pady=5)

        # Next song label
        self.next_song_label = ttk.Label(root, text="", anchor="center", foreground="#ffa500")
        self.next_song_label.pack(pady=5)

        # Start, Pause, and Cancel Buttons
        self.start_button = ttk.Button(root, text="Start Download", command=self.start_download)
        self.start_button.pack(pady=10)

        self.pause_button = ttk.Button(root, text="Pause Download", command=self.pause_download_func)
        self.pause_button.pack(pady=5)

        self.cancel_button = ttk.Button(root, text="Cancel Download", command=self.cancel_download_func)
        self.cancel_button.pack(pady=5)

    # Function to select the file
    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Excel or TXT File", 
            filetypes=(("Excel files", "*.xlsx"), ("Text files", "*.txt"))
        )
        if self.file_path:
            self.file_label.config(text=os.path.basename(self.file_path))
            logging.info(f"Selected file: {self.file_path}")  # Log selected file

    # Function to select download location
    def select_download_location(self):
        self.download_path = filedialog.askdirectory(title="Select Download Folder")
        if self.download_path:
            logging.info(f"Selected download folder: {self.download_path}")
            messagebox.showinfo("Download Location Selected", f"Download will be saved to: {self.download_path}")

    # Function to extract track names from the Excel file
    def extract_track_names_from_excel(self):
        data = pd.read_excel(self.file_path, sheet_name='Worksheet')
        track_names = data['Track Name'].tolist()

        # Save track names to a text file
        with open('track_names.txt', 'w', encoding='utf-8') as file:
            for track in track_names:
                if isinstance(track, str):
                    file.write(track + '\n')
        logging.info("Track names have been saved to track_names.txt")
        return track_names

    # Function to extract track names from the text file
    def extract_track_names_from_txt(self):
        logging.info("Extracting track names from TXT file...")  # Log extraction start
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                track_names = file.readlines()
            track_names = [track.strip() for track in track_names]
            logging.info(f"Extracted {len(track_names)} tracks from TXT file.")
            return track_names
        except Exception as e:
            logging.error(f"Error reading TXT file: {e}")
            messagebox.showerror("Error", f"Failed to read TXT file: {e}")
            return []

    # Function to update the progress bar
    def update_progress(self, current, total):
        progress_percentage = (current / total) * 100
        self.progress['value'] = progress_percentage
        self.progress_label.config(text=f"Progress: {int(progress_percentage)}%")
        self.root.update_idletasks()

    # Function to calculate remaining time
    def update_time_remaining(self, start_time, current, total):
        elapsed_time = time.time() - start_time
        estimated_time = elapsed_time / current * (total - current)
        minutes, seconds = divmod(estimated_time, 60)
        self.time_remaining_label.config(text=f"Estimated Time Remaining: {int(minutes)}m {int(seconds)}s")

    # Function to update download speed
    def update_speed(self, speed):
        with self.speed_lock:
            self.current_speed = speed  # Store current speed

    # Function to display download speed in the GUI
    def display_speed(self):
        while not self.cancel_download:
            with self.speed_lock:
                speed_display = self.current_speed
            self.speed_label.config(text=f"Download Speed: {speed_display:.2f} KB/s")
            time.sleep(0.001)  # Update every millisecond

    # Function to download songs (runs in a separate thread)
    def download_songs(self):
        try:
            format_choice = self.format_var.get()

            # Determine if the file is Excel or TXT and extract track names accordingly
            if self.file_path.endswith('.xlsx'):
                track_names = self.extract_track_names_from_excel()
            elif self.file_path.endswith('.txt'):
                track_names = self.extract_track_names_from_txt()
            else:
                messagebox.showerror("Error", "Unsupported file format!")
                return

            total_tracks = len(track_names)
            start_time = time.time()

            # Start a thread to display speed
            speed_thread = threading.Thread(target=self.display_speed)
            speed_thread.start()

            downloaded_count = 0  # Counter for downloaded songs

            for i, track in enumerate(track_names, start=1):
                if self.cancel_download:
                    logging.info("Download cancelled.")
                    messagebox.showinfo("Cancelled", "Download cancelled by user.")
                    break
                while self.pause_download:
                    time.sleep(1)  # Pause the download
                self.current_song_label.config(text=f"Downloading: {track} ({downloaded_count}/{total_tracks})")  # Update current track label
                self.next_song_label.config(text=f"Next Song: {track_names[i] if i < total_tracks else 'None'}")  # Show next song
                self.download_song(track, format_choice)
                downloaded_count += 1  # Increment the downloaded count
                self.update_progress(downloaded_count, total_tracks)
                self.update_time_remaining(start_time, downloaded_count, total_tracks)

            if not self.cancel_download:
                messagebox.showinfo("Success", "Download Complete!")
            self.reset_after_download()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Download failed: {e}")

    # Function to download song using yt-dlp
    def download_song(self, song_name, format_choice='mp3'):
        search_url = f"ytsearch:{song_name}"
        ydl_opts = {
            'format': 'bestaudio/best' if format_choice == 'mp3' else 'bestvideo+bestaudio',
            'extractaudio': True if format_choice == 'mp3' else False,
            'audioformat': format_choice,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s') if self.download_path else '%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],  # Use progress hooks to update download speed
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_url])
                logging.info(f"Successfully downloaded: {song_name}")
        except Exception as e:
            logging.error(f"Failed to download {song_name}: {e}")

    # Progress hook to get download speed
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            speed = d.get('speed', 0) / 1024  # Convert speed to KB/s
            self.update_speed(speed)  # Update speed using lock
        elif d['status'] == 'finished':
            logging.info(f"Finished downloading: {d['filename']}")

    # Function to start download
    def start_download(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file!")
            return
        if not self.download_path:
            messagebox.showwarning("Warning", "Please select a download location!")
            return
        self.cancel_download = False
        self.pause_download = False
        self.download_thread = threading.Thread(target=self.download_songs)
        self.download_thread.start()

    # Function to pause the download
    def pause_download_func(self):
        self.pause_download = not self.pause_download  # Toggle pause state
        if self.pause_download:
            self.pause_button.config(text="Resume Download")
            logging.info("Download paused.")
        else:
            self.pause_button.config(text="Pause Download")
            logging.info("Download resumed.")

    # Function to cancel the download
    def cancel_download_func(self):
        self.cancel_download = True

    # Function to reset after download
    def reset_after_download(self):
        self.progress['value'] = 0
        self.progress_label.config(text="Progress: 0%")
        self.time_remaining_label.config(text="Estimated Time Remaining: Calculating...")
        self.speed_label.config(text="Download Speed: 0 KB/s")
        self.current_song_label.config(text="")
        self.next_song_label.config(text="")
        self.cancel_download = False
        self.pause_download = False

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloadApp(root)
    root.mainloop()
