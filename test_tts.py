from models.text_to_speech import text_to_speech

audio_path = text_to_speech(
    "Welcome to AgriGuru"
)

print(audio_path)