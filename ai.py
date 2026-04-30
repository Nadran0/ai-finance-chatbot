import os
import google.generativeai as genai


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Set it in Streamlit Secrets.")

genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-1.5-flash")


def chat_with_ai(user_message, savings=0, expenses=None):

    if expenses is None:
        expenses = {}

    prompt = f"""
You are a financial assistant.

Give detailed, helpful advice.

User Data:
Savings: ₹{savings}
Expenses: {expenses}

User: {user_message}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )

        return response.text.strip()

    except Exception as e:
        return f"❌ API Error: {str(e)}"