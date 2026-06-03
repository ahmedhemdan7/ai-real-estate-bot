from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def extract_lead(conversation):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Extract lead information from the conversation.

Return ONLY valid JSON.
"""
            },
            {
                "role": "user",
                "content": conversation
            }
        ]
    )

    return response.choices[0].message.content