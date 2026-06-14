import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_treatment(disease_name):

    prompt = f"""
    You are an agricultural expert.

    Disease detected:
    {disease_name}

    Provide:

    1. Disease Summary
    2. Treatment
    3. Prevention
    4. Farmer Tips

    Keep it practical and easy to understand.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content