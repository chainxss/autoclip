import yt_dlp

def download(url, out_dir="downloads"):
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    download("https://www.youtube.com/watch?v=iCvEcY-Suikt")