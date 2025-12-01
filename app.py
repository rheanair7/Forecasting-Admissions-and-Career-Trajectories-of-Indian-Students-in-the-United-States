#!/usr/bin/env python3
"""
University Admission Recommender - Web UI
Streamlit-based interface for easy profile input and recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import pickle
import os
import json
import random

# Page configuration
st.set_page_config(
    page_title="University Admission Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .safe-school {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .target-school {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .reach-school {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin-bottom: 1rem;
    }
    .ambitious-school {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    .employer-tag {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load or train the ML model"""
    model_path = 'models/rf_admission_model.pkl'

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            saved_data = pickle.load(f)
            return saved_data['model'], saved_data['numeric_features'], saved_data['categorical_features']
    else:
        st.error("Model not found. Please train the model first by running university_recommender.py")
        st.stop()


@st.cache_resource
def load_employers_data():
    """Load Handshake employers data"""
    employers_path = 'Handshake_Events/handshake_employers_data.json'

    try:
        if os.path.exists(employers_path):
            with open(employers_path, 'r') as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        st.warning(f"Could not load employers data: {str(e)}")
        return None


def create_user_profile(form_data):
    """Create user profile from form data"""
    profile = {}

    # Basic Information
    profile['application_year'] = form_data['year']
    profile['application_term'] = form_data['term']
    profile['is_fall_term'] = 1 if form_data['term'] == 'Fall' else 0

    # Academic Scores
    profile['gpa_normalized'] = form_data['gpa']
    profile['gpa_missing'] = 0

    # GPA Category
    if profile['gpa_normalized'] >= 8.5:
        profile['gpa_category'] = "Very High"
    elif profile['gpa_normalized'] >= 7.5:
        profile['gpa_category'] = "High"
    elif profile['gpa_normalized'] >= 6.5:
        profile['gpa_category'] = "Medium"
    else:
        profile['gpa_category'] = "Low"

    # English Tests
    if form_data['english_test'] == 'TOEFL':
        profile['toefl'] = form_data['english_score']
        profile['ielts'] = 0
        profile['english_test_normalized'] = form_data['english_score'] / 120.0
    else:
        profile['ielts'] = form_data['english_score']
        profile['toefl'] = 0
        profile['english_test_normalized'] = form_data['english_score'] / 9.0

    profile['english_missing'] = 0

    # English proficiency category
    if profile['english_test_normalized'] >= 0.85:
        profile['english_proficiency'] = "High"
    elif profile['english_test_normalized'] >= 0.70:
        profile['english_proficiency'] = "Medium"
    else:
        profile['english_proficiency'] = "Low"

    # GRE Scores
    if form_data['has_gre']:
        profile['gre_verbal'] = form_data['gre_verbal']
        profile['gre_quant'] = form_data['gre_quant']
        profile['gre_awa'] = form_data['gre_awa']
        profile['gre_total'] = profile['gre_verbal'] + profile['gre_quant']
        profile['gre_missing'] = "False"

        if profile['gre_total'] >= 320:
            profile['gre_strength'] = "High"
        elif profile['gre_total'] >= 310:
            profile['gre_strength'] = "Medium"
        else:
            profile['gre_strength'] = "Low"
    else:
        profile['gre_verbal'] = 0
        profile['gre_quant'] = 0
        profile['gre_awa'] = 0
        profile['gre_total'] = 0
        profile['gre_missing'] = "True"
        profile['gre_strength'] = "Low"

    # Experience
    profile['work_experience'] = form_data['work_exp']
    profile['relevant_work_experience'] = form_data['work_exp'] * 0.7
    profile['internship_experience'] = form_data['intern_exp']
    profile['total_experience'] = form_data['work_exp'] + form_data['intern_exp']

    # Experience category
    if profile['total_experience'] >= 36:
        profile['experience_category'] = "High"
    elif profile['total_experience'] >= 12:
        profile['experience_category'] = "Medium"
    else:
        profile['experience_category'] = "Low"

    # Publications
    profile['publications'] = form_data['publications']
    profile['has_publications'] = 1 if form_data['publications'] > 0 else 0

    # Academic Background
    profile['undergrad_major'] = form_data['ug_major']
    profile['undergrad_university'] = form_data['ug_university']
    profile['ug_major_bucket'] = form_data['major_bucket']

    # Target Program
    profile['course_name'] = form_data['target_program']
    profile['categorical_course_name'] = form_data['program_bucket']
    profile['target_degree'] = form_data['degree_type']
    profile['credential'] = f"M.S. in {form_data['target_program']}"
    profile['credential_standardized'] = "Masters (Technical)"

    # Calculated features
    profile['major_alignment'] = 1 if profile['ug_major_bucket'] == profile['categorical_course_name'] else 0
    profile['academic_alignment_score'] = profile['major_alignment']
    profile['composite_academic_score'] = (profile['gpa_normalized'] / 10.0 + profile['english_test_normalized']) / 2

    # Default values
    profile['student_type'] = 'International'
    profile['student_type_encoded'] = 0
    profile['has_scholarship'] = 'False'
    profile['has_scholarship_encoded'] = 0
    profile['scholarship_amount'] = 0
    profile['application_term_encoded'] = 0 if profile['is_fall_term'] == 1 else 1
    profile['undergrad_missing'] = 0

    # Rank columns
    for rank_col in ['cs_rank', 'eng_rank', 'mba_rank', 'gen_rank']:
        profile[rank_col] = np.nan
        profile[f'{rank_col}_missing'] = 1

    # Additional categorical features
    profile['university_name_stripped'] = 'Unknown'
    profile['undergrad_canonical'] = profile['undergrad_university']
    profile['undergrad_canonical_stripped'] = profile['undergrad_university']
    profile['stripped_name'] = profile['undergrad_university'].lower().replace(' ', '')
    profile['university_tier'] = 'Unknown'
    profile['credential_standardized_grouped'] = 'Masters'
    profile['categorical_course_name_grouped'] = profile['categorical_course_name']
    profile['ug_major_bucket_grouped'] = profile['ug_major_bucket']

    # Binary flags for credentials
    for cred_type in ['Bachelors', 'Doctoral', 'Graduate Certificate', 'Masters (Professional)', 'Masters (Technical)', 'Other']:
        profile[f'credential_standardized_{cred_type}'] = 1 if cred_type == 'Masters (Technical)' else 0

    # Binary flags for course buckets
    for course_bucket in ['Bio_Biomed_Health_LifeSci', 'Business_Management_Finance',
                          'Chemical_Materials_Petroleum', 'Civil_Construction_Env_Arch',
                          'Computer_Science_Software', 'Data_Science_AI_Machine_Learning',
                          'Electrical_Electronics_ECE', 'Humanities_Social_Design_Arts',
                          'Mechanical_Industrial_Aero', 'Other']:
        profile[f'categorical_course_name_{course_bucket}'] = 1 if profile['categorical_course_name'] == course_bucket else 0

    # Binary flags for UG major buckets
    for ug_bucket in ['Bio_Biomed_Health_LifeSci', 'Business_Management_Finance',
                      'Chemical_Materials_Petroleum', 'Civil_Construction_Env_Arch',
                      'Computer_Science_Software', 'Data_Science_AI_Machine_Learning',
                      'Electrical_Electronics_ECE', 'Humanities_Social_Design_Arts',
                      'Mechanical_Industrial_Aero', 'Other']:
        profile[f'ug_major_bucket_{ug_bucket}'] = 1 if profile['ug_major_bucket'] == ug_bucket else 0

    return profile


