import os
import google.generativeai as genai

# 🔐 ===== API KEY HANDLING =====
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
def get_model():
    try:
        models = genai.list_models()

        valid = [
            m.name for m in models
            if "generateContent" in m.supported_generation_methods
        ]

        # Prefer flash / fast models
        for m in valid:
            if "flash" in m.lower():
                print("✅ Using:", m)
                return genai.GenerativeModel(m)

        # fallback
        if valid:
            print("⚠️ Fallback:", valid[0])
            return genai.GenerativeModel(valid[0])

    except Exception as e:
        print("⚠️ Model detection failed:", e)

    # final fallback
    return genai.GenerativeModel("gemini-pro")


model = get_model()


# 🤖 ===== CONVERSATIONAL CHAT FUNCTION =====
def chat_with_ai(user_message, savings=0, expenses=None, history=None):

    if expenses is None:
        expenses = {}

    if history is None:
        history = []

    # 🧠 Build conversation memory
    conversation = ""
    for msg in history[-6:]:  # last 6 messages only
        role = msg["role"]
        content = msg["content"]
        conversation += f"{role}: {content}\n"

    # 🧠 Strong prompt
    prompt = f"""
You are a professional financial advisor chatbot.

Your behavior:
- Be conversational and friendly
- Understand context from previous messages
- Give clear, structured, and complete answers
- Provide practical financial advice
- Never give incomplete responses

User Financial Data:
Savings: ₹{savings}
Expenses: {expenses}

Conversation History:
{conversation}

User: {user_message}

Respond in this format:

1. Understanding the situation  
2. Key advice  
3. Action steps  
4. Final tip
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 800,
                "top_p": 0.95
            }
        )

        text = response.text.strip()

        # 🛑 Fix incomplete / bad outputs
        if not text or len(text) < 50 or text.endswith("Based"):
            return "⚠️ I couldn't generate a proper answer. Please try again."

        return text

    except Exception as e:
        err = str(e)

        if "429" in err or "quota" in err.lower():
            return "⚠️ API quota exceeded. Please try again later."

        return f"❌ AI Error: {err}"