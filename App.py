import streamlit as st

st.set_page_config(
    page_title="Smart Campus Guardian",
    page_icon="🚨",
    layout="wide"
)

# -----------------------------
# Login Function
# -----------------------------
def login_page():

    st.title("🚨 Smart Campus Guardian")

    st.subheader(
        "AI-Based College Emergency & Safety Management System"
    )

    st.divider()

    st.header("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:

        if username == "student" and password == "1234":

            st.session_state.logged_in = True
            st.session_state.role = "student"

            st.success("Student login successful!")
            st.rerun()

        elif username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.session_state.role = "admin"

            st.success("Admin login successful!")
            st.rerun()

        else:
            st.error("Invalid username or password.")


# -----------------------------
# Student Dashboard
# -----------------------------
def student_dashboard():

    st.title("🎓 Student Dashboard")

    st.success("Welcome, Student!")

    st.divider()

    st.header("🆘 Emergency Report")

    st.write(
        "Use this section to report a campus emergency."
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
        "Describe the emergency"
    )

    if st.button("🚨 SEND EMERGENCY ALERT"):

        if description.strip() == "":
            st.warning(
                "Please describe the emergency."
            )
        else:
            st.success(
                "Emergency report submitted successfully!"
            )

    st.divider()

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()


# -----------------------------
# Admin Dashboard
# -----------------------------
def admin_dashboard():

    st.title("🛡️ Admin Dashboard")

    st.success("Welcome, Administrator!")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Total Reports", 0)

    with col2:
        st.metric("🚨 Critical Cases", 0)

    with col3:
        st.metric("⏳ Pending Cases", 0)

    with col4:
        st.metric("✅ Resolved Cases", 0)

    st.divider()

    st.info(
        "Emergency reports will appear here."
    )

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()


# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


# -----------------------------
# Main Application
# -----------------------------
if not st.session_state.logged_in:

    login_page()

elif st.session_state.role == "student":

    student_dashboard()

elif st.session_state.role == "admin":

    admin_dashboard()
