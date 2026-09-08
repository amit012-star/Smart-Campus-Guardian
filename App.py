import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px

from database import (
    create_database,
    add_emergency,
    get_emergencies,
    update_status,
    assign_team,
    authenticate_user
)

from ai_engine import analyze_emergency


# =====================================================
# SETUP
# =====================================================

st.set_page_config(
    page_title="Smart Campus Guardian",
    page_icon="🛡️",
    layout="wide"
)

create_database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""


# =====================================================
# FRONT PAGE
# =====================================================

if not st.session_state.logged_in:

    st.title("🛡️ Smart Campus Guardian")

    st.subheader(
        "🎓 AI-Based College Emergency & Safety Management System"
    )

    st.write(
        "🚨 Report emergencies • 🤖 AI Analysis • 👥 Quick Response • 📊 Smart Monitoring"
    )

    st.divider()

    st.header("✨ Smart Safety Features")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info(
            "🚨 **Emergency Reporting**\n\n"
            "Report accidents, medical, fire and security emergencies."
        )

    with c2:
        st.info(
            "🤖 **AI Analysis**\n\n"
            "Automatically identify emergency priority."
        )

    with c3:
        st.info(
            "👥 **Response Teams**\n\n"
            "Assign the right team to handle emergencies."
        )

    with c4:
        st.info(
            "📊 **Smart Analytics**\n\n"
            "Monitor campus emergency trends."
        )

    st.divider()

    st.header("🔐 Secure Login")

    username = st.text_input(
        "👤 Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button(
        "🚀 Login to Smart Campus Guardian",
        use_container_width=True
    ):

        role = authenticate_user(username, password)

        if role:

            st.session_state.logged_in = True
            st.session_state.role = role

            st.success("✅ Login successful!")
            st.rerun()

        else:

            st.error("❌ Invalid username or password.")

    st.divider()

    st.success(
        "🔒 **Secure Campus Platform**\n\n"
        "Only authorized users can access emergency information."
    )

    st.caption(
        "🛡️ Smart Campus Guardian | 🎓 Safer & Smarter Campus"
    )


# =====================================================
# STUDENT DASHBOARD
# =====================================================

elif st.session_state.role == "student":

    st.title("🎓 Student Dashboard")

    st.caption(
        "🚨 Quickly report any emergency or safety issue on campus."
    )

    st.divider()

    st.header("🚨 Report Emergency")

    name = st.text_input(
        "👤 Student Name"
    )

    emergency_type = st.selectbox(
        "🚨 Emergency Type",
        [
            "🏥 Medical",
            "🚑 Accident",
            "🔥 Fire",
            "🛡️ Security",
            "📌 Other"
        ]
    )

    location = st.selectbox(
        "📍 Campus Location",
        [
            "💻 Computer Lab",
            "🏢 Block A",
            "📚 Library",
            "⚽ Ground",
            "🏠 Hostel",
            "🍴 Canteen",
            "🔧 Workshop"
        ]
    )

    location_details = st.text_input(
        "📌 Location Details",
        placeholder="Example: 2nd floor, near Room 204"
    )

    description = st.text_area(
        "📝 Emergency Description",
        placeholder="Describe the emergency clearly..."
    )

    if st.button(
        "🚨 SEND EMERGENCY ALERT