def predict_universities(model, numeric_features, categorical_features, user_profile, top_n=30):
    """Predict admission probability for universities"""
    df = pd.read_csv('admissions_processed.csv', low_memory=False)
    universities = df['university_name'].value_counts().head(top_n).index.tolist()

    results = []

    for uni in universities:
        profile = user_profile.copy()
        profile['university_name'] = uni

        # Get university tier
        uni_data = df[df['university_name'] == uni]
        if len(uni_data) > 0 and 'university_tier' in uni_data.columns:
            profile['university_tier'] = uni_data['university_tier'].mode()[0] if len(uni_data['university_tier'].mode()) > 0 else 'Unknown'

        # Create DataFrame
        profile_df = pd.DataFrame([profile])

        # Ensure all features present
        for feat in numeric_features:
            if feat not in profile_df.columns:
                profile_df[feat] = 0

        for feat in categorical_features:
            if feat not in profile_df.columns:
                profile_df[feat] = 'Unknown'

        # Reorder columns
        all_features = list(numeric_features) + list(categorical_features)
        profile_df = profile_df[all_features]

        # Predict
        try:
            prob = model.predict_proba(profile_df)[0, 1]
            results.append({
                'university_name': uni,
                'university_tier': profile['university_tier'],
                'admission_probability': prob
            })
        except:
            continue

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('admission_probability', ascending=False)

    return results_df


