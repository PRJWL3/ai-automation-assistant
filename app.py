import streamlit as st
import ollama
import requests
import re
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:8000/add_task"

# ==============================
# 🔹 INIT SESSION
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# 🧠 AI TASK (UNCHANGED)
# ==============================
def ai_task(user_input):

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": """
                You are an AI automation assistant.

                Output ONLY:

                Task: <schedule_meeting / summarize_text / send_email / general>
                Details: <clean task>
                """
            },
            {"role": "user", "content": user_input}
        ]
    )

    return response["message"]["content"]

# ==============================
# 🔹 TASK DETECTION
# ==============================
def detect_task(ai_output):
    if "schedule_meeting" in ai_output:
        return "schedule_meeting"
    elif "summarize_text" in ai_output:
        return "summarize_text"
    elif "send_email" in ai_output:
        return "send_email"
    else:
        return "general"

# ==============================
# 🔹 EXTRACT DETAILS
# ==============================
def extract_details(ai_output):
    if "Details:" in ai_output:
        return ai_output.split("Details:")[-1].strip()
    return ai_output

# ==============================
# ⏰ TIME PARSER
# ==============================
def extract_time(text):
    match = re.search(r'(\d{1,2}):?(\d{0,2})\s*(am|pm)', text.lower())

    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        period = match.group(3)

        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0

        now = datetime.now()
        reminder_time = now.replace(hour=hour, minute=minute, second=0)

        if reminder_time < now:
            reminder_time += timedelta(days=1)

        return reminder_time

    return datetime.now()

# ==============================
# ⚙️ EXECUTION AGENT
# ==============================
def execution_agent(task, details):

    if task == "schedule_meeting":

        reminder_time = extract_time(details)

        # ✅ Send to backend
        requests.post(API_URL, json={
            "task": details,
            "time": reminder_time.isoformat()
        })

        return f"""📅 Reminder Scheduled

Task:
{details}

Time:
{reminder_time.strftime("%I:%M %p")}
"""

    elif task == "summarize_text":

        summary = ollama.chat(
            model="llama3",
            messages=[{
                "role": "user",
                "content": f"Summarize this in 2 lines:\n{details}"
            }]
        )

        return f"""📄 Summary

{summary['message']['content']}
"""

    elif task == "send_email":

        email = ollama.chat(
            model="llama3",
            messages=[{
                "role": "user",
                "content": f"Write a professional email for:\n{details}"
            }]
        )

        return f"""📧 Email Draft

{email['message']['content']}
"""

    else:
        return f"""🤖 AI Response

{details}
"""

# ==============================
# 🎨 UI (UNCHANGED STYLE)
# ==============================
st.title("🤖 AI Automation Assistant 🔥")

user_input = st.text_input("Enter your task:")

if user_input:

    ai_output = ai_task(user_input)
    task = detect_task(ai_output)
    details = extract_details(ai_output)

    result = execution_agent(task, details)

    st.subheader("🧠 AI Understanding")
    st.code(ai_output)

    st.subheader("⚙️ Execution")
    st.code(result)

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("AI", result))

# ==============================
# 💬 CHAT HISTORY
# ==============================
st.subheader("💬 Conversation")

for role, msg in st.session_state.history:
    st.write(f"{role}: {msg}")

# ==============================
# 🔴 STOP BUTTON
# ==============================
if st.button("Stop Alarm 🔇"):
    import os
    os.system("taskkill /f /im python.exe")
    st.success("Alarm stopped!")