from models.speech_to_text import transcribe_audio
from backend.main import get_answer

audio_path = "input/audio/test.wav"

print("Transcribing...")

question = transcribe_audio(audio_path)

print("\nQuestion:")
print(question)

print("\nGenerating Answer...")

answer = get_answer(question)

print("\nAgriGuru Answer:\n")
print(answer)