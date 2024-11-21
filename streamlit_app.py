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
    credits_without_ff = 0
    invalid_lines = []
    course_data = []

    seen_courses = set()  # To track duplicate courses

    for line in lines:
        try:
            parts = line.split()
            if len(parts) < 3:  # Make sure there are at least 3 parts
                invalid_lines.append(line)
                continue  # Skip this line if it's invalid

            course = " ".join(parts[:-2])  # Combine all but the last two columns as course name
            credit = int(parts[-2])  # Second-to-last column is the credit
            grade = parts[-1]  # Last column is the grade
            
            if course in seen_courses:
                continue  # Skip duplicate courses
            seen_courses.add(course)
            
            grade_points = calculate_grade_points(grade)
            
            sum_points += grade_points * credit
            total_credits += credit  # Always count total credits
            if grade != "FF":
                credits_without_ff += credit  # Exclude FF credits for this count
            
            # Append valid data to course_data
            course_data.append({"Course Name": course, "Credit": credit, "Grade": grade})
        except Exception as e:
            invalid_lines.append(line)
    
    gpa = sum_points / total_credits if total_credits > 0 else 0.0
    return gpa, invalid_lines, total_credits, credits_without_ff, course_data

# Streamlit App
st.title("GPA Calculator")

# Input section
st.markdown("<h3>Enter your course data:</h3>", unsafe_allow_html=True)
user_input = st.text_area(
    "",
    placeholder="E.g.,\nDers Adi      Kredi     Harf Notu\nMAT 103       4         BA \nFIZ 101E      3         CC \n...",
    height=300
)

if st.button("Calculate GPA"):
    if not user_input.strip():
        st.error("Please enter some data!")
    else:
        gpa, invalid_lines, total_credits, credits_without_ff, course_data = calculate_gpa(user_input)
        
        # Display results
        st.markdown(f"<h2 style='font-size: 28px;'>📊 Results:</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px;'><strong>Total Credits Given:</strong> {total_credits}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px;'><strong>Total Credits Without FF:</strong> {credits_without_ff}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px;'><strong>GPA:</strong> {gpa:.2f}</p>", unsafe_allow_html=True)
        
        # Prepare DataFrame
        if course_data:
            df = pd.DataFrame(course_data)
            df.index += 1  # Start index from 1
            
            # Highlighting rows directly within the DataFrame
            def row_styles(row):
                if row["Grade"] == "FF":
                    return ["background-color: rgba(255, 0, 0, 0.25); color: white"] * len(row)
                elif calculate_grade_points(row["Grade"]) > 3.0:
                    return ["background-color: rgba(0, 255, 0, 0.25); color: white"] * len(row)
                else:
                    return ["background-color: transparent; color: white"] * len(row)
            
            styled_df = df.style.apply(row_styles, axis=1).set_table_styles([{
                'selector': 'table', 'props': [('width', '100%'), ('font-size', '16px')]}, {
                'selector': 'th', 'props': [('text-align', 'center'), ('font-size', '18px')]}, {
                'selector': 'td', 'props': [('text-align', 'center')]},])
            
            st.markdown("### 📋 Input Data (No Duplicates):")
            st.write(styled_df.to_html(), unsafe_allow_html=True)  # Use HTML rendering for custom styles
        
        # Display invalid lines if any
        if invalid_lines:
            st.error("Some lines could not be processed:")
            st.text("\n".join(invalid_lines))
