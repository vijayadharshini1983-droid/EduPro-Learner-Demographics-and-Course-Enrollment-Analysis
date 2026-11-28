
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="EduPro Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduPro – Learner Demographics and Course Enrollment Analysis")
st.markdown(
    "### Exploring learner demographics and course enrollment behavior"
)

st.sidebar.title("EduPro Dashboard")
st.sidebar.write("Learner Analytics Platform")

# ---------------------------------
# LOAD DATASET
# ---------------------------------

st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload your EduPro Excel or CSV file",
    type=["xlsx", "csv"]
)

file_path = "EduPro Online Platform.xlsx"

try:
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    elif os.path.exists(file_path):
        df = pd.read_excel(file_path)

    else:
        st.warning("Please upload your EduPro dataset to continue.")
        st.stop()

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------------------------
# DATA CLEANING
# ---------------------------------

df.columns = df.columns.astype(str).str.strip()

df = df.drop_duplicates()

st.sidebar.success("Dataset loaded successfully!")

# ---------------------------------
# AUTOMATIC COLUMN DETECTION
# ---------------------------------

def find_column(possible_names):
    for col in df.columns:
        normalized = col.lower().replace("_", " ").strip()
        if normalized in possible_names:
            return col
    return None

age_col = find_column(["age", "learner age", "student age"])
gender_col = find_column(["gender", "sex"])
category_col = find_column([
    "course category", "category", "course type"
])
level_col = find_column([
    "course level", "level", "difficulty level"
])
course_col = find_column([
    "course name", "course", "course title"
])
date_col = find_column([
    "enrollment date", "enrolment date",
    "registration date", "date"
])

# ---------------------------------
# OVERVIEW
# ---------------------------------

st.header("📊 Project Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Learner Records", len(df))

if course_col:
    col2.metric("Total Courses", df[course_col].nunique())
else:
    col2.metric("Total Columns", len(df.columns))

if gender_col:
    col3.metric("Gender Categories", df[gender_col].nunique())
else:
    col3.metric("Dataset Columns", len(df.columns))

st.divider()

# ---------------------------------
# LEARNER DEMOGRAPHICS
# ---------------------------------

st.header("👥 Learner Demographics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Gender Distribution")

    if gender_col:
        gender_data = df[gender_col].value_counts()

        fig, ax = plt.subplots()
        gender_data.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Gender column not found.")

with col2:
    st.subheader("Age Group Distribution")

    if age_col:
        df[age_col] = pd.to_numeric(
            df[age_col], errors="coerce"
        )

        age_data = df[age_col].dropna()

        if not age_data.empty:
            bins = [0, 18, 25, 35, 45, 60, 100]
            labels = [
                "Below 18", "18-25", "26-35",
                "36-45", "46-60", "Above 60"
            ]

            groups = pd.cut(
                age_data,
                bins=bins,
                labels=labels
            )

            st.bar_chart(groups.value_counts().sort_index())
        else:
            st.info("No valid age values found.")
    else:
        st.info("Age column not found.")

st.divider()

# ---------------------------------
# COURSE PREFERENCES
# ---------------------------------

st.header("📚 Course Enrollment Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Course Category Preferences")

    if category_col:
        category_data = df[category_col].value_counts()
        st.bar_chart(category_data)
    else:
        st.info("Course category column not found.")

with col2:
    st.subheader("Course Level Distribution")

    if level_col:
        level_data = df[level_col].value_counts()
        st.bar_chart(level_data)
    else:
        st.info("Course level column not found.")

st.divider()

# ---------------------------------
# COURSE ENROLLMENT PATTERNS
# ---------------------------------

st.header("📈 Enrollment Patterns")

if date_col:
    dates = pd.to_datetime(
        df[date_col], errors="coerce"
    ).dropna()

    if not dates.empty:
        monthly = dates.dt.to_period("M").astype(str)
        monthly_counts = monthly.value_counts().sort_index()

        st.subheader("Monthly Enrollment Trends")
        st.line_chart(monthly_counts)
    else:
        st.info("No valid enrollment dates found.")
else:
    st.info(
        "Enrollment date column not detected. "
        "Upload a dataset containing enrollment dates "
        "to view monthly trends."
    )

if course_col:
    st.subheader("Top 10 Popular Courses")
    st.bar_chart(df[course_col].value_counts().head(10))

st.divider()

# ---------------------------------
# DATASET PREVIEW
# ---------------------------------

st.header("📋 Dataset Preview")

st.write("Dataset Shape:", df.shape)

st.dataframe(df, use_container_width=True)

# ---------------------------------
# DOWNLOAD CLEANED DATA
# ---------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Cleaned Dataset",
    data=csv,
    file_name="EduPro_Cleaned_Data.csv",
    mime="text/csv"
)

st.success("EduPro Analytics Dashboard is ready!")
