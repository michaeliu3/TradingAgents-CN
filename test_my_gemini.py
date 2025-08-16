import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
print("🧪 Starting Google AI connection test...")

# 1. Check if the API key is available from your .env file
api_key = os.getenv('GOOGLE_API_KEY')

if api_key:
    print(f"✅ Google API Key found: {api_key[:8]}...")
    try:
        # 2. Test creating an instance of the specific model
        print("   Attempting to create 'gemini-2.5-pro' model instance...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro", # Specifically testing this model
            google_api_key=api_key
        )
        print("✅ SUCCESS: Google AI model 'gemini-2.5-pro' was created successfully.")
        
        # 3. Test a simple API call
        print("\n   Sending a test message to the model...")
        response = llm.invoke("Hello, who are you?")
        if response and response.content:
            print(f"✅ SUCCESS: Received a response from the model:\n   '{response.content[:80]}...'")
        else:
            print("❌ FAILED: Model created, but the response was empty.")

    except Exception as e:
        print(f"\n❌ FAILED: Could not use the 'gemini-2.5-pro' model. Error: {e}")

else:
    print("⚠️ FAILED: Could not find the GOOGLE_API_KEY in your environment. Please check your .env file.")