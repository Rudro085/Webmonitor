import streamlit as st
import pandas as pd
import time

# Simulated processed data
processed_data = pd.DataFrame(columns=["URL", "Status"])

# App title
st.markdown(
    "<h1 style='text-align: center; color: #4A4A4A;'>The Site Checker Bot</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# Section: Select Database
st.subheader("Select Database")
db_choice = st.radio("Choose a source:", ("Fixed", "Scrapped DB"), horizontal=True)

st.markdown("---")

# Status Message placeholder
status_placeholder = st.empty()

# Buttons: Start and Stop
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚀 Start Process", use_container_width=True):
        status_placeholder.info("Processing started... please wait.")
        # Simulate processing time
        time.sleep(2)
        # Add dummy data
        processed_data = pd.DataFrame({
            "URL": ["https://example.com", "https://site.com"],
            "Status": ["OK", "Failed"]
        })
        status_placeholder.success("Processing complete!")

with col2:
    if st.button("🛑 Stop Process", use_container_width=True):
        status_placeholder.warning("Process stopped.")

st.markdown("---")

# Download CSV button
if not processed_data.empty:
    csv = processed_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='processed_data.csv',
        mime='text/csv',
        use_container_width=True
    )

st.markdown("---")

# Textbox for adding data
st.subheader("Add New Row to Database")
new_row_data = st.text_input("Enter row data (comma-separated values, e.g., URL,Status)")

if st.button("➕ Add to DB", use_container_width=True):
    if new_row_data.strip():
        try:
            url, status = [x.strip() for x in new_row_data.split(",")]
            new_row_df = pd.DataFrame([[url, status]], columns=["URL", "Status"])
            processed_data = pd.concat([processed_data, new_row_df], ignore_index=True)
            st.success("Row added to the database.")
        except ValueError:
            st.error("Please enter data in the correct format: URL,Status")
    else:
        st.warning("Input field is empty.")

# Show updated table (optional)
if not processed_data.empty:
    st.markdown("### Current Processed Data")
    st.dataframe(processed_data, use_container_width=True)
