import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Initialize the client
# Note: The new SDK automatically looks for the GEMINI_API_KEY environment variable. 
# If your .env uses GEMINI_API_KEY, you can just do: client = genai.Client()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Generate content
response = client.models.generate_content(
    model="gemini-3-flash-preview",  # Updated to the stable 2.5 flash model
    contents="Say hello in one sentence."
)

print(response.text)