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


# 🤖 ===== SAFE MODEL SELECTION =====
def get_working_model():
    try:
        models = genai.list_models()

        # Only models that support generateContent
        valid_models = [
            m.name for m in models
            if "generateContent" in m.supported_generation_methods
        ]

        # Prefer safe models (avoid 3.x / pro quota issues)
        preferred_keywords = ["flash", "pro"]

        for keyword in preferred_keywords:
            for m in valid_models:
                if keyword in m.lower():
                    print(f"✅ Using model: {m}")
                    return genai.GenerativeModel(m)

        # fallback
        if valid_models:
            print(f"⚠️ Using fallback model: {valid_models[0]}")
            return genai.GenerativeModel(valid_models[0])

        raise Exception("No valid models found")

    except Exception as e:
        raise Exception(f"❌ Model init failed: {str(e)}")


model = get_working_model()


# 🤖 ===== CHAT FUNCTION =====
def chat_with_ai(user_message, savings=0, expenses=None):

    if expenses is None:
        expenses = {}

    prompt = f"""
You are a professional financial advisor.

Give clear, helpful, and practical advice.

User Data:
Savings: ₹{savings}
Expenses: {expenses}

User Question:
{user_message}

Answer clearly with steps if needed.
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 600
            }
        )

        return response.text.strip()

    except Exception as e:
        return f"❌ AI Error: {str(e)}"