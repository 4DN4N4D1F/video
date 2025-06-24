import os
from flask import Flask, render_template, request, flash, redirect, url_for
import yt_dlp

app = Flask(__name__)
app.secret_key = "your_secret_key"

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "Downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def get_video_info(url):
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def download_video(url, format_choice):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
    }
    if format_choice == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET', 'POST'])
def index():
    info = None
    if request.method == 'POST':
        url = request.form.get('url')
        format_choice = request.form.get('format')
        folder = request.form.get('folder') or "Downloads"
        try:
            info = get_video_info(url)
            download_video(url, format_choice)
            flash(f"Downloaded: {info.get('title', 'Unknown Title')} as {format_choice.upper()} in {folder}", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template('videodown.html', info=info)

if __name__ == '__main__':
    app.run(debug=True)