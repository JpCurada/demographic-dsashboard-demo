import streamlit as st
import plotly.express as px
import pandas as pd
import re

# Streamlit page configuration
st.set_page_config(page_title="Student Demographics", layout="wide")

# Minimalist title
st.title("Student Insights")

# Google Sheet ID
SHEET_ID = "1JSEnjf6ovLPH-2DqFNdT3aKbLD-3BWBuRhwGycDrhWw"

try:
    # Load data
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)
    
    if not df.empty:
        # Process College column to extract text in parentheses
        if 'College' in df.columns:
            df['College'] = df['College'].apply(lambda x: re.search(r'\((.*?)\)', str(x)).group(1) if re.search(r'\((.*?)\)', str(x)) else x)

        # Row 1: Metrics
        st.subheader("Key Figures")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", f"{df.shape[0]:,}")
        with col2:
            if 'Monthly Allowance' in df.columns:
                st.metric("Avg. Monthly Allowance", f"₱{df['Monthly Allowance'].mean():,.0f}")
        with col3:
            if 'Year Level' in df.columns:
                st.metric("Unique Year Levels", f"{df['Year Level'].nunique()}")

        # Row 2: Residence and Allowance
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Residence' in df.columns:
                residence_df = df['Residence'].value_counts().reset_index()
                residence_df.columns = ['Residence', 'Count']
                residence_df = residence_df.sort_values('Count', ascending=True)  # Sort for row chart
                fig_res = px.bar(residence_df, y='Residence', x='Count', orientation='h',
                                title="Where Do Our Students Live?",
                                text_auto=True)
                fig_res.update_layout(
                    template="simple_white",
                    showlegend=False,
                    title_x=0.5,
                    margin=dict(t=50, b=0)
                )
                st.plotly_chart(fig_res, use_container_width=True)
        
        with col2:
            if 'Monthly Allowance' in df.columns:
                fig_allow = px.histogram(df, x='Monthly Allowance',
                                        title="How Much Allowance Do They Receive?",
                                        nbins=20)
                fig_allow.update_layout(
                    template="simple_white",
                    showlegend=False,
                    title_x=0.5,
                    margin=dict(t=50, b=0)
                )
                fig_allow.update_traces(marker=dict(line=dict(width=0)))
                st.plotly_chart(fig_allow, use_container_width=True)

        # Row 3: Course, College, Year Level
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Course' in df.columns:
                course_df = df['Course'].value_counts().head(10).reset_index()
                course_df.columns = ['Course', 'Count']
                course_df = course_df.sort_values('Count', ascending=True)  # Sort for row chart
                fig_course = px.bar(course_df, y='Course', x='Count', orientation='h',
                                    title="What Are the Top 10 Courses?",
                                    text_auto=True)
                fig_course.update_layout(
                    template="simple_white",
                    showlegend=False,
                    title_x=0.5,
                    margin=dict(t=50, b=0)
                )
                st.plotly_chart(fig_course, use_container_width=True)
        
        with col2:
            if 'College' in df.columns:
                college_df = df['College'].value_counts().head(5).reset_index()
                college_df.columns = ['College', 'Count']
                college_df = college_df.sort_values('Count', ascending=True)  # Sort for row chart
                fig_college = px.bar(college_df, y='College', x='Count', orientation='h',
                                    title="Which Colleges Lead?",
                                    text_auto=True)
                fig_college.update_layout(
                    template="simple_white",
                    showlegend=False,
                    title_x=0.5,
                    margin=dict(t=50, b=0)
                )
                st.plotly_chart(fig_college, use_container_width=True)
        
        with col3:
            if 'Year Level' in df.columns:
                year_df = df['Year Level'].value_counts().reset_index()
                year_df.columns = ['Year Level', 'Count']
                fig_year = px.pie(year_df, names='Year Level', values='Count',
                                title="Which Year Dominates?",
                                hole=0.4,  # Donut chart
                                color_discrete_sequence=px.colors.sequential.Blues_r)  # Shades of blue
                fig_year.update_layout(
                    template="simple_white",
                    showlegend=False,  # No legend
                    title_x=0.5,
                    margin=dict(t=50, b=0)
                )
                fig_year.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#FFFFFF', width=1))  # White borders for clarity
                )
                st.plotly_chart(fig_year, use_container_width=True)
        
    else:
        st.warning("No data found in the spreadsheet")
        
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.write("Check if the Google Sheet ID is correct and publicly accessible")

