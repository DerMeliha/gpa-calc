import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Function to calculate grade points based on letter grade
def calculate_grade_points(letter):
    grade_mapping = {
        "AA": 4.0, "BA+": 3.75, "BA": 3.5, "BB+": 3.25, "BB": 3.0,
        "CB+": 2.75, "CB": 2.5, "CC+": 2.25, "CC": 2.0, "DC+": 1.75,
        "DC": 1.5, "DD+": 1.25, "DD": 1.0, "FF": 0.0
    }
    return grade_mapping.get(letter, 0.0)

# Function to fetch course details from the website
def fetch_course_data(course_code):
    url = "https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-planlari/plan/JEF/202210.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the table rows
    table = soup.find("table", {"class": "table"})  # Assuming table has a class "table"
    rows = table.find_all("tr")[1:]  # Skip header row
    
    course_data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0 and cols[0].text.strip() == course_code:
            course_data.append({
                "Ders Kodu": cols[0].text.strip(),
                "Kredi": cols[2].text.strip(),
                "Yarıyıl": cols[3].text.strip()
            })
    return course_data

# Streamlit App Layout
st.title("GPA Calculator with Course Info")

# Input field for grade data
st.markdown("### Enter Grades (Format: 'Course Code, Credits, Grade'):")
user_input = st.text_area(
    "",
    placeholder="E.g.,\nMAT 103, 4, BA\nFIZ 101E, 3, CC\nING 100, 3, AA",
    height=200
)

if st.button("Calculate GPA"):
    if user_input.strip():
        # Parse input
        lines = user_input.strip().split("\n")
        data = []
        unique_rows = set()
        total_credits = 0
        total_credits_with_ff = 0
        weighted_sum = 0

        for line in lines:
            parts = line.split(",")
            if len(parts) != 3:
                st.error(f"Invalid input format: {line}")
                continue
            
            course_code, credit, grade = map(str.strip, parts)
            if line in unique_rows:
                continue  # Skip duplicates
            unique_rows.add(line)
            
            grade_points = calculate_grade_points(grade)
            credit_value = int(credit)
            
            total_credits_with_ff += credit_value
            if grade != "FF":
                total_credits += credit_value
            
            weighted_sum += grade_points * credit_value
            data.append({"Course Code": course_code, "Credits": credit_value, "Grade": grade})
        
        # Calculate GPA
        gpa = weighted_sum / total_credits_with_ff if total_credits_with_ff > 0 else 0.0
        gpa = round(gpa, 2)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        df["Background Color"] = df["Grade"].apply(
            lambda x: "rgba(255,0,0,0.25)" if x == "FF" else ("rgba(0,255,0,0.25)" if calculate_grade_points(x) >= 3.0 else "transparent")
        )
        
        # Style DataFrame
        styled_df = df.style.apply(
            lambda x: [f"background-color: {color}" for color in x["Background Color"]],
            axis=1
        ).hide(axis="index").set_table_styles(
            [{"selector": "thead th", "props": [("background-color", "black"), ("color", "white"), ("font-size", "18px")]}]
        )

        # Display GPA and tables
        st.markdown(f"### GPA: {gpa}")
        st.dataframe(styled_df, use_container_width=True)
        
        st.markdown(f"### Total Credits (Excluding FF): {total_credits}")
        st.markdown(f"### Total Credits (Including FF): {total_credits_with_ff}")

        # Fetch course info for a specific course
        course_code_to_fetch = "BIL 112E"  # Change this code to test for a different course
        course_info = fetch_course_data(course_code_to_fetch)
        if course_info:
            st.markdown("### Course Info:")
            st.table(pd.DataFrame(course_info))
        else:
            st.error(f"Course info for {course_code_to_fetch} not found.")
    else:
        st.error("Please enter some data before pressing Calculate GPA.")
