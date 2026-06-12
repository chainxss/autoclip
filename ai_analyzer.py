import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("api_key")
)
# taking the json file from downloder.py
def load_transcript(path="transcript.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
#making the trascript more digestable and more efficent for ai to read
def format_transcript(transcript):
    lines = []
    for entry in transcript:
        start = int(entry["start"])
        lines.append(f"[{start}s] {entry['text']}")
    return "\n".join(lines)
#giving the trascript to ai to find the viral moments
def find_moments(transcript_text):
    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {"role": "user", "content": f"""You are a video editor cutting short clips from a conversation transcript.

Each transcript line is formatted as [seconds] text. Find the 3 most clip-worthy moments.

RULES for each clip:
- end minus start MUST be between 30 and 65 seconds. This is mandatory.
- A clip spans MANY consecutive lines combined (usually 5-15 lines), never a single line.
- It must be self-contained: a clear beginning, middle, and end, making sense on its own.
- Before outputting, calculate end - start and confirm it is 30 or more. If under 30, add more lines.

Return ONLY valid JSON, a list of 3 objects, nothing else:
[{{"start": <seconds>, "end": <seconds>, "title": "<short title>"}}]

Example of a correct clip (note 158 - 120 = 38 seconds):
{{"start": 120, "end": 158, "title": "the bet goes wrong"}}

Transcript:
{transcript_text}
"""}
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    transcript = load_transcript()              # 1. read transcript.json
    text = format_transcript(transcript)        # 2. make timestamped string
    result = find_moments(text)                 # 3. ask the AI
    print(result)
    