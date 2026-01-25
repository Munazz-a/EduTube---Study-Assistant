from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

OUTPUT_DIR = "output"
AUDIO_M4A = os.path.join(OUTPUT_DIR, "audio.m4a")
CLEAN_WAV = os.path.join(OUTPUT_DIR, "clean.wav")
TRANSCRIPT = os.path.join(OUTPUT_DIR, "clean.txt")

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json
    yt_url = data.get("videoLink")

    if not yt_url:
        return jsonify({"error": "No YouTube link provided"}), 400

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        run(f'yt-dlp -f bestaudio -o "{AUDIO_M4A}" "{yt_url}"')
        run(f'ffmpeg -y -i "{AUDIO_M4A}" -ar 16000 -ac 1 -vn "{CLEAN_WAV}"')
        run(
            f'whisper "{CLEAN_WAV}" '
            f'--task translate '
            f'--model base '
            f'--output_dir "{OUTPUT_DIR}" '
            f'--output_format txt '
        )

        with open(TRANSCRIPT, "r", encoding="utf-8") as f:
            transcript_text = f.read()

        return jsonify({"transcript": transcript_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
