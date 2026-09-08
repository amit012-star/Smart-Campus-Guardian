import streamlit as st
from datetime import datetime

from database import (
    create_database,
    add_emergency,
    get_emergencies,
    update_status,
    assign_team,
    authenticate_user
)

from ai_engine import analyze_emergency


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


# =========================================================
# LOGIN PAGE
# =========================================================

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

        role = authenticate_user(
            username,
            password
        )

        if role:

            st.session_state.logged_in = True
            st.session_state.role = role

            st.success(
                "Login successful!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

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
                "Emergency alert submitted successfully!"
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

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()


# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif st.session_state.role == "admin":

    st.title("🛡️ Admin Safety Dashboard")

    reports = get_emergencies()

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


    # =====================================================
    # OVERVIEW
    # =====================================================

    st.subheader(
        "📊 Emergency Overview"
    )

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


    # =====================================================
    # ANALYTICS
    # =====================================================

    st.subheader(
        "📈 Emergency Analytics"
    )

    if reports:

        emergency_type_counts = {}

        for report in reports:

            emergency_type = report[2]

            if emergency_type not in emergency_type_counts:

                emergency_type_counts[emergency_type] = 0

            emergency_type_counts[emergency_type] += 1


        st.write(
            "### 🚨 Emergency Type Distribution"
        )

        st.bar_chart(
            emergency_type_counts
        )


        priority_counts = {}

        for report in reports:

            priority = report[6]

            if priority not in priority_counts:

                priority_counts[priority] = 0

            priority_counts[priority] += 1


        st.write(
            "### ⚠️ Priority Distribution"
        )

        st.bar_chart(
            priority_counts
        )

    else:

        st.info(
            "Charts will appear after emergency reports are submitted."
        )


    st.divider()


    # =====================================================
    # EMERGENCY REPORTS
    # =====================================================

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
                    f"Report #{report[0]} assigned to {selected_team}."
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


    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.rerun()
