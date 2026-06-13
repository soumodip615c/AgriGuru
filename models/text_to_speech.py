from gtts import gTTS
import os


def text_to_speech(text):

    os.makedirs("output/audio", exist_ok=True)

    audio_path = os.path.join(
        "output",
        "audio",
        "response.mp3"
    )

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save(audio_path)

    return audio_path