import streamlit as st

st.set_page_config(
    page_title="Smart Campus Guardian",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Smart Campus Guardian")

st.subheader(
    "AI-Based College Emergency & Safety Management System"
)

st.write(
    "A digital platform for managing campus emergencies "
    "quickly and efficiently."
)

st.divider()

st.header("🛡️ Campus Safety Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🆘 Emergency SOS")
    st.write(
        "Quickly report an emergency."
    )

with col2:
    st.subheader("📍 Location")
    st.write(
        "Provide the campus location."
    )

with col3:
    st.subheader("🤖 Smart Priority")
    st.write(
        "Identify emergency priority."
    )

st.divider()

st.info(
    "Student safety and quick emergency response."
)
