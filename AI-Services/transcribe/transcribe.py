import subprocess
import sys
import os

OUTPUT_DIR = "output"
AUDIO_M4A = os.path.join(OUTPUT_DIR, "audio.m4a")
CLEAN_WAV = os.path.join(OUTPUT_DIR, "clean.wav")
TRANSCRIPT = os.path.join(OUTPUT_DIR, "clean.txt")

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a YouTube URL")
        return

    yt_url = sys.argv[1]
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("⬇ Downloading audio...")
    run(f'yt-dlp -f bestaudio -o "{AUDIO_M4A}" "{yt_url}"')

    print("🎚 Normalizing audio...")
    run(f'ffmpeg -y -i "{AUDIO_M4A}" -ar 16000 -ac 1 -vn "{CLEAN_WAV}"')

    print("🧠 Transcribing & translating to English...")
    run(
        f'whisper "{CLEAN_WAV}" '
        f'--task translate '
        f'--model base '
        f'--output_dir "{OUTPUT_DIR}" '
        f'--output_format txt '
        f'--language English'
    )

    print("✅ DONE!")
    print(f"📄 Transcript saved at: {TRANSCRIPT}")

if __name__ == "__main__":
    main()
