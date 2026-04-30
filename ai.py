import os
import google.generativeai as genai

API_KEY = "AIzaSyBmFCmv6kwMWBVjw-7RtHLnD3F2pxwhrgQ"



if not API_KEY:
    raise ValueError("❌ Gemini API key not found. Please set it in ai.py or as environment variable.")


genai.configure(api_key=API_KEY)


try:
    models = genai.list_models()

    usable_model = None
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            usable_model = m.name
            break

    if not usable_model:
        raise Exception("No supported Gemini model found.")

    model = genai.GenerativeModel(usable_model)

except Exception as e:
    raise Exception(f"❌ Model initialization failed: {str(e)}")



def chat_with_ai(user_message, savings=0, expenses=None):
    """
    Gemini-powered financial chatbot
    """

    if expenses is None:
        expenses = {}

   
    context = f"""
You are a smart financial assistant.

User Financial Data:
- Savings: ₹{savings}
- Expense Breakdown: {expenses}

Your job:
- Give practical financial advice
- Suggest savings improvements
- Help manage money better
- Keep answers short, clear, and actionable
"""

    try:
        response = model.generate_content(
            context + "\nUser: " + user_message
        )

        
        if hasattr(response, "text"):
            return response.text.strip()
        else:
            return str(response)

    except Exception as e:
        return f"❌ AI Error: {str(e)}"