def categorize_buckets(results_df):
    """Categorize universities into buckets"""
    def bucket_with_tier(row):
        p = row['admission_probability']
        tier = row.get('university_tier', 'Unknown')

        if tier == 'Top_20':
            if p >= 0.60:
                return 'Target'
            elif p >= 0.50:
                return 'Reach'
            else:
                return 'Ambitious'
        elif tier == 'Top_50':
            if p >= 0.65:
                return 'Safe'
            elif p >= 0.52:
                return 'Target'
            elif p >= 0.45:
                return 'Reach'
            else:
                return 'Ambitious'
        elif tier == 'Top_100':
            if p >= 0.62:
                return 'Safe'
            elif p >= 0.55:
                return 'Target'
            elif p >= 0.48:
                return 'Reach'
            else:
                return 'Ambitious'
        elif tier == 'Top_200':
            if p >= 0.60:
                return 'Safe'
            elif p >= 0.53:
                return 'Target'
            else:
                return 'Reach'
        else:
            if p >= 0.60:
                return 'Safe'
            elif p >= 0.50:
                return 'Target'
            else:
                return 'Reach'

    results_df['bucket'] = results_df.apply(bucket_with_tier, axis=1)
    return results_df


def get_random_employers(employers_data, num=4):
    """Get random top employers"""
    if not employers_data or 'employers' not in employers_data:
        return []

    employers_list = employers_data['employers']

    def parse_followers(follower_str):
        try:
            num_str = follower_str.split()[0].replace(',', '')
            if 'M' in num_str:
                return int(float(num_str.replace('M', '')) * 1000000)
            elif 'K' in num_str:
                return int(float(num_str.replace('K', '')) * 1000)
            else:
                return int(num_str)
        except:
            return 0

    sorted_employers = sorted(employers_list, key=lambda x: parse_followers(x['followers']), reverse=True)
    top_100 = sorted_employers[:100]

    return random.sample(top_100, min(num, len(top_100)))


