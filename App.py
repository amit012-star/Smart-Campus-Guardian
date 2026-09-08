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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Campus Guardian",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.title("🛡️ Smart Campus Guardian")

    st.subheader(
        "College Emergency & Safety Management System"
    )

    st.write(
        "A smart platform for reporting, managing and responding "
        "to campus emergencies."
    )

    st.divider()

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("🔐 Login"):

        role = authenticate_user(
            username,
            password
        )

        if role:

            st.session_state.logged_in = True
            st.session_state.role = role

            st.success("Login successful!")

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

elif st.session_state.role == "student":

    st.title("🎓 Student Emergency Dashboard")

    st.write(
        "Report any emergency or safety issue on campus."
    )

    st.divider()

    st.subheader("🚨 Report Emergency")

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

            ai_priority, recommended_action = analyze_emergency(
                emergency_type,
                description
            )

            created_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            add_emergency(
                student_name,
                emergency_type,
                location,
                location_details,
                description,
                ai_priority,
                "Pending",
                created_at
            )

            st.success(
                "🚨 Emergency alert submitted successfully!"
            )

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

    st.divider()

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()


# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif st.session_state.role == "admin":

    st.title("🛡️ Admin Safety Dashboard")

    st.write(
        "Central control panel for managing campus emergencies."
    )

    reports = get_emergencies()


    # =====================================================
    # CRITICAL ALERTS
    # =====================================================

    critical_alerts = [
        report
        for report in reports
        if report[6] == "CRITICAL"
        and report[7] == "Pending"
    ]

    if critical_alerts:

        st.error(
            f"🚨 {len(critical_alerts)} "
            f"CRITICAL EMERGENCY ALERT(S)!"
        )

        for alert in critical_alerts:

            st.warning(
                f"""
🚨 Report #{alert[0]}

Emergency Type: {alert[2]}

📍 Location: {alert[3]}

📌 Location Details: {alert[4]}

⚠️ Priority: {alert[6]}

👥 Assigned Team: {alert[9]}

⏳ Status: {alert[7]}
"""
            )

    else:

        st.success(
            "🟢 No critical pending emergencies."
        )


    st.divider()


    # =====================================================
    # STATISTICS
    # =====================================================

    total_reports = len(reports)

    critical_cases = sum(
        1 for report in reports
        if report[6] == "CRITICAL"
    )

    important_cases = sum(
        1 for report in reports
        if report[6] == "IMPORTANT"
    )

    normal_cases = sum(
        1 for report in reports
        if report[6] == "NORMAL"
    )

    pending_cases = sum(
        1 for report in reports
        if report[7] == "Pending"
    )

    responded_cases = sum(
        1 for report in reports
        if report[7] == "Responded"
    )

    resolved_cases = sum(
        1 for report in reports
        if report[7] == "Resolved"
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    st.subheader("📊 Emergency Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Reports",
        total_reports
    )

    col2.metric(
        "🔴 Critical",
        critical_cases
    )

    col3.metric(
        "🟠 Important",
        important_cases
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🟢 Normal",
        normal_cases
    )

    col2.metric(
        "⏳ Pending",
        pending_cases
    )

    col3.metric(
        "🟠 Responded",
        responded_cases
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "✅ Resolved",
        resolved_cases
    )

    col2.metric(
        "🚨 Critical Pending",
        len(critical_alerts)
    )


    st.divider()


    # =====================================================
    # PROFESSIONAL ANALYTICS
    # =====================================================

    st.subheader("📈 Emergency Analytics")

    if reports:

        # -------------------------------------------------
        # EMERGENCY TYPE DATA
        # -------------------------------------------------

        emergency_type_counts = {}

        for report in reports:

            emergency_type = report[2]

            if emergency_type not in emergency_type_counts:

                emergency_type_counts[emergency_type] = 0

            emergency_type_counts[emergency_type] += 1


        type_data = pd.DataFrame(
            list(emergency_type_counts.items()),
            columns=["Emergency Type", "Count"]
        )


        # -------------------------------------------------
        # PRIORITY DATA
        # -------------------------------------------------

        priority_counts = {}

        for report in reports:

            priority = report[6]

            if priority not in priority_counts:

                priority_counts[priority] = 0

            priority_counts[priority] += 1


        priority_data = pd.DataFrame(
            list(priority_counts.items()),
            columns=["Priority", "Count"]
        )


        # -------------------------------------------------
        # STATUS DATA
        # -------------------------------------------------

        status_counts = {}

        for report in reports:

            status = report[7]

            if status not in status_counts:

                status_counts[status] = 0

            status_counts[status] += 1


        status_data = pd.DataFrame(
            list(status_counts.items()),
            columns=["Status", "Count"]
        )


        # =================================================
        # EMERGENCY TYPE BAR CHART
        # =================================================

        st.write("### 🚨 Emergency Type Distribution")

        fig1 = px.bar(
            type_data,
            x="Count",
            y="Emergency Type",
            orientation="h",
            text="Count",
            title="Emergency Type Distribution"
        )

        fig1.update_traces(
            textposition="outside"
        )

        fig1.update_layout(
            height=400,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )


        # =================================================
        # PRIORITY DONUT CHART
        # =================================================

        st.write("### ⚠️ Priority Distribution")

        fig2 = px.pie(
            priority_data,
            names="Priority",
            values="Count",
            hole=0.55,
            title="Emergency Priority Distribution"
        )

        fig2.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig2.update_layout(
            height=400,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


        # =================================================
        # STATUS BAR CHART
        # =================================================

        st.write("### 🔄 Emergency Status Distribution")

        fig3 = px.bar(
            status_data,
            x="Status",
            y="Count",
            text="Count",
            title="Emergency Status Distribution"
        )

        fig3.update_traces(
            textposition="outside"
        )

        fig3.update_layout(
            height=400,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )


    else:

        st.info(
            "📊 Analytics will appear after emergency reports "
            "are submitted."
        )


    st.divider()


    # =====================================================
    # EMERGENCY REPORTS
    # =====================================================

    st.subheader("🚨 Emergency Reports")

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

            st.write(
                f"**Assigned Team:** {report[9]}"
            )


            # =================================================
            # TEAM ASSIGNMENT
            # =================================================

            st.write(
                "### 👥 Assign Response Team"
            )

            teams = [
                "Unassigned",
                "Medical Team",
                "Security Team",
                "Fire Response Team",
                "Maintenance Team"
            ]

            current_team = report[9]

            if current_team not in teams:

                current_team = "Unassigned"


            selected_team = st.selectbox(
                "Select Response Team",
                teams,
                index=teams.index(current_team),
                key=f"team_{report[0]}"
            )


            if st.button(
                "👥 Assign Team",
                key=f"assign_{report[0]}"
            ):

                assign_team(
                    report[0],
                    selected_team
                )

                st.success(
                    f"Report #{report[0]} assigned to "
                    f"{selected_team}."
                )

                st.rerun()


            # =================================================
            # STATUS UPDATE
            # =================================================

            st.write(
                "### 🔄 Update Emergency Status"
            )

            status_options = [
                "Pending",
                "Responded",
                "Resolved"
            ]

            current_status = report[7]

            if current_status not in status_options:

                current_status = "Pending"


            new_status = st.selectbox(
                "Select Status",
                status_options,
                index=status_options.index(current_status),
                key=f"status_{report[0]}"
            )


            if st.button(
                "🔄 Update Status",
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


    st.divider()


    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()
