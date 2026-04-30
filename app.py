import streamlit as st
from logic import *
from ai import chat_with_ai  

st.set_page_config(page_title="AI Finance Bot", layout="wide")

st.title("💰 AI Financial Chatbot App")


st.sidebar.header("📥 Income")
income_input = st.sidebar.number_input("Monthly Income", 0.0)

if st.sidebar.button("Save Income"):
    add_income(income_input)
    st.sidebar.success("Income Saved!")

if st.sidebar.button("Reset Income"):
    reset_income()
    st.sidebar.success("Income Reset!")


st.header("🧾 Add Expense")

col1, col2, col3 = st.columns(3)

name = col1.text_input("Expense Name")
amount = col2.number_input("Amount", 0.0)
category = col3.selectbox("Category", ["Food", "Rent", "Travel", "Other"])

if st.button("Add Expense"):
    add_expense(name, amount, category)
    st.success("Expense Added!")


st.header("📊 Financial Overview")

income, total, savings, breakdown = get_summary()

col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{income}")
col2.metric("Expenses", f"₹{total}")
col3.metric("Savings", f"₹{savings}")

st.subheader("📊 Expense Distribution")

if breakdown:
    st.bar_chart(breakdown)
else:
    st.info("No expenses added yet.")

st.header("🎯 Financial Goal")

goal = st.number_input("Goal Amount", 0.0)
months = st.slider("Time (months)", 1, 60)

if st.button("Generate Plan"):
    monthly, gap = calculate_goal(goal, months, savings)

    st.write(f"Required per month: ₹{monthly:.2f}")

    if gap > 0:
        st.error(f"Need ₹{gap:.2f} more per month")
    else:
        st.success("On track 🎯")


st.header("✏️ Manage Expenses")

data = load_data()

for i, exp in enumerate(data["expenses"]):
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.write(exp["name"])
    col2.write(f"₹{exp['amount']}")
    col3.write(exp.get("category", "Other"))

    if col4.button("Delete", key=f"del{i}"):
        delete_expense(i)
        st.rerun()

    if col5.button("Edit", key=f"edit{i}"):
        st.session_state["edit_index"] = i

if "edit_index" in st.session_state:
    idx = st.session_state["edit_index"]
    exp = data["expenses"][idx]

    st.subheader("Edit Expense")

    new_name = st.text_input("Name", exp["name"])
    new_amount = st.number_input("Amount", value=float(exp["amount"]))
    new_category = st.selectbox(
        "Category",
        ["Food", "Rent", "Travel", "Other"],
        index=["Food", "Rent", "Travel", "Other"].index(exp.get("category", "Other"))
    )

    if st.button("Save Changes"):
        edit_expense(idx, new_name, new_amount, new_category)
        del st.session_state["edit_index"]
        st.success("Updated!")
        st.rerun()


st.markdown("## 💬 AI Financial Assistant 🤖")
st.caption("Ask anything about saving, investing, or buying smarter")

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about your finances...")

if user_input:
   
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    
    income, total, savings, breakdown = get_summary()

   
    response = chat_with_ai(
        user_message=user_input,
        savings=savings,
        expenses=breakdown
    )

    
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)