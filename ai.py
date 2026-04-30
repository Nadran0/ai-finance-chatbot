import os
import google.generativeai as genai


def get_api_key():
    
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key


    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except:
        pass

    raise ValueError("❌ GEMINI_API_KEY not found in environment or Streamlit secrets")



genai.configure(api_key=get_api_key())


def select_model():
    try:
        models = genai.list_models()

        
        preferred = [
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]

        available = [
            m.name for m in models
            if "generateContent" in m.supported_generation_methods
        ]

        
        for p in preferred:
            for m in available:
                if p in m:
                    print(f"✅ Using model: {m}")
                    return genai.GenerativeModel(m)

        
        if available:
            print(f"⚠️ Fallback model: {available[0]}")
            return genai.GenerativeModel(available[0])

    except Exception as e:
        print("⚠️ Model detection failed:", e)

    
    print("⚠️ Using default safe model: gemini-1.5-flash")
    return genai.GenerativeModel("gemini-1.5-flash")



model = select_model()



def is_finance_query(user_message):
    keywords = [
        "money", "finance", "expense", "income",
        "save", "budget", "investment", "loan",
        "debt", "spending"
    ]
    return any(word in user_message.lower() for word in keywords)


def chat_with_ai(user_message, savings=0, expenses=None):

    if expenses is None:
        expenses = {}

    
    if not is_finance_query(user_message):
        return "❌ I can only answer finance-related questions."

    
    prompt = f"""
You are an expert financial advisor.

Rules:
- Answer ONLY finance-related questions
- Give detailed, practical advice
- Use bullet points where helpful
- Keep explanation clear and actionable

User Data:
Savings: ₹{savings}
Expenses: {expenses}

User Question:
{user_message}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500,
                "top_p": 0.95,
                "top_k": 50
            }
        )

        return response.text.strip()

    except Exception as e:
        error_msg = str(e)


        if "429" in error_msg or "quota" in error_msg.lower():
            return "⚠️ API quota exceeded. Please try again later."

        return f"❌ API Error: {error_msg}"