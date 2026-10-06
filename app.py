```python
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Configuration
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="AI Smart Tutor",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Gemini Client
# -----------------------------
if not API_KEY:
    st.error("GEMINI_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# -----------------------------
# AI Function
# -----------------------------
def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"


# -----------------------------
# Session State
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "questions" not in st.session_state:
    st.session_state.questions = 0


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🎓 AI Smart Tutor")

menu = st.sidebar.radio(
    "Choose an option",
    [
        "🏠 Home",
        "🤖 AI Tutor",
        "📚 Notes",
        "📝 Quiz",
        "💡 Hint",
        "📊 Progress"
    ]
)


# =====================================================
# HOME
# =====================================================
if menu == "🏠 Home":

    st.title("🎓 AI-Powered Smart Tutor")

    st.subheader("Your Personal AI Learning Assistant 🤖")

    st.write(
        "Learn subjects, generate notes, practice quizzes, "
        "get hints and track your learning progress."
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Questions Attempted", st.session_state.questions)

    with col2:
        st.metric("Correct Answers", st.session_state.score)

    with col3:
        if st.session_state.questions > 0:
            percentage = (
                st.session_state.score /
                st.session_state.questions
            ) * 100
        else:
            percentage = 0

        st.metric("Accuracy", f"{percentage:.1f}%")

    st.markdown("---")

    st.info(
        "Use the sidebar to ask questions, generate notes, "
        "practice quizzes and check your progress."
    )


# =====================================================
# AI TUTOR
# =====================================================
elif menu == "🤖 AI Tutor":

    st.title("🤖 AI Tutor")

    subject = st.selectbox(
        "Select Subject",
        [
            "Python",
            "Java",
            "Data Structures",
            "Database Management",
            "Operating Systems",
            "Computer Networks",
            "Software Engineering",
            "Data Science"
        ]
    )

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    topic = st.text_input(
        "Enter the topic you want to learn"
    )

    if st.button("🤖 Explain Topic"):

        if topic:

            prompt = f"""
You are an intelligent college AI tutor.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Explain the topic clearly.

Give:
1. Simple definition
2. Detailed explanation
3. Easy example
4. Real-world application
5. Important points
6. Three practice questions

Use simple student-friendly language.
"""

            with st.spinner("AI Tutor is thinking..."):

                answer = ask_ai(prompt)

            st.markdown("### 📖 AI Explanation")
            st.write(answer)

        else:
            st.warning("Please enter a topic.")


# =====================================================
# NOTES
# =====================================================
elif menu == "📚 Notes":

    st.title("📚 AI Notes Generator")

    subject = st.selectbox(
        "Subject",
        [
            "Python",
            "Java",
            "Data Structures",
            "Operating Systems",
            "DBMS",
            "Computer Networks",
            "Data Science"
        ]
    )

    topic = st.text_input("Enter topic")

    if st.button("📚 Generate Notes"):

        if topic:

            prompt = f"""
Create easy college notes.

Subject: {subject}
Topic: {topic}

Include:

1. Definition
2. Introduction
3. Main concepts
4. Important points
5. Example
6. Advantages
7. Applications
8. Short conclusion

Use headings and bullet points.
Keep the language simple.
"""

            with st.spinner("Generating notes..."):

                notes = ask_ai(prompt)

            st.markdown("### 📖 Your Notes")
            st.write(notes)

        else:
            st.warning("Please enter a topic.")


# =====================================================
# QUIZ
# =====================================================
elif menu == "📝 Quiz":

    st.title("📝 AI Quiz Generator")

    subject = st.selectbox(
        "Select Subject",
        [
            "Python",
            "Java",
            "Data Structures",
            "DBMS",
            "Operating Systems"
        ]
    )

    topic = st.text_input("Quiz Topic")

    number = st.slider(
        "Number of Questions",
        1,
        5,
        3
    )

    if st.button("📝 Generate Quiz"):

        if topic:

            prompt = f"""
Create {number} multiple-choice questions.

Subject: {subject}
Topic: {topic}

For every question provide:

Question
A
B
C
D
Correct Answer

Do not give explanations.
"""

            with st.spinner("Generating quiz..."):

                quiz = ask_ai(prompt)

            st.markdown("### 📝 Generated Quiz")

            st.write(quiz)

            st.session_state.questions += number

        else:
            st.warning("Please enter a topic.")


# =====================================================
# HINT
# =====================================================
elif menu == "💡 Hint":

    st.title("💡 AI Hint System")

    question = st.text_area(
        "Enter your question"
    )

    if st.button("💡 Get Hint"):

        if question:

            prompt = f"""
You are a helpful tutor.

Student question:
{question}

Give ONLY a useful hint.

Do not directly give the final answer.
Help the student think about the solution.
"""

            with st.spinner("Preparing hint..."):

                hint = ask_ai(prompt)

            st.markdown("### 💡 Hint")
            st.write(hint)

        else:
            st.warning("Please enter a question.")


# =====================================================
# PROGRESS
# =====================================================
elif menu == "📊 Progress":

    st.title("📊 Learning Progress")

    questions = st.session_state.questions
    correct = st.session_state.score

    if questions > 0:
        accuracy = (correct / questions) * 100
    else:
        accuracy = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Questions",
            questions
        )

    with col2:
        st.metric(
            "Correct",
            correct
        )

    with col3:
        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%"
        )

    st.markdown("---")

    if accuracy >= 80:
        st.success(
            "🎉 Excellent performance! Keep learning."
        )

    elif accuracy >= 60:
        st.info(
            "👍 Good performance. Practice a little more."
        )

    else:
        st.warning(
            "📚 Keep practicing. You can improve!"
        )
```
