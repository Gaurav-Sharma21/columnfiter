import streamlit as st
import pandas as pd
from io import BytesIO
from zipfile import ZipFile



st.title("CSV Column Extractor")

upload_option = st.radio("Choose your upload option?", ("Upload a file", "Upload multiple files"))


files = None
if upload_option == "Upload a file":
    uploaded_file = st.file_uploader("Upload a CSV, txt or tsv file", type=["csv","CSV","txt","tsv"])
    if uploaded_file is not None:
        files = [uploaded_file]
else:
    uploaded_files = st.file_uploader("Upload multiple CSV, txt or tsv files", type=["csv","CSV","txt","tsv"], accept_multiple_files=True)
    files = uploaded_files if uploaded_files else []


#Function to detect dilimiter 
def detect_delimiter(file_extension):
    if file_extension == "csv":
        return st.selectbox("Choose delimiter for CSV file", [',', '\t', ';', '|'], index=0, key=f"{file.name}")
    elif file_extension == "CSV":
        return st.selectbox("Choose delimiter for CSV file", [',', '\t', ';', '|'], index=0, key=f"{file.name}")
    elif file_extension == "tsv":
        return "\t"
    elif file_extension == "txt":
        return st.selectbox("Choose delimiter for TXT file", [',', '\t', ';', '|'], index=0, key=f"{file.name}")



#Checking if the files are uploaded
if files:

    for file in files:
        file_extension = file.name.split(".")[-1].lower()
        delimiter = detect_delimiter(file_extension)

        skip_rows = st.number_input("Enter the number of rows to skip", min_value=0, max_value=30, step=1)
        st.subheader(f"Processing File: {file.name}")
        df = pd.read_csv(file, delimiter=delimiter, skiprows= skip_rows, on_bad_lines="skip")
        st.write("Preview of the file:")
        st.dataframe(df.head())

        column_name = st.selectbox(f"Select the column to extract from {file.name}", df.columns, key=f"column_select_{file.name}")

        # New column name 
        new_column_name = st.text_input("Enter the new column name",column_name, key=f"{file.name}_new_column") 
        new_file_name = st.text_input("Enter the new file name (without .csv)", f"extracted_{file.name.replace('.csv', '')}", key=f"{file.name}_new_file_name")

        if st.button(f"Extract {column_name} from {file.name} and save as {new_file_name}.csv", key=f"{file.name}_extract_button"):
            if isinstance(df[[column_name]], pd.DataFrame):
                extracted_df = df[[column_name]].rename(columns={column_name: new_column_name})
            else:
                extracted_df = df[column_name].rename(new_column_name)


            csv_data = extracted_df.to_csv(index=False).encode('utf-8')

            st.download_button(label=f"Download {new_file_name}.csv", data=csv_data, file_name=f"{new_file_name}.csv", mime="text/csv")

else:
    st.info("Please upload a file or files to start")


