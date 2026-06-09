import whisper
import os

# Tell Whisper exactly where ffmpeg is

os.environ["PATH"] += os.pathsep + r"C:\Users\LENOVO\Downloads\ffmpeg-8.1.1-essentials_build\ffmpeg-8.1.1-essentials_build\bin"

model = whisper.load_model("base")


def transcribe_audio(audio_file):

    print("FILE PATH =", audio_file)
    print("EXISTS =", os.path.exists(audio_file))

    result = model.transcribe(audio_file)

    return result["text"]