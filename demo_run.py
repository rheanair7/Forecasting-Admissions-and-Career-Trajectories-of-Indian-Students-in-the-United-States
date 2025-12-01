#!/usr/bin/env python3
"""
Demo run of University Recommender with pre-filled profile
Shows the system in action without requiring manual input
"""

import sys
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

# Import the recommender class
from university_recommender import UniversityRecommender

def create_sample_profile():
    """Create a sample student profile"""
    print("\n" + "="*80)
    print("🎓 DEMO MODE - Using Pre-filled Sample Profile")
    print("="*80)

    profile = {
        'application_year': 2025,
        'application_term': 'Fall',
        'is_fall_term': 1,
        'gpa_normalized': 8.5,
        'gpa_missing': 0,
        'gpa_category': 'Very High',
        'toefl': 105,
        'ielts': 0,
        'english_test_normalized': 105 / 120.0,
        'english_missing': 0,
        'english_proficiency': 'High',
        'gre_verbal': 162,
        'gre_quant': 168,
        'gre_awa': 4.0,
        'gre_total': 330,
        'gre_missing': 'False',
        'gre_strength': 'High',
        'work_experience': 12,
        'relevant_work_experience': 8.4,
        'internship_experience': 3,
        'total_experience': 15,
        'experience_category': 'Medium',
        'publications': 0,
        'has_publications': 0,
        'undergrad_major': 'Computer Science',
        'undergrad_university': 'IIT Bombay',
        'ug_major_bucket': 'Computer_Science_Software',
        'course_name': 'Computer Science',
        'categorical_course_name': 'Computer_Science_Software',
        'target_degree': 'Masters',
        'credential': 'M.S. in Computer Science',
        'credential_standardized': 'Masters (Technical)',
        'major_alignment': 1,
        'academic_alignment_score': 1,
        'composite_academic_score': (8.5 / 10.0 + 105 / 120.0) / 2,
        'student_type': 'International',
        'student_type_encoded': 0,
        'has_scholarship': 'False',
        'has_scholarship_encoded': 0,
        'scholarship_amount': 0,
        'application_term_encoded': 0,
        'undergrad_missing': 0,
        'university_name_stripped': 'Unknown',
        'undergrad_canonical': 'IIT Bombay',
        'undergrad_canonical_stripped': 'IIT Bombay',
        'stripped_name': 'iitbombay',
        'university_tier': 'Unknown',
        'credential_standardized_grouped': 'Masters',
        'categorical_course_name_grouped': 'Computer_Science_Software',
        'ug_major_bucket_grouped': 'Computer_Science_Software',
    }

    # Rank columns
    for rank_col in ['cs_rank', 'eng_rank', 'mba_rank', 'gen_rank']:
        profile[rank_col] = np.nan
        profile[f'{rank_col}_missing'] = 1

    # Binary flags for credentials
    for cred_type in ['Bachelors', 'Doctoral', 'Graduate Certificate', 'Masters (Professional)', 'Masters (Technical)', 'Other']:
        profile[f'credential_standardized_{cred_type}'] = 1 if cred_type == 'Masters (Technical)' else 0

    # Binary flags for course buckets
    for course_bucket in ['Bio_Biomed_Health_LifeSci', 'Business_Management_Finance',
                          'Chemical_Materials_Petroleum', 'Civil_Construction_Env_Arch',
                          'Computer_Science_Software', 'Data_Science_AI_Machine_Learning',
                          'Electrical_Electronics_ECE', 'Humanities_Social_Design_Arts',
                          'Mechanical_Industrial_Aero', 'Other']:
        profile[f'categorical_course_name_{course_bucket}'] = 1 if course_bucket == 'Computer_Science_Software' else 0

    # Binary flags for UG major buckets
    for ug_bucket in ['Bio_Biomed_Health_LifeSci', 'Business_Management_Finance',
                      'Chemical_Materials_Petroleum', 'Civil_Construction_Env_Arch',
                      'Computer_Science_Software', 'Data_Science_AI_Machine_Learning',
                      'Electrical_Electronics_ECE', 'Humanities_Social_Design_Arts',
                      'Mechanical_Industrial_Aero', 'Other']:
        profile[f'ug_major_bucket_{ug_bucket}'] = 1 if ug_bucket == 'Computer_Science_Software' else 0

    return profile


def main():
    print("\n" + "="*80)
    print(" "*15 + "🎓 UNIVERSITY ADMISSION RECOMMENDER - DEMO MODE 🎓")
    print("="*80)
    print("\nThis demo shows the system in action with a pre-filled profile.")
    print("For interactive mode, run: python3 university_recommender.py")
    print("="*80)

    # Initialize recommender
    recommender = UniversityRecommender(
        model_path='models/rf_admission_model.pkl',
        data_path='admissions_processed.csv',
        employers_path='Handshake_Events/handshake_employers_data.json'
    )

    # Load or train model
    recommender.load_or_train_model()

    # Create sample profile
    user_profile = create_sample_profile()

    # Display profile
    print("\n" + "="*80)
    print("📊 SAMPLE STUDENT PROFILE")
    print("="*80)
    print(f"GPA: {user_profile['gpa_normalized']:.2f}/10 ({user_profile['gpa_category']})")
    print(f"English: TOEFL {user_profile['toefl']:.0f} ({user_profile['english_proficiency']})")
    print(f"GRE: V{user_profile['gre_verbal']:.0f} + Q{user_profile['gre_quant']:.0f} + AWA{user_profile['gre_awa']:.1f} = {user_profile['gre_total']:.0f} ({user_profile['gre_strength']})")
    print(f"Experience: {user_profile['total_experience']:.0f} months ({user_profile['experience_category']})")
    print(f"Publications: {user_profile['publications']}")
    print(f"UG Major: {user_profile['undergrad_major']} from {user_profile['undergrad_university']}")
    print(f"Target: {user_profile['course_name']} ({user_profile['target_degree']})")
    print(f"Term: {user_profile['application_term']} {user_profile['application_year']}")
    print("="*80)

    # Predict for universities
    print("\nAnalyzing top 30 universities...")
    results_df = recommender.predict_universities(user_profile, top_n=30)

    # Categorize into buckets
    results_df = recommender.categorize_into_buckets(results_df)

    # Display recommendations
    recommender.display_recommendations(results_df)

    # Save results
    filename = f"demo_recommendations_{user_profile['application_year']}.csv"
    results_df.to_csv(filename, index=False)
    print(f"\n✓ Demo results saved to {filename}")

    print("\n" + "="*80)
    print("🎓 Demo Complete!")
    print("="*80)
    print("\nTo run with YOUR profile:")
    print("  python3 university_recommender.py")
    print("\nTo see this demo again:")
    print("  python3 demo_run.py")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
