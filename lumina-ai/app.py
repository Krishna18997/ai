import streamlit as st
from database.auth import create_user, login_user
from database.stats import add_xp, get_stats
from utils.gemini_client import get_gemini_response

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Lumina AI",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------
# SESSION STATE
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------------------
# HEADER
# ----------------------------
st.title("🧠 Lumina AI")
st.subheader("Illuminating the Path to Intelligent Learning")

# ==================================================
# LOGIN / SIGNUP
# ==================================================
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    # ----------------------------
    # SIGNUP
    # ----------------------------
    if menu == "Signup":
        st.header("Create Account")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Signup"):
            if not username or not password:
                st.error("Please enter username and password.")
            else:
                success = create_user(
                    username,
                    password
                )

                if success:
                    st.success(
                        "Account created successfully!"
                    )
                else:
                    st.error(
                        "Username already exists!"
                    )

    # ----------------------------
    # LOGIN
    # ----------------------------
    else:
        st.header("Login")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):
            user = login_user(
                username,
                password
            )

            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error(
                    "Invalid Username or Password"
                )

# ==================================================
# MAIN APP
# ==================================================
else:

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.success(
        f"Welcome back, {st.session_state.username}! 🚀"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Command Center",
        "💬 Study Engine",
        "🎯 Assessment Zone",
        "🚨 Exam Night"
    ])

    # =====================================
    # TAB 1 : COMMAND CENTER
    # =====================================
    with tab1:

        st.header("🏠 Command Center")

        stats = get_stats(
            st.session_state.username
        )

        xp = stats[0]
        streak = stats[1]
        sessions = stats[2]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("⭐ XP", xp)

        with col2:
            st.metric("🔥 Streak", streak)

        with col3:
            st.metric("📚 Sessions", sessions)

        st.divider()

        st.subheader(
            f"Welcome, {st.session_state.username} 👋"
        )

        st.info(
            "Keep studying to increase your XP and learning streak."
        )

    # =====================================
    # TAB 2 : STUDY ENGINE
    # =====================================
    with tab2:

        st.header("💬 Study Engine")

        mode = st.radio(
            "Choose Learning Mode",
            [
                "🧠 Deep Dive",
                "🧒 Explain Like I'm 10",
                "📝 Notes Simplifier",
                "🃏 Flashcards"
            ],
            horizontal=True
        )

        user_input = st.text_area(
            "Enter your topic/question"
        )

        if st.button("Generate Response"):

            if not user_input.strip():
                st.warning(
                    "Please enter a topic."
                )

            else:

                if mode == "🧠 Deep Dive":
                    prompt = f"""
Explain this topic in detail.

Topic:
{user_input}
"""

                elif mode == "🧒 Explain Like I'm 10":
                    prompt = f"""
Explain this topic like I am 10 years old.

Topic:
{user_input}
"""

                elif mode == "📝 Notes Simplifier":
                    prompt = f"""
Convert this into short notes:

{user_input}
"""

                else:
                    prompt = f"""
Create flashcards for:

{user_input}
"""

                with st.spinner(
                    "Lumina is thinking..."
                ):
                    answer = get_gemini_response(
                        prompt
                    )

                add_xp(
                    st.session_state.username,
                    5
                )

                st.write(answer)

    # =====================================
    # TAB 3 : ASSESSMENT ZONE
    # =====================================
    with tab3:

        st.header("🎯 Assessment Zone")

        subject = st.text_input(
            "Enter Subject"
        )

        if st.button("Start Viva"):

            if subject:

                prompt = f"""
Act as a college viva examiner.

Subject:
{subject}

Ask only one viva question.
"""

                with st.spinner(
                    "Preparing Viva..."
                ):
                    question = (
                        get_gemini_response(
                            prompt
                        )
                    )

                st.session_state.viva_question = (
                    question
                )

        if "viva_question" in st.session_state:

            st.info(
                st.session_state.viva_question
            )

            student_answer = st.text_area(
                "Your Answer"
            )

            if st.button(
                "Evaluate Answer"
            ):

                prompt = f"""
Question:
{st.session_state.viva_question}

Student Answer:
{student_answer}

Evaluate and score out of 10.
"""

                with st.spinner(
                    "Evaluating..."
                ):
                    feedback = (
                        get_gemini_response(
                            prompt
                        )
                    )

                st.success(feedback)

    # =====================================
    # TAB 4 : EXAM NIGHT
    # =====================================
    with tab4:

        st.header("🚨 Exam Night Mode")

        subject = st.text_input(
            "Enter Subject",
            key="exam_subject"
        )

        if st.button(
            "🚨 EXAM TOMORROW"
        ):

            if subject:

                prompt = f"""
Subject:
{subject}

Generate:
1. 1 Hour Revision Plan
2. Most Important Topics
3. 5 Expected Questions
4. Last Minute Notes
"""

                with st.spinner(
                    "Generating..."
                ):
                    result = (
                        get_gemini_response(
                            prompt
                        )
                    )

                st.success(result)
