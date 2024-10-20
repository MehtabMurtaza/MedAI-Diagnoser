

GROQ_API_KEY = "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"


import os

from groq import Groq

client = Groq(
    api_key=GROQ_API_KEY,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What category of diseases are there?",
        }
    ],
    model="llama3-8b-8192",
)

# print(chat_completion.choices[0].message.content)


from groq import Groq

client = Groq(
    api_key=GROQ_API_KEY,
)

chat_completion_2 = client.chat.completions.create(
    messages=[
        {
        "role": "user",
        "content": "I am having an headache can you tell me what medicine should I take?"
        }
    ],
    model="llama-guard-3-8b",
)

print(chat_completion_2.choices[0].message.content)