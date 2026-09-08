import streamlit as st
from datetime import datetime
from database import create_database, add_emergency, get_emergencies

st.set_page_config(
    page_title="Smart Campus Guardian",
    page_icon="🚨",
    layout="wide"
)

create_database()


def calculate_priority(emergency_type, description):

    text = (emergency_type + " " + description).lower()

    critical_words = [
        "fire",
        "accident",
        "unconscious",
        "serious",
        "bleeding",
        "danger"
    ]

    for word in critical_words:
        if word in text:
            return "CRITICAL"

    if emergency_type in ["Medical", "Accident", "Security"]:
        return "IMPORTANT"

    return "NORMAL"


def login_page():

    st.title("🚨 Smart Campus Guardian")

    st.subheader(
        "AI-Based College Emergency & Safety Management System"
    )

    st.divider()

    st.header("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "student" and password == "1234":

            st.session_state.logged_in = True
            st.session_state.role = "student"
            st.rerun()

        elif username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.rerun()

        else:
            st.error("Invalid username or password.")


def student_dashboard():

    st.title("🎓 Student Dashboard")

    st.success("Welcome to Smart Campus Guardian!")

    st.divider()

    st.header("🆘 Emergency Report")

    student_name = st.text_input("Student Name")

    emergency_type = st.selectbox(
        "Emergency Type",
        [
            "Medical",
            "Fire",
            "Security",
            "Accident",
            "Other"
        ]
    )

    location = st.selectbox(
        "Campus Location",
        [
            "Computer Lab",
            "Block A",
            "Library",
            "Ground",
            "Hostel",
            "Canteen",
            "Workshop"
        ]
    )

    description = st.text_area(
        "Describe the Emergency"
    )

    if st.button("🚨 SEND EMERGENCY ALERT"):

        if student_name.strip() == "":
            st.warning("Please enter your name.")

        elif description.strip() == "":
            st.warning(
                "Please describe the emergency."
            )

        else:

            priority = calculate_priority(
                emergency_type,
                description
            )

            status = "Pending"

            created_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            add_emergency(
                student_name,
                emergency_type,
                location,
                description,
                priority,
                status,
                created_at
            )

            st.success(
                "🚨 Emergency report submitted successfully!"
            )

            st.info(
                f"Priority assigned: {priority}"
            )

    st.divider()

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()


def admin_dashboard():

    st.title("🛡️ Admin Dashboard")

    st.success("Welcome, Administrator!")

    reports = get_emergencies()

    total_reports = len(reports)

    critical_cases = sum(
        1 for report in reports
        if report[5] == "CRITICAL"
    )

    pending_cases = sum(
        1 for report in reports
        if report[6] == "Pending"
    )

    resolved_cases = sum(
        1 for report in reports
        if report[6] == "Resolved"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 Total Reports",
            total_reports
        )

    with col2:
        st.metric(
            "🚨 Critical Cases",
            critical_cases
        )

    with col3:
        st.metric(
            "⏳ Pending Cases",
            pending_cases
        )

    with col4:
        st.metric(
            "✅ Resolved Cases",
            resolved_cases
        )

    st.divider()

    st.header("📋 Emergency Reports")

    if len(reports) == 0:

        st.info(
            "No emergency reports available."
        )

    else:

        for report in reports:

            st.subheader(
                f"🚨 Report #{report[0]}"
            )

            st.write(
                f"**Student:** {report[1]}"
            )

            st.write(
                f"**Emergency Type:** {report[2]}"
            )

            st.write(
                f"**Location:** {report[3]}"
            )

            st.write(
                f"**Description:** {report[4]}"
            )

            st.write(
                f"**Priority:** {report[5]}"
            )

            st.write(
                f"**Status:** {report[6]}"
            )

            st.write(
                f"**Time:** {report[7]}"
            )

            st.divider()

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


if not st.session_state.logged_in:

    login_page()

elif st.session_state.role == "student":

    student_dashboard()

elif st.session_state.role == "admin":

    admin_dashboard()
