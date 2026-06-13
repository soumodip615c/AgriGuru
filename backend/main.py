import os
from dotenv import load_dotenv
from groq import Groq

# =========================
# Load Environment Variables
# =========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# =========================
# Initialize Groq Client
# =========================
client = Groq(api_key=GROQ_API_KEY)

# =========================
# System Prompt
# =========================
SYSTEM_PROMPT = """
You are AgriGuru, an expert agricultural assistant.

Your responsibilities include:
- Crop selection
- Fertilizer recommendations
- Pest and disease management
- Irrigation guidance
- Soil health improvement
- Sustainable farming practices
- General agriculture-related questions

Provide practical, easy-to-understand, and farmer-friendly answers.
"""

# =========================
# Generate Answer
# =========================
def get_answer(question):

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# Save History
# =========================
def save_history(question, answer):

    os.makedirs("output", exist_ok=True)

    history_file = os.path.join("output", "history.txt")

    with open(history_file, "a", encoding="utf-8") as file:

        file.write("\n")
        file.write("=" * 100)
        file.write("\n")

        file.write("QUESTION:\n")
        file.write(question)
        file.write("\n\n")

        file.write("ANSWER:\n")
        file.write(answer)
        file.write("\n")

        file.write("=" * 100)
        file.write("\n")


# =========================
# Main Function
# =========================
def main():

    print("=" * 50)
    print("🌾 Welcome to AgriGuru")
    print("=" * 50)

    question = input("\nAsk your agriculture question: ")

    answer = get_answer(question)

    save_history(question, answer)

    print("\nAgriGuru:\n")
    print(answer)


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    main()