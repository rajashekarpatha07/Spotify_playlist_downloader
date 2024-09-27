# Spotify Playlist Downloader

Spotify Playlist Downloader is a Python application that helps you download songs from your Spotify playlist via YouTube. It extracts tracks from a provided playlist file and allows you to download them in MP3 or MP4 format.

---

## How to Download Your Spotify Playlist as an Excel File

### Step 1: Export Your Spotify Playlist
1. Go to [Exportify](https://exportify.app/) and log in using your Spotify credentials.
2. Download your Spotify playlist as a `.csv` file.

<!-- Replace with
actual path -->

### Step 2: Convert CSV to Excel
1. Visit [CloudConvert](https://cloudconvert.com/).
2. Convert your `.csv` file to `.xlsx` (Excel).

---

## Features

- **Download Spotify Playlist Tracks from YouTube**: Converts your playlist's track names into a downloadable format by searching on YouTube.
- **Batch Processing**: Downloads multiple songs at once.
- **MP3 or MP4 Format**: Choose whether you want audio or video downloads.
- **Track Progress and Speed**: Displays progress percentage, estimated time remaining, current download speed, and total number of songs downloaded.
- **Pause and Cancel Functionality**: Pause and resume downloads at your convenience.

---

## How to Use

1. Download the Spotify Playlist Downloader executable from the [releases](https://github.com/rajashekarpatha07/Spotify_playlist_downloader).
2. Run the `.exe` file.
3. Select your **Excel** or **TXT** file containing track names.
4. Choose your download location.
5. Select **MP3** or **MP4** as the desired format.
6. Press **Start Download**.

---

## Instructions Based on Code

### File Requirements:
- **Excel or TXT File**: Provide the track names in either `.xlsx` format (exported from Spotify via Exportify and converted to Excel) or a plain text file (`.txt`).

### How the App Works:
1. **Track Extraction**: The app extracts the track names from the selected file (Excel or TXT) and prepares them for YouTube searches.
2. **Download Process**: Each track is searched on YouTube, and the audio (or video) is downloaded.
3. **Speed and Progress Updates**: Throughout the download, you can see:
    - Current download speed (updated every millisecond).
    - The total number of songs downloaded out of the entire playlist.
    - The song currently downloading and the next song in the queue.
4. **Pause and Cancel Options**: You can pause or cancel the downloads anytime during the process.

### GUI Highlights:
- Dark-themed background for a visually appealing interface.
- Progress bar with percentage and real-time download speed display.
- Labels for current and next downloading tracks.
- Buttons for file selection, format selection (MP3 or MP4), and download location setup.

---

## How to Run Locally

1. Clone the repository:

    ```bash
     https://github.com/rajashekarpatha07/Spotify_playlist_downloader

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```


## Requirements

- Python 3.x
- Required libraries:
    - `pandas`
    - `yt-dlp`
    - `tkinter`
    - `logging`
    - `threading`

---
