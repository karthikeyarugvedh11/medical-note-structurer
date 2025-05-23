import streamlit as st
import pandas as pd
import requests
import json
st.title(" Medical Notes Structure")
uploaded_file = st.file_uploader("Upload clinical notes CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []
    with st.spinner("Extracting info..."):
        for _, row in df.iterrows():
            res = requests.post("http://localhost:8000/extract/",data={"note":row["doctor_notes"]})
            extracted = res.json().get("structured")
            try:
                structured = json.loads(extracted)
            except:
                structured = {"symptoms": "N/A", "diagnosis": "N/A", "medications": "N/A"}
            results.append({
                "patient_id": row["patient_id"],
                **structured
            })
    result_df = pd.DataFrame(results)
    st.success("Extraction complete!")
    st.dataframe(result_df)
    st.download_button("Download Results as CSV", result_df.to_csv(index=False),file_name="example_notes.csv", mime="text/csv")
