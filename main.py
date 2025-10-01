# main.py
import google.generativeai as genai
import os
import time
from typing import List, Dict

class AIEngine:
    def __init__(self):
        # Initialize with your API key
        self.api_key = "AIzaSyBJtlYGk_oHUq5zmRhc9UnMhmyhmo1I2QA"
        self.configure_ai()
        
        # Learning concepts database
        self.concepts = {
            "Variables": "Basic data storage in programming",
            "Data Types": "Different types of data (int, float, string, bool)",
            "Conditional Statements": "if, elif, else statements",
            "Loops": "for and while loops for repetition",
            "Functions": "Reusable code blocks",
            "Lists": "Ordered collections of items",
            "Dictionaries": "Key-value pair data structures",
            "Classes and Objects": "Object-oriented programming basics",
            "File Handling": "Reading and writing files",
            "Error Handling": "try, except blocks for error management"
        }
        
        # Chat context for maintaining conversation
        self.chat_context = []
        self.current_concept = None
        self.last_request_time = 0
        self.request_delay = 8  # 8 seconds between requests
        
    def configure_ai(self):
        """Configure the Gemini AI with enhanced settings"""
        try:
            genai.configure(api_key=self.api_key)
            # Try different models in order of preference
            try:
                self.model = genai.GenerativeModel('models/gemini-2.5-flash')
                print("🤖 AI Engine initialized with gemini-2.5-flash!")
            except Exception as e:
                try:
                    self.model = genai.GenerativeModel('gemini-pro')
                    print("🤖 AI Engine initialized with gemini-pro!")
                except Exception as e2:
                    print(f"❌ AI Configuration Error: {e2}")
                    self.model = None
        except Exception as e:
            print(f"❌ AI Configuration Error: {e}")
            self.model = None

    def _rate_limit(self):
        """Implement rate limiting to avoid quota issues"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            wait_time = self.request_delay - time_since_last
            print(f"⏳ Rate limiting: waiting {wait_time:.1f} seconds")
            time.sleep(wait_time)
        self.last_request_time = time.time()

    def get_concept_list(self) -> List[str]:
        """Return list of available learning concepts"""
        return ["Select a concept"] + list(self.concepts.keys())

    def reset_chat_context(self, concept: str):
        """Reset chat context when new concept is selected"""
        self.current_concept = concept
        self.chat_context = [{
            "role": "system",
            "content": f"You are CodeCompanion, an expert programming tutor specializing in {concept}. "
                      f"Provide clear, engaging explanations with practical examples. "
                      f"Use analogies and real-world scenarios to make concepts memorable. "
                      f"Be encouraging and patient with learners of all levels. "
                      f"Keep responses concise and focused on the topic."
        }]
        return f"✅ Ready to learn about {concept}! Ask me anything or choose an explanation style."

    def get_explanation(self, concept: str, explanation_type: str) -> str:
        """Get AI explanation based on concept and type"""
        if not self.model:
            return "⚠️ AI service not available. Please check API configuration."

        # Apply rate limiting
        self._rate_limit()

        prompt_templates = {
            "Funny Real-World Example": 
                f"Explain '{concept}' using a funny, memorable real-world analogy. "
                f"Make it entertaining but educational. Include a simple code example. Keep response under 150 words.",
                
            "Technical Definition": 
                f"Provide a precise technical definition of '{concept}'. "
                f"Include key characteristics, syntax (if applicable), and common use cases. "
                f"Be concise but comprehensive. Keep response under 100 words.",
                
            "Pseudocode Example": 
                f"Explain '{concept}' using clear pseudocode first, then show a Python implementation. "
                f"Focus on the logical structure and step-by-step process. Keep response under 120 words.",
                
            "Comprehensive Explanation": 
                f"Give a complete beginner-friendly explanation of '{concept}'. "
                f"Cover: 1) What it is 2) Why it's important 3) How to use it 4) Common pitfalls 5) Best practices. "
                f"Keep response under 200 words.",
                
            "Wikipedia Search": 
                f"Provide a Wikipedia-style overview of '{concept}'. "
                f"Include: Definition, History (if relevant), Key Features, Examples, and Related Concepts. "
                f"Keep response under 150 words.",
                
            "Documentation": 
                f"Create official-style documentation for '{concept}'. "
                f"Include: Purpose, Syntax, Parameters, Return Values, Examples, and Notes. "
                f"Keep response under 120 words.",
                
            "Syntax": 
                f"Focus specifically on the syntax of '{concept}'. "
                f"Show different variations with examples. Highlight common syntax errors to avoid. "
                f"Keep response under 100 words."
        }

        if explanation_type not in prompt_templates:
            return f"❌ Unknown explanation type: {explanation_type}"

        try:
            prompt = prompt_templates[explanation_type]
            full_prompt = f"Concept: {concept}\n\n{prompt}"
            
            # Add to chat context
            self.chat_context.append({"role": "user", "content": full_prompt})
            
            response = self.model.generate_content(full_prompt)
            explanation = response.text
            
            # Add to chat context
            self.chat_context.append({"role": "assistant", "content": explanation})
            
            return explanation
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                return "⚠️ API quota exceeded. Please wait a minute and try again."
            elif "503" in error_msg:
                return "⚠️ Service temporarily unavailable. Please try again in a moment."
            else:
                return f"❌ Error generating explanation: {error_msg}"

    def chat_with_ai(self, user_message: str) -> str:
        """Chat with AI about the current concept - FIXED VERSION"""
        if not self.model:
            return "⚠️ AI service not available. Please check API configuration."

        if not self.current_concept:
            return "⚠️ Please select a learning concept first!"

        if not user_message.strip():
            return "Please type a question."

        # Apply rate limiting
        self._rate_limit()

        try:
            # Add user message to context
            self.chat_context.append({"role": "user", "content": user_message})
            
            # Create a simpler, more direct prompt for chat
            chat_prompt = f"""As a programming tutor specializing in {self.current_concept}, answer this question clearly and helpfully:

