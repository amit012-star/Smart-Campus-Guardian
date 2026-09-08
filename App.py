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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL DESIGN
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}


/* Main Background */

.stApp {
    background: #f5f7fb;
}


/* Top Header */

.top-header {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 15px 25px;
    border-radius: 0 0 16px 16px;
    margin-bottom: 25px;
}

.brand {
    font-size: 24px;
    font-weight: 800;
    color: #123b70;
}

.brand-small {
    font-size: 13px;
    color: #64748b;
}


/* Hero */

.hero-box {
    background: linear-gradient(
        135deg,
        #0b1f3a 0%,
        #123b70 55%,
        #1769aa 100%
    );

    padding: 55px 35px;
    border-radius: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 12px 35px rgba(15, 43, 76, 0.18);
    margin-bottom: 28px;
}

.hero-shield {
    font-size: 58px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 18px;
    margin-top: 10px;
    opacity: 0.9;
}

.hero-tag {
    display: inline-block;
    margin-top: 20px;
    padding: 8px 18px;
    border-radius: 30px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    font-size: 14px;
}


/* Section Heading */

.section-heading {
    text-align: center;
    font-size: 27px;
    font-weight: 800;
    color: #172033;
    margin: 30px 0 8px 0;
}

.section-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 15px;
    margin-bottom: 25px;
}


/* Feature Cards */

.feature-card {
    background: white;
    border: 1px solid #e6eaf0;
    border-radius: 18px;
    padding: 25px 18px;
    min-height: 185px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
}

.feature-icon {
    font-size: 38px;
    margin-bottom: 10px;
}

.feature-title {
    font-size: 17px;
    font-weight: 750;
    color: #172033;
}

.feature-description {
    color: #64748b;
    font-size: 13px;
    line-height: 1.5;
    margin-top: 8px;
}


/* Login Area */

.login-wrapper {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
}


/* Login Heading */

.login-title {
    text-align: center;
    font-size: 25px;
    font-weight: 800;
    color: #172033;
}

.login-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 14px;
    margin-bottom: 20px;
}


/* Trust Bar */

.trust-bar {
    background: #eef6ff;
    border: 1px solid #d7e9ff;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    color: #31577d;
    margin-top: 25px;
}


/* Footer */

.footer-box {
    text-align: center;
    margin-top: 35px;
    padding: 22px;
    color: #64748b;
    font-size: 13px;
    border-top: 1px solid #e5e7eb;
}


/* Buttons */

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}


/* Dashboard Cards */

.dashboard-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
}


/* Mobile */

@media (max-width: 768px) {

    .hero-title {
        font-size: 30px;
    }

    .hero-subtitle {
        font-size: 15px;
    }

    .hero-box {
        padding: 40px 20px;
    }

}

</style>
""", unsafe_allow_html=True)


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
# PROFESSIONAL FRONT SCREEN
# =========================================================

if not st.session_state.logged_in:

    # -----------------------------------------------------
    # INSTITUTE HEADER
    # -----------------------------------------------------

    st.markdown("""
    <div class="top-header">

        <div class="brand">
            🛡️ Smart Campus Guardian
        </div>

        <div class="brand-small">
            Digital Campus Safety & Emergency Management Platform
        </div>

    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    st.markdown("""
    <div class="hero-box">

        <div class="hero-shield">
            🛡️
        </div>

        <div class="hero-title">
            Smart Campus Guardian
        </div>

        <div class="hero-subtitle">
            AI-Based College Emergency & Safety Management System
        </div>

        <div class="hero-tag">
            🚨 Report &nbsp; • &nbsp;
            🤖 Analyze &nbsp; • &nbsp;
            👥 Respond &nbsp; • &nbsp;
            📊 Monitor
        </div>

    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # INTRODUCTION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">A Safer & Smarter Campus</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'One centralized platform for reporting, analyzing and managing campus emergencies.'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # FEATURES
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                🚨
            </div>

            <div class="feature-title">
                Emergency Reporting
            </div>

            <div class="feature-description">
                Students can quickly report medical,
                fire, accident and security emergencies.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                🤖
            </div>

            <div class="feature-title">
                AI-Based Analysis
            </div>

            <div class="feature-description">
                Analyze emergency information and
                determine priority with recommended action.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with col3:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                👥
            </div>

            <div class="feature-title">
                Response Management
            </div>

            <div class="feature-description">
                Assign medical, security, fire and
                maintenance teams to emergencies.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with col4:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                📊
            </div>

            <div class="feature-title">
                Smart Analytics
            </div>

            <div class="feature-description">
                Monitor emergency reports, priorities
                and response status through analytics.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # LOGIN SECTION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">Secure Access</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Authorized students and administrators can access the system.'
        '</div>',
        unsafe_allow_html=True
    )


    login_left, login_center, login_right = st.columns(
        [1, 2, 1]
    )

    with login_center:

        st.markdown("""
        <div class="login-wrapper">

            <div class="login-title">
                🔐 Welcome Back
            </div>

            <div class="login-subtitle">
                Sign in to Smart Campus Guardian
            </div>

        </div>
        """, unsafe_allow_html=True)


        username = st.text_input(
            "👤 Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter password"
        )


        if st.button(
            "🚀 Sign In",
            use_container_width=True
        ):

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
                    "❌ Invalid username or password."
                )


    # -----------------------------------------------------
    # SECURITY MESSAGE
    # -----------------------------------------------------

    st.markdown("""
    <div class="trust-bar">

        🔒 <b>Secure Campus Platform</b><br>

        Emergency information is accessible only
        to authorized system users.

    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.markdown("""
    <div class="footer-box">

        🛡️ <b>Smart Campus Guardian</b><br>

        AI-Based College Emergency & Safety Management System<br><br>

        Designed for a safer, smarter and more responsive campus.

    </div>
    """, unsafe_allow_html=True)


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


    if st.button(
        "🚨 Send Emergency Alert",
        use_container_width=True
    ):

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
                "⚠️ Please fill all fields."
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
    # CRITICAL ALERT
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
    # KPI
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
    # ANALYTICS
    # =====================================================

    st.subheader("📈 Emergency Analytics")

    if reports:

        emergency_type_counts = {}

        for report in reports:

            emergency_type = report[2]

            if emergency_type not in emergency_type_counts:

                emergency_type_counts[emergency_type] = 0

            emergency_type_counts[emergency_type] += 1


        type_data = pd.DataFrame(
            list(emergency_type_counts.items()),
            columns=[
                "Emergency Type",
                "Count"
            ]
        )


        priority_counts = {}

        for report in reports:

            priority = report[6]

            if priority not in priority_counts:

                priority_counts[priority] = 0

            priority_counts[priority] += 1


        priority_data = pd.DataFrame(
            list(priority_counts.items()),
            columns=[
                "Priority",
                "Count"
            ]
        )


        status_counts = {}

        for report in reports:

            status = report[7]

            if status not in status_counts:

                status_counts[status] = 0

            status_counts[status] += 1


        status_data = pd.DataFrame(
            list(status_counts.items()),
            columns=[
                "Status",
                "Count"
            ]
        )


        # -------------------------------------------------
        # CHART 1
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CHART 2
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CHART 3
        # -------------------------------------------------

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


            # -------------------------------------------------
            # TEAM ASSIGNMENT
            # -------------------------------------------------

            st.write("### 👥 Assign Response Team")

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


            # -------------------------------------------------
            # STATUS UPDATE
            # -------------------------------------------------

            st.write("### 🔄 Update Emergency Status")

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
