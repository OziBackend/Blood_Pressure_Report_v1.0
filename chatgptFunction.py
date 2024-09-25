import os
from openai import OpenAI

from authKeys import keys

os.environ["OPENAI_API_KEY"] = keys["openAI"]

client = OpenAI()

def search_gpt(prompt):
    try:
        completion = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a helpful Physician, who will help me with how to improve health outcomes  ",
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                    )
        completed_data = completion.choices[0].message.content
        
        # print('Chat GPT Response',completed_data)
        return completed_data
    except Exception as e:
        print(e)
        return []
    
