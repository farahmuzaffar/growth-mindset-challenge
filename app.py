import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup your app
st.set_page_config(page_title="Growth Mindset Challenge", page_icon=":smiley:", layout="wide")
st.title("🧠Growth Mindset Challenge: ")
st.write("✨Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
        # Show five rows of our df
        st.write("Preview the Head of the DataFrame:")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {uploaded_file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates for {uploaded_file.name}"):
                    df = df.drop_duplicates()
                    st.write("Duplicates Removed!")
            with col2:
                if st.button(f"Fill Missing Values for {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled!")

        # Choose specific columns to keep or convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create some visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {uploaded_file.name}"):
            # Check if there are numeric columns in the DataFrame
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.write("Visualizing the numeric columns:")
                st.bar_chart(df[numeric_cols].iloc[:, :2])  
            else:
                st.warning("No numeric columns available for visualization.")

        # Convert the file -> CSV to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {uploaded_file.name} to:", ("CSV", "Excel"), key=uploaded_file.name)
        if st.button(f"Convert {uploaded_file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = uploaded_file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = uploaded_file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"🔽Download {uploaded_file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type  # Fixed: Changed `mime_type` to `mime`
            )

st.success("All files processed!🎉")

              

                    
                   




