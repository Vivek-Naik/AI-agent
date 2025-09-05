from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

# Configure Gemini
gemini_api_key = os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
    print("Please create a .env file with your Google API key:")
    print("GOOGLE_API_KEY=your_google_api_key_here")
    exit(1)

# Configure Gemini
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

print("🤖 Gemini Chatbot is ready!")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("👋 Goodbye!")
        break
    
    try:
        response = model.generate_content(user_input)
        print(f"Gemini: {response.text}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
