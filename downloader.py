import yt_dlp
import json
from youtube_transcript_api import YouTubeTranscriptApi
#getting the video

def download(url, out_dir="downloads"):
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])



#getting transcript
def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    return transcript.to_raw_data()
#saving the trascripit
def save_transcript(transcript, path="transcript.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=2)
# calling the functions
if __name__ == "__main__":
    
    download("https://www.youtube.com/watch?v=K-QA3Mb11AE")
    data = get_transcript("K-QA3Mb11AE")
        
    save_transcript(data)
    print("saved")
   