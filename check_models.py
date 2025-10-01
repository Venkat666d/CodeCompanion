import os
import google.generativeai as genai
from dotenv import load_dotenv

print("Attempting to list available models...")

try:
    # Load the secret API key from the .env file
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        print("\nERROR: GEMINI_API_KEY not found in .env file.")
        print("Please make sure your .env file is correct.")
    else:
        # Configure the generative AI model with the API key
        genai.configure(api_key=GEMINI_API_KEY)

        print("\nSuccessfully configured. Fetching models...\n")
        
        # List all models and find the ones that support 'generateContent'
        print("--- Models available to your API key ---")
        found_models = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
                found_models = True
        
        if not found_models:
            print("\nNo models supporting generateContent found for your key.")
            print("This might indicate an issue with the project setup or permissions.")
        print("----------------------------------------")


except Exception as e:
    print(f"\nAN ERROR OCCURRED WHILE RUNNING THE SCRIPT:")
    print(e)