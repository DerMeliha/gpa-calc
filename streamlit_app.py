import streamlit as st
import pandas as pd

# Define the grade points based on the letter grade
def calculateGradePoints(letter):
    switcher = {
        "AA": 4.0,
        "BA+": 3.75,
        "BA": 3.5,
        "BB+": 3.25,
        "BB": 3.0,
        "CB+": 2.75,
        "CB": 2.5,
        "CC+": 2.25,
        "CC": 2.0,
        "DC+": 1.75,
        "DC": 1.5,
        "DD+": 1.25,
        "DD": 1.0,
        "FF": 0.0,
    }
    return switcher.get(letter.strip(), 0.0)

# Main function to calculate GPA and total credits
def calculateGPA(data):
    total_credits = 0
    total_grade_points = 0
    total_credits_given = 0
    total_credits_with_FF = 0

    for course in data:
        course_name = course[0].strip()
        credits = int(course[1].strip())
        grade = course[2].strip()

        # If FF grade, don't add the credits to total credits
        if grade == "FF":
            total_credits_with_FF += credits
            grade_points = 0  # FF is 0 points, but still counted as a failed course.
        else:
            total_credits_given += credits
            grade_points = calculateGradePoints(grade)

        total_grade_points += grade_points * credits
        total_credits += credits

    gpa = total_grade_points / total_credits_given if total_credits_given != 0 else 0
    return total_credits, total_credits_given, total_credits_with_FF, gpa

# Streamlit App Layout
st.title("GPA Calculator")

# Instructions
st.markdown("**Enter your course details:**")
st.markdown("Format: `Course Name, Credits, Grade (e.g., AA)`")

# Input for courses as a text area
courses_input = st.text_area(
    "Enter your courses here",
    placeholder="E.g., MAT 103, 4, BA\nFIZ 101, 3, CC\nJEF 111, 2, AA", 
    height=200
)

# Parse input data and calculate GPA when "Calculate GPA" button is clicked
if st.button("Calculate GPA"):
    if courses_input.strip():  # Check if input is not empty
        # Parse the input into a list of tuples (Course Name, Credits, Grade)
        courses = [line.split(',') for line in courses_input.strip().split('\n') if line]
        
        total_credits, total_credits_given, total_credits_with_FF, gpa = calculateGPA(courses)

        # Display results
        st.markdown(f"**Total Credits:** {total_credits}")
        st.markdown(f"**Credits Given (not FF):** {total_credits_given}")
        st.markdown(f"**Credits with FF (not counted):** {total_credits_with_FF}")
        st.markdown(f"**GPA:** {gpa:.2f}")

    else:
        st.error("Please enter some course data.")
