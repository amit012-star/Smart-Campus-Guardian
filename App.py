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
        "🚨 SEND EMERGENCY ALERT",
        use_container_width=True
    ):

        if name and location_details and description:

            priority, action = analyze_emergency(
                emergency_type,
                description
            )

            created_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            add_emergency(
                name,
                emergency_type,
                location,
                location_details,
                description,
                priority,
                "Pending",
                created_at
            )

            st.success(
                "✅ Emergency alert submitted successfully!"
            )

            st.header("🤖 AI Emergency Analysis")

            st.metric(
                "⚠️ Priority",
                priority
            )

            st.info(
                f"🩺 **Recommended Action:** {action}"
            )

        else:

            st.warning(
                "⚠️ Please fill all fields before submitting."
            )

    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()


# =====================================================
# ADMIN DASHBOARD
# =====================================================

elif st.session_state.role == "admin":

    st.title("🛡️ Admin Safety Dashboard")

    st.caption(
        "📊 Central control panel for campus emergency management."
    )

    reports = get_emergencies()

    st.divider()

    # =================================================
    # STATISTICS
    # =================================================

    st.header("📊 Emergency Overview")

    total = len(reports)

    critical = sum(
        1 for r in reports if r[6] == "CRITICAL"
    )

    important = sum(
        1 for r in reports if r[6] == "IMPORTANT"
    )

    normal = sum(
        1 for r in reports if r[6] == "NORMAL"
    )

    pending = sum(
        1 for r in reports if r[7] == "Pending"
    )

    resolved = sum(
        1 for r in reports if r[7] == "Resolved"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📋 Total", total)
    c2.metric("🔴 Critical", critical)
    c3.metric("🟠 Important", important)
    c4.metric("🟢 Normal", normal)
    c5.metric("⏳ Pending", pending)

    st.divider()

    # =================================================
    # ANALYTICS
    # =================================================

    st.header("📈 Emergency Analytics")

    if reports:

        type_count = {}

        for r in reports:
            type_count[r[2]] = type_count.get(r[2], 0) + 1

        df = pd.DataFrame(
            type_count.items(),
            columns=["Emergency Type", "Count"]
        )

        fig = px.bar(
            df,
            x="Emergency Type",
            y="Count",
            text="Count",
            title="🚨 Emergency Type Distribution"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "📊 No emergency reports available yet."
        )

    st.divider()

    # =================================================
    # REPORTS
    # =================================================

    st.header("🚨 Emergency Reports")

    if not reports:

        st.info("📭 No reports available.")

    for r in reports:

        with st.expander(
            f"🚨 Report #{r[0]} | {r[2]} | ⚠️ {r[6]}"
        ):

            st.write("👤 **Student:**", r[1])
            st.write("🚨 **Emergency:**", r[2])
            st.write("📍 **Location:**", r[3])
            st.write("📌 **Details:**", r[4])
            st.write("📝 **Description:**", r[5])
            st.write("⚠️ **Priority:**", r[6])
            st.write("🔄 **Status:**", r[7])
            st.write("🕐 **Reported:**", r[8])
            st.write("👥 **Team:**", r[9])

            st.divider()

            teams = [
                "Unassigned",
                "Medical Team",
                "Security Team",
                "Fire Response Team",
                "Maintenance Team"
            ]

            team = st.selectbox(
                "👥 Response Team",
                teams,
                key=f"team_{r[0]}"
            )

            if st.button(
                "👥 Assign Team",
                key=f"assign_{r[0]}"
            ):

                assign_team(r[0], team)

                st.success(
                    "✅ Response team assigned!"
                )

                st.rerun()

            status = st.selectbox(
                "🔄 Update Status",
                [
                    "Pending",
                    "Responded",
                    "Resolved"
                ],
                key=f"status_{r[0]}"
            )

            if st.button(
                "✅ Update Status",
                key=f"update_{r[0]}"
            ):

                update_status(r[0], status)

                st.success(
                    "✅ Status updated successfully!"
                )

                st.rerun()

    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()
