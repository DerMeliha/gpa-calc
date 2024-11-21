import pandas as pd
import streamlit as st

# Function to calculate grade points based on letter grade
def calculate_grade_points(letter):
    grades = {
        "AA": 4.0, "BA+": 3.75, "BA": 3.5, "BB+": 3.25, "BB": 3.0,
        "CB+": 2.75, "CB": 2.5, "CC+": 2.25, "CC": 2.0,
        "DC+": 1.75, "DC": 1.5, "DD+": 1.25, "DD": 1.0, "FF": 0.0
    }
    return grades.get(letter.strip(), 0.0)

# Function to calculate GPA
def calculate_gpa(data):
    lines = data.strip().split('\n')[1:]  # Skip header row
    sum_points = 0
    total_credits = 0
    invalid_lines = []
    course_data = []

    for line in lines:
        try:
            # Use fixed-width splitting by columns
            parts = line.split()
            if len(parts) < 3:
                raise ValueError("Invalid line format")
            
            course = " ".join(parts[:-2])  # Combine all but the last two columns as course name
            credit = int(parts[-2])  # Second-to-last column is the credit
            grade = parts[-1]  # Last column is the grade
            
            grade_points = calculate_grade_points(grade)
            
            sum_points += grade_points * credit
            total_credits += credit
            
            # Append valid data to course_data
            course_data.append({"Course Name": course, "Credit": credit, "Grade": grade})
        except Exception as e:
            invalid_lines.append(line)
    
    gpa = sum_points / total_credits if total_credits > 0 else 0.0
    return gpa, invalid_lines, total_credits, course_data

# Streamlit App
st.title("GPA Calculator")

# Input section
st.markdown("### Enter your course data:")
user_input = st.text_area(
    "Input format: Ders Adı      Kredi     Harf Notu",
    placeholder="E.g.,\nDers Adi      Kredi     Harf Notu\nMAT 103       4         BA \nFIZ 101E      3         CC \n...",
    height=300
)

if st.button("Calculate GPA"):
    if not user_input.strip():
        st.error("Please enter some data!")
    else:
        gpa, invalid_lines, total_credits, course_data = calculate_gpa(user_input)
        
        # Display results
        st.markdown(f"### 📊 Results:")
        st.markdown(f"**Total Credits:** {total_credits}")
        st.markdown(f"**GPA:** {gpa:.2f}")
        
        # Display input data as a table
        if course_data:
            df = pd.DataFrame(course_data)
            st.markdown("### 📋 Input Data:")
            st.table(df)
        
        # Display invalid lines if any
        if invalid_lines:
            st.error("Some lines could not be processed:")
            st.text("\n".join(invalid_lines))