User Question: {user_message}

Context: We're discussing {self.current_concept} in programming.

Please provide a helpful, concise answer with practical examples if relevant."""
            
            print(f"🤖 Sending chat request for: {user_message[:50]}...")  # Debug log
            
            response = self.model.generate_content(chat_prompt)
            ai_response = response.text
            
            print(f"🤖 Received chat response: {ai_response[:50]}...")  # Debug log
            
            # Add AI response to context
            self.chat_context.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Chat error details: {error_msg}")  # Debug log
            if "quota" in error_msg.lower() or "429" in error_msg:
                return "⚠️ API quota exceeded. Please wait a minute and try again."
            elif "503" in error_msg:
                return "⚠️ Service temporarily unavailable. Please try again in a moment."
            elif "500" in error_msg:
                return "⚠️ Internal server error. Please try again in a moment."
            else:
                return f"❌ Error in chat: {error_msg}"

    def get_local_explanation(self, concept: str, explanation_type: str) -> str:
        """Provide local explanations without API calls"""
        local_explanations = {
            "Variables": {
                "Funny Real-World Example": "Think of variables like labeled boxes! 🎁 'age = 25' is like putting 25 in a box labeled 'age'. You can change what's inside anytime! In Python: name = 'Alice', score = 100",
                "Technical Definition": "Variables are named storage locations in memory that hold data values. They have a name, type, and value. Python is dynamically typed, so types are inferred.",
                "Syntax": "Python syntax: variable_name = value\nExamples:\nname = 'Alice'  # String\nage = 25        # Integer\nprice = 19.99   # Float\nis_student = True  # Boolean"
            },
            "Functions": {
                "Funny Real-World Example": "Functions are like kitchen appliances! 🍳 A blender (function) takes ingredients (parameters) and returns a smoothie (result). def make_smoothie(fruits): return 'Yummy smoothie!'",
                "Technical Definition": "Functions are reusable code blocks that perform specific tasks. They take inputs (parameters), process them, and return outputs. They help avoid code repetition.",
                "Syntax": "def function_name(parameters):\n    # code block\n    return result\n\nExample:\ndef greet(name):\n    return f'Hello, {name}!'"
            },
            "Loops": {
                "Funny Real-World Example": "Loops are like a DJ repeating your favorite song! 🔄 'for song in playlist: play(song)' keeps playing until the playlist ends.",
                "Technical Definition": "Loops repeatedly execute a block of code. 'for' loops iterate over sequences, 'while' loops run while a condition is true.",
                "Syntax": "For loop:\nfor item in sequence:\n    # code\n\nWhile loop:\nwhile condition:\n    # code"
            }
        }
        
        if concept in local_explanations and explanation_type in local_explanations[concept]:
            return f"📚 {concept} - {explanation_type}:\n\n{local_explanations[concept][explanation_type]}"
        
        return None

    def get_learning_progress(self) -> Dict:
        """Get user's learning progress"""
        return {
            "current_concept": self.current_concept,
            "chat_messages": len(self.chat_context) // 2,
            "concepts_covered": list(self.concepts.keys())[:3] if self.current_concept else []
        }


# Test the AI Engine with chat specifically
if __name__ == "__main__":
    ai = AIEngine()
    print("Available concepts:", ai.get_concept_list())
    
    if ai.model:
        print("\n🧪 TESTING CHAT FUNCTIONALITY...")
        
        # Test chat specifically
        ai.reset_chat_context("Variables")
        print("✅ Chat context reset")
        
        # Test chat directly
        chat_response = ai.chat_with_ai("What are variables in programming?")
        print("\n💬 Chat Response:")
        print(chat_response)
        
        # Test another chat
        chat_response2 = ai.chat_with_ai("Can you give me an example?")
        print("\n💬 Second Chat Response:")
        print(chat_response2)
    else:
        print("❌ AI Engine failed to initialize")