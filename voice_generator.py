from gtts import gTTS

def generate_voice(question):

    tts = gTTS(
        text=question,
        lang="en"
    )

    filename = "question.mp3"

    tts.save(filename)

    return filename