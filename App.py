import streamlit as st
from datetime import datetime

from database import (
    create_database,
    add_emergency,
    get_emergencies,
    update_status
)

from ai_engine import analyze_emergency


# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="Smart Campus Guardian",
    page_icon="🛡️",
    layout="wide"
)


# --------------------------------
# CREATE DATABASE
# --------------------------------

create_database()


# --------------------------------
# PRIORITY SYSTEM
# --------------------------------

def calculate_priority(emergency_type, description):

    text = (
        emergency_type + " " + description
    ).lower()

    critical_words = [
        "fire",
        "accident",
        "unconscious",
        "serious",
        "bleeding",
        "danger",
        "emergency",
        "critical"
    ]

    important_words = [
        "injury",
        "injured",
        "pain",
        "security",
        "threat",
        "medical",
        "help"
    ]

    for word in critical_words:

        if word in text:
            return "CRITICAL"

    for word in important_words:

        if word in text:
            return "IMPORTANT"

    return "NORMAL"


# --------------------------------
# SESSION STATE
# --------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""


# --------------------------------
# LOGIN PAGE
# --------------------------------

if not st.session_state.logged_in:

    st.title("🛡️ Smart Campus Guardian")

    st.subheader(
        "College Emergency & Safety Management System"
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("🔐 Login"):

        if username == "student" and password == "1234":

            st.session_state.logged_in = True
            st.session_state.role = "student"

            st.rerun()

        elif username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.session_state.role = "admin"

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )


# --------------------------------
# STUDENT DASHBOARD
# --------------------------------

elif st.session_state.role == "student":

    st.title("🎓 Student Emergency Dashboard")

    st.write(
        "Report any emergency or safety issue on campus."
    )

    student_name = st.text_input(
        "Student Name"
    )

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
        "📍 Campus Location",
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

    location_details = st.text_input(
        "📍 Location Details",
        placeholder="Example: 2nd floor, near Room 204"
    )

    description = st.text_area(
        "Emergency Description",
        placeholder="Describe the emergency clearly..."
    )

    if st.button("🚨 Send Emergency Alert"):

        if (
            student_name
            and location
            and location_details
            and description
        ):

            # AI emergency analysis
            ai_priority, recommended_action = analyze_emergency(
                emergency_type,
                description
            )

            # Save AI priority
            priority = ai_priority

            created_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Save emergency report
            add_emergency(
                student_name,
                emergency_type,
                location,
                location_details,
                description,
                priority,
                "Pending",
                created_at
            )

            st.success(
                "Emergency alert submitted successfully!"
            )

            # --------------------------------
            # AI ANALYSIS RESULT
            # --------------------------------

            st.subheader(
                "🤖 AI Emergency Analysis"
            )

            st.write(
                f"**AI Priority:** {ai_priority}"
            )

            st.write(
                f"**Recommended Action:** {recommended_action}"
            )

        else:

            st.warning(
                "Please fill all fields."
            )

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()


# --------------------------------
# ADMIN DASHBOARD
# --------------------------------

elif st.session_state.role == "admin":

    st.title("🛡️ Admin Safety Dashboard")

    reports = get_emergencies()

    # --------------------------------
    # ANALYTICS
    # --------------------------------

    total_reports = len(reports)

    critical_cases = sum(
        1
        for report in reports
        if report[6] == "CRITICAL"
    )

    important_cases = sum(
        1
        for report in reports
        if report[6] == "IMPORTANT"
    )

    normal_cases = sum(
        1
        for report in reports
        if report[6] == "NORMAL"
    )

    pending_cases = sum(
        1
        for report in reports
        if report[7] == "Pending"
    )

    resolved_cases = sum(
        1
        for report in reports
        if report[7] == "Resolved"
    )

    # --------------------------------
    # ANALYTICS CARDS
    # --------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Reports",
        total_reports
    )

    col2.metric(
        "🔴 Critical Cases",
        critical_cases
    )

    col3.metric(
        "🟠 Important Cases",
        important_cases
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🟢 Normal Cases",
        normal_cases
    )

    col2.metric(
        "⏳ Pending",
        pending_cases
    )

    col3.metric(
        "✅ Resolved",
        resolved_cases
    )

    st.divider()

    # --------------------------------
    # EMERGENCY REPORTS
    # --------------------------------

    st.subheader(
        "🚨 Emergency Reports"
    )

    if not reports:

        st.info(
            "No emergency reports available."
        )

    else:

        for report in reports:

            st.markdown("---")

            st.write(
                f"### 🚨 Report #{report[0]}"
            )

            st.write(
                f"**Student:** {report[1]}"
            )

            st.write(
                f"**Emergency Type:** {report[2]}"
            )

            st.write(
                f"**Campus Location:** {report[3]}"
            )

            st.write(
                f"**Location Details:** {report[4]}"
            )

            st.write(
                f"**Description:** {report[5]}"
            )

            st.write(
                f"**Priority:** {report[6]}"
            )

            st.write(
                f"**Current Status:** {report[7]}"
            )

            st.write(
                f"**Reported At:** {report[8]}"
            )

            new_status = st.selectbox(
                "Update Status",
                [
                    "Pending",
                    "Responded",
                    "Resolved"
                ],
                index=[
                    "Pending",
                    "Responded",
                    "Resolved"
                ].index(report[7]),
                key=f"status_{report[0]}"
            )

            if st.button(
                "Update Status",
                key=f"update_{report[0]}"
            ):

                update_status(
                    report[0],
                    new_status
                )

                st.success(
                    "Status updated successfully!"
                )

                st.rerun()

    # --------------------------------
    # LOGOUT
    # --------------------------------

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()
