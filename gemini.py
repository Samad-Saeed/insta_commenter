import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables or .env file")

genai.configure(api_key=api_key)

# Function to get a short response
def get_short_reply(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    # Extract the response text and limit it to 15 words
    reply = response.text
    return reply

# Main program loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter your prompt (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        reply = get_short_reply(user_input)
        print("Reply:", reply)