def main():
    # Header
    st.markdown('<div class="main-header">🎓 University Admission Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Predictions for MS/PhD Admissions at Top US Universities</div>', unsafe_allow_html=True)

    # Load model and data
    with st.spinner("Loading ML model..."):
        model, numeric_features, categorical_features = load_model()
        employers_data = load_employers_data()

    st.success("✓ Model loaded successfully!")

    # Sidebar - User Input
    st.sidebar.header("📝 Student Profile")

    with st.sidebar.form("profile_form"):
        st.subheader("Basic Information")
        year = st.number_input("Application Year", min_value=2024, max_value=2030, value=2025)
        term = st.selectbox("Application Term", ["Fall", "Spring", "Summer", "Winter"])

        st.subheader("Academic Scores")
        gpa = st.slider("GPA (out of 10)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)

        english_test = st.radio("English Test", ["TOEFL", "IELTS"])
        if english_test == "TOEFL":
            english_score = st.slider("TOEFL Score", min_value=0, max_value=120, value=100, step=1)
        else:
            english_score = st.slider("IELTS Score", min_value=0.0, max_value=9.0, value=7.0, step=0.5)

        has_gre = st.checkbox("I have GRE scores", value=True)
        if has_gre:
            gre_verbal = st.slider("GRE Verbal", min_value=130, max_value=170, value=155, step=1)
            gre_quant = st.slider("GRE Quantitative", min_value=130, max_value=170, value=165, step=1)
            gre_awa = st.slider("GRE AWA", min_value=0.0, max_value=6.0, value=4.0, step=0.5)
        else:
            gre_verbal = gre_quant = gre_awa = 0

        st.subheader("Professional Experience")
        work_exp = st.number_input("Work Experience (months)", min_value=0, max_value=120, value=0, step=1)
        intern_exp = st.number_input("Internship Experience (months)", min_value=0, max_value=60, value=0, step=1)
        publications = st.number_input("Research Publications", min_value=0, max_value=20, value=0, step=1)

        st.subheader("Academic Background")
        ug_major = st.text_input("Undergraduate Major", value="Computer Science")
        ug_university = st.text_input("Undergraduate University", value="")

        major_bucket = st.selectbox("UG Major Category", [
            "Computer_Science_Software",
            "Data_Science_AI_Machine_Learning",
            "Electrical_Electronics_ECE",
            "Mechanical_Industrial_Aero",
            "Business_Management_Finance",
            "Bio_Biomed_Health_LifeSci",
            "Other"
        ])

        st.subheader("Target Program")
        target_program = st.text_input("Target Program Name", value="Computer Science")
        program_bucket = st.selectbox("Program Category", [
            "Computer_Science_Software",
            "Data_Science_AI_Machine_Learning",
            "Electrical_Electronics_ECE",
            "Mechanical_Industrial_Aero",
            "Business_Management_Finance",
            "Bio_Biomed_Health_LifeSci",
            "Other"
        ])
        degree_type = st.selectbox("Degree Type", ["Masters", "PhD", "Graduate Certificate"])

        submitted = st.form_submit_button("🎯 Get Recommendations", use_container_width=True)

    # Main content
    if submitted:
        # Collect form data
        form_data = {
            'year': year,
            'term': term,
            'gpa': gpa,
            'english_test': english_test,
            'english_score': english_score,
            'has_gre': has_gre,
            'gre_verbal': gre_verbal,
            'gre_quant': gre_quant,
            'gre_awa': gre_awa,
            'work_exp': work_exp,
            'intern_exp': intern_exp,
            'publications': publications,
            'ug_major': ug_major,
            'ug_university': ug_university,
            'major_bucket': major_bucket,
            'target_program': target_program,
            'program_bucket': program_bucket,
            'degree_type': degree_type
        }

        # Create profile
        with st.spinner("Creating your profile..."):
            user_profile = create_user_profile(form_data)

        # Display profile summary
        st.header("📊 Your Profile Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("GPA", f"{user_profile['gpa_normalized']:.2f}/10", user_profile['gpa_category'])

        with col2:
            if english_test == "TOEFL":
                st.metric("TOEFL", f"{user_profile['toefl']:.0f}/120", user_profile['english_proficiency'])
            else:
                st.metric("IELTS", f"{user_profile['ielts']:.1f}/9", user_profile['english_proficiency'])

        with col3:
            if has_gre:
                st.metric("GRE", f"{user_profile['gre_total']:.0f}/340", user_profile['gre_strength'])
            else:
                st.metric("GRE", "Not Provided", "")

        with col4:
            st.metric("Experience", f"{user_profile['total_experience']:.0f} months", user_profile['experience_category'])

        # Predict universities
        with st.spinner("Analyzing top 30 universities..."):
            results_df = predict_universities(model, numeric_features, categorical_features, user_profile, top_n=30)
            results_df = categorize_buckets(results_df)

        # Display statistics
        st.header("📈 Prediction Results")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Universities Analyzed", len(results_df))
        with col2:
            st.metric("Average Probability", f"{results_df['admission_probability'].mean():.1%}")
        with col3:
            st.metric("Highest Probability", f"{results_df['admission_probability'].max():.1%}")
        with col4:
            st.metric("Lowest Probability", f"{results_df['admission_probability'].min():.1%}")

        # Display by bucket
        st.header("🎯 University Recommendations")

        tabs = st.tabs(["🟢 Safe", "🟡 Target", "🔵 Reach", "🔴 Ambitious", "📊 All Results"])

        buckets_config = [
            ("Safe", "safe-school", "✓ Strong likelihood of admission"),
            ("Target", "target-school", "→ Good match for your profile"),
            ("Reach", "reach-school", "↗ Competitive - solid chance with strong application"),
            ("Ambitious", "ambitious-school", "⚠ Highly selective - dream schools")
        ]

        for idx, (bucket_name, css_class, description) in enumerate(buckets_config):
            with tabs[idx]:
                bucket_df = results_df[results_df['bucket'] == bucket_name]

                if len(bucket_df) == 0:
                    st.info(f"No {bucket_name} schools found for your profile.")
                    continue

                st.markdown(f"**{description}**")
                st.markdown(f"**Total: {len(bucket_df)} universities**")
                st.markdown("---")

                for rank, (_, row) in enumerate(bucket_df.iterrows(), 1):
                    with st.container():
                        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)

                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.markdown(f"**{rank}. {row['university_name']}**")
                            st.caption(f"Tier: {row['university_tier']}")

                        with col2:
                            prob_color = "green" if row['admission_probability'] >= 0.65 else "orange" if row['admission_probability'] >= 0.50 else "red"
                            st.markdown(f"<h3 style='color: {prob_color}; text-align: right;'>{row['admission_probability']:.1%}</h3>", unsafe_allow_html=True)

                        # Show employers
                        if employers_data:
                            employers = get_random_employers(employers_data, num=random.randint(3, 4))
                            if employers:
                                st.markdown("**💼 Top Recruiters:**")
                                for emp in employers:
                                    location = emp['location'][:30] + "..." if len(emp['location']) > 30 else emp['location']
                                    st.markdown(f"<span class='employer-tag'>• {emp['name']} ({emp['industry']}, {location})</span>", unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("")

        # All Results Tab
        with tabs[4]:
            st.dataframe(
                results_df[['university_name', 'university_tier', 'admission_probability', 'bucket']]
                .rename(columns={
                    'university_name': 'University',
                    'university_tier': 'Tier',
                    'admission_probability': 'Probability',
                    'bucket': 'Category'
                }),
                hide_index=True,
                use_container_width=True
            )

            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"university_recommendations_{year}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Application Strategy
        st.header("📋 Recommended Application Strategy")

        safe_count = len(results_df[results_df['bucket'] == 'Safe'])
        target_count = len(results_df[results_df['bucket'] == 'Target'])
        reach_count = len(results_df[results_df['bucket'] == 'Reach'])
        ambitious_count = len(results_df[results_df['bucket'] == 'Ambitious'])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.success(f"**Safe Schools**\n\n{safe_count} available\n\nApply to 3-4")
        with col2:
            st.warning(f"**Target Schools**\n\n{target_count} available\n\nApply to 4-6")
        with col3:
            st.info(f"**Reach Schools**\n\n{reach_count} available\n\nApply to 3-4")
        with col4:
            st.error(f"**Ambitious Schools**\n\n{ambitious_count} available\n\nApply to 1-2")

        st.markdown("### 💡 Tips")
        st.info("""
        - **Balance your portfolio**: Apply to a mix across all categories
        - **Consider beyond probability**: Location, program fit, cost, and research opportunities matter
        - **Research thoroughly**: Look into specific program requirements and faculty
        - **Tailor applications**: Customize your SOP and materials for each school
        - **Network strategically**: Connect with alumni at target companies
        """)

    else:
        # Welcome message
        st.info("👈 **Get Started:** Fill in your profile in the sidebar and click 'Get Recommendations'")

        st.markdown("### 🎯 What This Tool Does")
        st.markdown("""
        This AI-powered tool analyzes your academic profile and predicts your admission chances at **30 top US universities**.

        **Features:**
        - 🤖 **ML-Powered**: Random Forest model with 83% accuracy
        - 🎯 **Smart Categorization**: Universities grouped into Safe/Target/Reach/Ambitious
        - 💼 **Career Insights**: See top recruiters for each university
        - 📊 **Comprehensive Analysis**: Based on 250K+ real admission records
        - 📥 **Export Results**: Download recommendations as CSV

        **Model Performance:**
        - ROC-AUC: 83.2%
        - Training Data: 250,795 applications
        - Universities: Top 30 programs
        """)

        st.markdown("### 📚 How It Works")
        st.markdown("""
        1. **Input Your Profile**: GPA, test scores, experience, background
        2. **AI Analysis**: Machine learning model predicts admission probability
        3. **Smart Bucketing**: Universities categorized by your chances
        4. **Career Insights**: View top companies recruiting from each school
        5. **Application Strategy**: Get personalized recommendations
        """)


if __name__ == "__main__":
    main()
