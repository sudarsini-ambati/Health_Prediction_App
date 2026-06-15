import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    hemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()

st.title("Health Prediction Application")
st.subheader("Patient Details Form")

name = st.text_input("Full Name")
dob = st.date_input("Date of Birth")
email = st.text_input("Email Address")

glucose = st.number_input("Glucose Level")
hemoglobin = st.number_input("Hemoglobin Level")
cholesterol = st.number_input("Cholesterol Level")

remarks = st.text_area("Remarks")

if glucose > 0.12:
    prediction = "High Glucose Level Detected"
else:
    prediction = "Glucose Level Normal"


if st.button("Save Record"):

    final_remarks = remarks if remarks else prediction

    c.execute("""
    INSERT INTO patients
    (name,dob,email,glucose,hemoglobin,cholesterol,remarks)
    VALUES (?,?,?,?,?,?,?)
    """,
    (
        name,
        str(dob),
        email,
        glucose,
        hemoglobin,
        cholesterol,
        final_remarks
    ))

    conn.commit()

    st.success("Patient Record Saved Successfully")


if st.button("View Records"):

    c.execute("SELECT * FROM patients")
    data = c.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "DOB",
            "Email",
            "Glucose",
            "Hemoglobin",
            "Cholesterol",
            "Remarks"
        ]
    )

    st.dataframe(df)

    st.subheader("Health Prediction")

    if glucose > 0.12:
        st.error("High Glucose Level Detected")
    else:
        st.success("Glucose Level Normal")


st.subheader("Delete Record")

delete_id = st.number_input(
    "Enter ID to Delete",
    min_value=1,
    step=1
)

if st.button("Delete Record"):

    c.execute(
        "DELETE FROM patients WHERE id=?",
        (delete_id,)
    )

    conn.commit()

    st.success("Record Deleted Successfully")


st.subheader("Update Remarks")

update_id = st.number_input(
    "Enter ID to Update",
    min_value=1,
    step=1,
    key="update_id"
)

new_remarks = st.text_area(
    "Enter New Remarks",
    key="new_remarks"
)

if st.button("Update Remarks"):

    c.execute(
        "UPDATE patients SET remarks=? WHERE id=?",
        (new_remarks, update_id)
    )

    conn.commit()

    st.success("Remarks Updated Successfully")


st.subheader("Search Patient")

search_name = st.text_input(
    "Enter Patient Name",
    key="search_name"
)

if st.button("Search"):

    c.execute(
        "SELECT * FROM patients WHERE name=?",
        (search_name,)
    )

    result = c.fetchall()

    if result:

        search_df = pd.DataFrame(
            result,
            columns=[
                "ID",
                "Name",
                "DOB",
                "Email",
                "Glucose",
                "Hemoglobin",
                "Cholesterol",
                "Remarks"
            ]
        )

        st.dataframe(search_df)

    else:
        st.warning("No Patient Found")


st.subheader("Download Records")

c.execute("SELECT * FROM patients")
all_data = c.fetchall()

download_df = pd.DataFrame(
    all_data,
    columns=[
        "ID",
        "Name",
        "DOB",
        "Email",
        "Glucose",
        "Hemoglobin",
        "Cholesterol",
        "Remarks"
    ]
)

csv = download_df.to_csv(index=False)

st.download_button(
    label="Download Records CSV",
    data=csv,
    file_name="patients.csv",
    mime="text/csv"
)