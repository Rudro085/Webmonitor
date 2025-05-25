import streamlit as st
import pandas as pd

st.set_page_config(page_title="Webmonitor", layout="wide")

# Title
st.title("Webmonitor")
st.subheader("A bot for checking govt websites")

# Initialize session state
if "db_type" not in st.session_state:
    st.session_state.db_type = "Static"
if "db" not in st.session_state:
    st.session_state.db = []
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

# Layout: Main (left) and Activity Log (right)
col_main, col_log = st.columns([3, 1])

with col_main:
    # Database selector
    db_type = st.radio(
        "Select database type:",
        ("Static", "Dynamic")
    )
    st.session_state.db_type = db_type

    # Start/Stop toggle
    if st.session_state.monitoring:
        if st.button("🛑 Stop Monitoring", key="stop_btn"):
            st.session_state.monitoring = False
            st.session_state.activity_log.append("Monitoring stopped.")
    else:
        if st.button("🚀 Start Monitoring", key="start_btn"):
            st.session_state.monitoring = True
            st.session_state.activity_log.append("Monitoring started.")

    st.markdown("---")

    if db_type == "Static":
        # Add element to DB
        new_element = st.text_input("Add element to database")
        if st.button("Add Element"):
            if new_element:
                st.session_state.db.append([new_element] + [""]*6)
                st.session_state.activity_log.append(f"Added element: {new_element}")
        # Upload CSV
        uploaded_file = st.file_uploader("Upload CSV and add to DB", type=["csv"])
        if st.button("Upload csv and add to DB"):
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                for row in df.values.tolist():
                    # Pad or trim to 7 columns
                    row = (row + [""]*7)[:7]
                    st.session_state.db.append(row)
                st.session_state.activity_log.append(f"Uploaded CSV with {len(df)} rows.")
    else:
        # Change root website
        root_website = st.text_input("Change root website", value="bangladesh.gov.bd")
        if st.button("Populate DB"):
            # Placeholder: Add root website to DB
            st.session_state.db.append([root_website] + [""]*6)
            st.session_state.activity_log.append(f"Populated DB with root: {root_website}")

    # Clear DB
    if st.button("Clear DB"):
        st.session_state.db = []
        st.session_state.activity_log.append("Database cleared.")

    st.markdown("---")

    # Table display
    st.markdown("### Database Table")
    columns = ["Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7"]
    df_display = pd.DataFrame(st.session_state.db, columns=columns)
    st.dataframe(df_display, use_container_width=True)

with col_log:
    st.markdown("### Activity Log")
    for log in reversed(st.session_state.activity_log[-20:]):
        st.write(log)