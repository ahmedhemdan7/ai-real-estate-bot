from save_lead import save_lead
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from conversation import get_messages, save_messages
from lead_extractor import extract_lead
from pydantic import BaseModel
import json
import os
class ChatRequest(BaseModel):
    user_id: str
    message: str

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI()

@app.post("/chat")
def chat(data: ChatRequest):

    user_id = data.user_id
    message = data.message

    history = get_messages(user_id)

    full_conversation = history + f"\nUser: {message}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are PropertyBot AI.

                Collect:
                - Name
                - Phone
                - Budget
                - Location
                - Property Type
                - Bedrooms

                Ask one question at a time.

                When all information is collected,
                say THANK_YOU_COMPLETE.
                """
            },
            {
                "role": "user",
                "content": full_conversation
            }
        ]
    )

    reply = response.choices[0].message.content

    full_conversation += f"\nAssistant: {reply}"

    save_messages(user_id, full_conversation)

    if "THANK_YOU_COMPLETE" in reply:

        lead_data = extract_lead(full_conversation)

        lead = json.loads(lead_data)

        save_lead(
            lead["name"],
            lead["phone"],
            int(lead["budget"]),
            lead["location"],
            lead["property_type"],
            int(lead["bedrooms"])
        )

        return {
            "reply": reply,
            "lead": lead,
            "saved": True
        }

    return {
        "reply": reply
    }