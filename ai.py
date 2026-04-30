import os
import google.generativeai as genai

# 🔐 ===== API KEY =====
def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except:
        pass

    raise ValueError("❌ GEMINI_API_KEY not found")

genai.configure(api_key=get_api_key())


# 🤖 ===== USE STABLE MODEL =====
model = genai.GenerativeModel("gemini-1.5-flash")


# 🤖 ===== CHAT FUNCTION =====
def chat_with_ai(user_message, savings=0, expenses=None):

    if expenses is None:
        expenses = {}

    # 🧠 MUCH BETTER PROMPT
    prompt = f"""
You are a professional financial advisor helping a user manage money.

Your job:
- Understand the user's intent clearly
- Give practical, step-by-step financial advice
- Personalize advice using user's data
- Be clear, helpful, and slightly detailed
- Use bullet points when useful

User Financial Data:
Savings: ₹{savings}
Expenses: {expenses}

User Question:
{user_message}

Answer in a helpful and structured way.
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 600,
                "top_p": 0.95
            }
        )

        text = response.text.strip()

        # fallback if empty/weak response
        if not text or len(text) < 20:
            return "⚠️ I couldn't generate a proper answer. Try rephrasing your question."

        return text

    except Exception as e:
        return f"❌ AI Error: {str(e)}"