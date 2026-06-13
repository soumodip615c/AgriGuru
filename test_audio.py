from models.speech_to_text import transcribe_audio

audio_path = "input/audio/test.wav"

text = transcribe_audio(audio_path)

print("\nTranscript:")
print(text)