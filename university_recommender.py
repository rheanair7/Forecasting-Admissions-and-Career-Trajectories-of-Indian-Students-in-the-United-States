#!/usr/bin/env python3
"""
University Admission Recommender System
Terminal-based interface for predicting admission chances and recommending universities
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, roc_auc_score
import pickle
import os
import sys
import json
import random


class UniversityRecommender:
    def __init__(self, model_path='models/rf_model.pkl', data_path='admissions_processed.csv',
                 employers_path='Handshake_Events/handshake_employers_data.json'):
        self.model_path = model_path
        self.data_path = data_path
        self.employers_path = employers_path
        self.model = None
        self.numeric_features = None
        self.categorical_features = None
        self.df = None
        self.universities = None
        self.employers_data = None

    def load_or_train_model(self):
        """Load existing model or train a new one"""
        if os.path.exists(self.model_path):
            print("Loading existing model...")
            with open(self.model_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.model = saved_data['model']
                self.numeric_features = saved_data['numeric_features']
                self.categorical_features = saved_data['categorical_features']
            print("✓ Model loaded successfully!")
        else:
            print("Training new model (this may take a few minutes)...")
            self._train_model()

        # Load employers data
        self._load_employers_data()

    def _load_employers_data(self):
        """Load Handshake employers data"""
        try:
            if os.path.exists(self.employers_path):
                with open(self.employers_path, 'r') as f:
                    self.employers_data = json.load(f)
                print(f"✓ Loaded {self.employers_data['total_employers']} employers from Handshake")
            else:
                print("⚠️  Handshake employers data not found - skipping employer recommendations")
                self.employers_data = None
        except Exception as e:
            print(f"⚠️  Could not load employers data: {str(e)}")
            self.employers_data = None

    def _train_model(self):
        """Train the Random Forest model"""
        # Load data
        print("Loading data...")
        self.df = pd.read_csv(self.data_path, low_memory=False)

        # Handle rank columns
        rank_cols = ["cs_rank", "eng_rank", "mba_rank", "gen_rank"]
        for col in rank_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].replace(9999, np.nan)
                self.df[f"{col}_missing"] = self.df[col].isna().astype(int)

        # Prepare features and target
        y = self.df["admission_result"]
        drop_cols = [
            "admission_result", "student_name", "student_id", "id",
            "gpa", "gpa_scale", "scholarship_currency"
        ]
        X = self.df.drop(columns=[c for c in drop_cols if c in self.df.columns])

        if "application_status" in X.columns:
            X = X.drop(columns=["application_status"])

        # Identify feature types
        self.numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_features = [c for c in X.columns if c not in self.numeric_features]
        X[self.categorical_features] = X[self.categorical_features].astype(str)

        # Build preprocessing pipeline
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])

        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore")),
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.numeric_features),
                ("cat", categorical_transformer, self.categorical_features),
            ]
        )

        # Build model pipeline
        rf = RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features="sqrt",
            bootstrap=True,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        )

        self.model = Pipeline(steps=[
            ("preprocess", preprocessor),
            ("rf", rf),
        ])

        # Train model
        print("Training Random Forest model...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]

        print("\n=== Model Performance ===")
        print(classification_report(y_test, y_pred))
        print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

        # Save model
        os.makedirs(os.path.dirname(self.model_path) if os.path.dirname(self.model_path) else 'models', exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'numeric_features': self.numeric_features,
                'categorical_features': self.categorical_features
            }, f)
        print(f"✓ Model saved to {self.model_path}")

    def get_user_profile(self):
        """Collect user profile information via terminal input"""
        print("\n" + "="*80)
        print(" "*25 + "STUDENT PROFILE INPUT")
        print("="*80)

        profile = {}

        # Basic Information
        print("\n--- Basic Information ---")
        profile['application_year'] = int(input("Application Year (e.g., 2025): ") or 2025)
        profile['application_term'] = input("Application Term (Fall/Spring/Summer/Winter): ").strip().title() or "Fall"
        profile['is_fall_term'] = 1 if profile['application_term'].lower() == 'fall' else 0

        # Academic Scores
        print("\n--- Academic Scores ---")
        gpa_input = input("GPA (out of 10, e.g., 8.5): ").strip()
        profile['gpa_normalized'] = float(gpa_input) if gpa_input else 7.5
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
        print("\n--- English Proficiency (Enter one) ---")
        test_choice = input("Which test? (1) TOEFL (2) IELTS: ").strip()

        if test_choice == "1":
            toefl = input("TOEFL Score (out of 120, e.g., 100): ").strip()
            profile['toefl'] = float(toefl) if toefl else 100
            profile['ielts'] = 0
            profile['english_test_normalized'] = profile['toefl'] / 120.0
        else:
            ielts = input("IELTS Score (out of 9, e.g., 7.5): ").strip()
            profile['ielts'] = float(ielts) if ielts else 7.0
            profile['toefl'] = 0
            profile['english_test_normalized'] = profile['ielts'] / 9.0

        profile['english_missing'] = 0

        # English proficiency category
        if profile['english_test_normalized'] >= 0.85:
            profile['english_proficiency'] = "High"
        elif profile['english_test_normalized'] >= 0.70:
            profile['english_proficiency'] = "Medium"
        else:
            profile['english_proficiency'] = "Low"

        # GRE Scores
        print("\n--- GRE Scores (Optional - press Enter to skip) ---")
        has_gre = input("Do you have GRE scores? (yes/no): ").strip().lower()

        if has_gre in ['yes', 'y']:
            gre_verbal = input("GRE Verbal (out of 170, e.g., 160): ").strip()
            gre_quant = input("GRE Quant (out of 170, e.g., 165): ").strip()
            gre_awa = input("GRE AWA (out of 6, e.g., 4.0): ").strip()

            profile['gre_verbal'] = float(gre_verbal) if gre_verbal else 155
            profile['gre_quant'] = float(gre_quant) if gre_quant else 160
            profile['gre_awa'] = float(gre_awa) if gre_awa else 3.5
            profile['gre_total'] = profile['gre_verbal'] + profile['gre_quant']
            profile['gre_missing'] = "False"

            # GRE strength
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
        print("\n--- Professional Experience (in months) ---")
        work_exp = input("Work Experience (months, e.g., 24): ").strip()
        profile['work_experience'] = float(work_exp) if work_exp else 0
        profile['relevant_work_experience'] = profile['work_experience'] * 0.7  # Assume 70% relevant

        intern_exp = input("Internship Experience (months, e.g., 6): ").strip()
        profile['internship_experience'] = float(intern_exp) if intern_exp else 0

        profile['total_experience'] = profile['work_experience'] + profile['internship_experience']

        # Experience category
        if profile['total_experience'] >= 36:
            profile['experience_category'] = "High"
        elif profile['total_experience'] >= 12:
            profile['experience_category'] = "Medium"
        else:
            profile['experience_category'] = "Low"

        # Publications
        pubs = input("Number of Publications/Research Papers: ").strip()
        profile['publications'] = int(pubs) if pubs else 0
        profile['has_publications'] = 1 if profile['publications'] > 0 else 0

        # Academic Background
        print("\n--- Academic Background ---")
        profile['undergrad_major'] = input("Undergraduate Major (e.g., Computer Science): ").strip() or "Computer Science"
        profile['undergrad_university'] = input("Undergraduate University: ").strip() or "Unknown University"

        # Determine UG major bucket
        ug_major_lower = profile['undergrad_major'].lower()
        if 'computer' in ug_major_lower or 'cs' in ug_major_lower or 'software' in ug_major_lower:
            profile['ug_major_bucket'] = "Computer_Science_Software"
        elif 'data' in ug_major_lower or 'machine' in ug_major_lower or 'ai' in ug_major_lower:
            profile['ug_major_bucket'] = "Data_Science_AI_Machine_Learning"
        elif 'electric' in ug_major_lower or 'ece' in ug_major_lower or 'electronics' in ug_major_lower:
            profile['ug_major_bucket'] = "Electrical_Electronics_ECE"
        elif 'mechanical' in ug_major_lower or 'industrial' in ug_major_lower or 'aero' in ug_major_lower:
            profile['ug_major_bucket'] = "Mechanical_Industrial_Aero"
        elif 'business' in ug_major_lower or 'management' in ug_major_lower or 'finance' in ug_major_lower:
            profile['ug_major_bucket'] = "Business_Management_Finance"
        else:
            profile['ug_major_bucket'] = "Other"

        # Target Program
        print("\n--- Target Program ---")
        print("Common programs:")
        print("1. Computer Science")
        print("2. Data Science / AI / Machine Learning")
        print("3. Electrical Engineering")
        print("4. Mechanical Engineering")
        print("5. Business / MBA")
        print("6. Other")

        program_choice = input("Choose program (1-6) or type custom: ").strip()

        program_map = {
            '1': ('Computer Science', 'Computer_Science_Software'),
            '2': ('Data Science', 'Data_Science_AI_Machine_Learning'),
            '3': ('Electrical Engineering', 'Electrical_Electronics_ECE'),
            '4': ('Mechanical Engineering', 'Mechanical_Industrial_Aero'),
            '5': ('Business Administration', 'Business_Management_Finance'),
        }

        if program_choice in program_map:
            profile['course_name'], profile['categorical_course_name'] = program_map[program_choice]
        else:
            profile['course_name'] = input("Enter program name: ").strip() or "Computer Science"
            profile['categorical_course_name'] = "Other"

        # Degree type
        profile['target_degree'] = input("Target Degree (Masters/PhD/Graduate Certificate): ").strip() or "Masters"
        profile['credential'] = f"M.S. in {profile['course_name']}"
        profile['credential_standardized'] = "Masters (Technical)"

        # Calculate derived features
        profile['major_alignment'] = 1 if profile['ug_major_bucket'] == profile['categorical_course_name'] else 0
        profile['academic_alignment_score'] = profile['major_alignment']
        profile['composite_academic_score'] = (profile['gpa_normalized'] / 10.0 + profile['english_test_normalized']) / 2

        # Default values for missing features
        profile['student_type'] = 'International'
        profile['student_type_encoded'] = 0
        profile['has_scholarship'] = 'False'
        profile['has_scholarship_encoded'] = 0
        profile['scholarship_amount'] = 0
        profile['application_term_encoded'] = 0 if profile['is_fall_term'] == 1 else 1
        profile['undergrad_missing'] = 0

        # Rank columns (default to missing)
        for rank_col in ['cs_rank', 'eng_rank', 'mba_rank', 'gen_rank']:
            profile[rank_col] = np.nan
            profile[f'{rank_col}_missing'] = 1

        # Additional categorical features with defaults
        profile['university_name_stripped'] = 'Unknown'
        profile['undergrad_canonical'] = profile['undergrad_university']
        profile['undergrad_canonical_stripped'] = profile['undergrad_university']
        profile['stripped_name'] = profile['undergrad_university'].lower().replace(' ', '')
        profile['university_tier'] = 'Unknown'
        profile['credential_standardized_grouped'] = 'Masters'
        profile['categorical_course_name_grouped'] = profile['categorical_course_name']
        profile['ug_major_bucket_grouped'] = profile['ug_major_bucket']

        # Binary flags for credential types
        for cred_type in ['Bachelors', 'Doctoral', 'Graduate Certificate', 'Masters (Professional)', 'Masters (Technical)', 'Other']:
            profile[f'credential_standardized_{cred_type}'] = 1 if profile['credential_standardized'] == cred_type else 0

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

    def predict_universities(self, user_profile, top_n=30):
        """Predict admission probability for universities"""
        # Load university data
        df = pd.read_csv(self.data_path, low_memory=False)

        # Get unique universities
        universities = df['university_name'].value_counts().head(top_n).index.tolist()

        results = []

        print(f"\n{'='*80}")
        print(f"Calculating admission probabilities for top {top_n} universities...")
        print(f"{'='*80}\n")

        for uni in universities:
            # Create a copy of user profile
            profile = user_profile.copy()
            profile['university_name'] = uni

            # Get university tier if available
            uni_data = df[df['university_name'] == uni]
            if len(uni_data) > 0 and 'university_tier' in uni_data.columns:
                profile['university_tier'] = uni_data['university_tier'].mode()[0] if len(uni_data['university_tier'].mode()) > 0 else 'Unknown'

            # Create DataFrame with all required features
            profile_df = pd.DataFrame([profile])

            # Ensure all required features are present
            for feat in self.numeric_features:
                if feat not in profile_df.columns:
                    profile_df[feat] = 0

            for feat in self.categorical_features:
                if feat not in profile_df.columns:
                    profile_df[feat] = 'Unknown'

            # Reorder columns to match training
            all_features = self.numeric_features + self.categorical_features
            profile_df = profile_df[all_features]

            # Predict
            try:
                prob = self.model.predict_proba(profile_df)[0, 1]
                results.append({
                    'university_name': uni,
                    'university_tier': profile['university_tier'],
                    'admission_probability': prob
                })
            except Exception as e:
                print(f"Warning: Could not predict for {uni}: {str(e)}")
                continue

        # Convert to DataFrame
        results_df = pd.DataFrame(results)

        # Sort by probability
        results_df = results_df.sort_values('admission_probability', ascending=False)

        return results_df

    def categorize_into_buckets(self, results_df):
        """Categorize universities into Safe/Target/Ambitious buckets"""

        def bucket_with_tier(row):
            p = row['admission_probability']
            tier = row.get('university_tier', 'Unknown')

            # Adjust thresholds based on tier - More granular bucketing
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
                # Others tier - more lenient
                if p >= 0.60:
                    return 'Safe'
                elif p >= 0.50:
                    return 'Target'
                else:
                    return 'Reach'

        results_df['bucket'] = results_df.apply(bucket_with_tier, axis=1)

        return results_df

    def _display_employers_for_university(self, university_name):
        """Display 3-4 random top employers recruiting from this university"""
        if not self.employers_data or 'employers' not in self.employers_data:
            return

        # Get top employers by followers (more prominent companies)
        employers_list = self.employers_data['employers']

        # Parse follower count helper
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

        # Sort by followers and get top employers
        sorted_employers = sorted(employers_list,
                                  key=lambda x: parse_followers(x['followers']),
                                  reverse=True)

        # Select 3-4 random employers from top 100 (mix of very top and good companies)
        top_100 = sorted_employers[:100]
        num_to_show = random.randint(3, 4)
        selected = random.sample(top_100, min(num_to_show, len(top_100)))

        print(f"      💼 Top Recruiters ({len(selected)} companies):")
        for emp in selected:
            # Truncate location if too long
            location = emp['location'][:25] + "..." if len(emp['location']) > 28 else emp['location']
            print(f"         • {emp['name']} ({emp['industry']}, {location})")
        print()  # Empty line for spacing

    def display_recommendations(self, results_df):
        """Display university recommendations in buckets"""
        print("\n" + "="*80)
        print(" "*20 + "UNIVERSITY RECOMMENDATIONS")
        print("="*80)

        # Summary statistics
        print(f"\nTotal universities analyzed: {len(results_df)}")
        print(f"Average admission probability: {results_df['admission_probability'].mean():.1%}")
        print(f"Highest probability: {results_df['admission_probability'].max():.1%}")
        print(f"Lowest probability: {results_df['admission_probability'].min():.1%}")

        # Display by bucket
        buckets = ['Safe', 'Target', 'Reach', 'Ambitious']

        for bucket in buckets:
            bucket_df = results_df[results_df['bucket'] == bucket]

            if len(bucket_df) == 0:
                continue

            print(f"\n{'='*80}")
            print(f"🎯 {bucket.upper()} SCHOOLS ({len(bucket_df)} universities)")
            print(f"{'='*80}")

            if bucket == 'Safe':
                print("✓ Strong likelihood of admission - these are your safety schools.")
            elif bucket == 'Target':
                print("→ Good match for your profile - realistic chances with strong application.")
            elif bucket == 'Reach':
                print("↗ Competitive schools - solid chance but prepare thoroughly.")
            else:
                print("⚠ Highly selective - consider as ambitious/dream schools.")

            print(f"\n{'Rank':<6}{'University':<50}{'Tier':<15}{'Probability':<15}")
            print("-"*80)

            for idx, (_, row) in enumerate(bucket_df.iterrows(), 1):
                uni_name = row['university_name'][:47] + "..." if len(row['university_name']) > 50 else row['university_name']
                tier = row['university_tier'] if row['university_tier'] != 'Unknown' else 'N/A'
                prob = f"{row['admission_probability']:.1%}"

                print(f"{idx:<6}{uni_name:<50}{tier:<15}{prob:<15}")

                # Show 3-4 random employers for this university
                if self.employers_data:
                    self._display_employers_for_university(row['university_name'])

        # Application strategy
        print(f"\n{'='*80}")
        print("📋 RECOMMENDED APPLICATION STRATEGY")
        print(f"{'='*80}")

        safe_count = len(results_df[results_df['bucket'] == 'Safe'])
        target_count = len(results_df[results_df['bucket'] == 'Target'])
        reach_count = len(results_df[results_df['bucket'] == 'Reach'])
        ambitious_count = len(results_df[results_df['bucket'] == 'Ambitious'])

        print(f"\nSuggested mix for 12-15 applications:")
        print(f"  • Safe schools:       3-4 universities ({safe_count} available)")
        print(f"  • Target schools:     4-6 universities ({target_count} available)")
        print(f"  • Reach schools:      3-4 universities ({reach_count} available)")
        print(f"  • Ambitious schools:  1-2 universities ({ambitious_count} available)")

        print("\n💡 Tips:")
        print("  • Apply to a balanced mix of safe, target, and ambitious schools")
        print("  • Consider factors beyond admission probability (location, cost, program fit)")
        print("  • Research each university's specific requirements and deadlines")
        print("  • Tailor your application materials to each school")

        print(f"\n{'='*80}\n")

    def run(self):
        """Main execution flow"""
        print("\n" + "="*80)
        print(" "*15 + "🎓 UNIVERSITY ADMISSION RECOMMENDER SYSTEM 🎓")
        print("="*80)
        print("\nThis tool predicts your admission chances at top US universities")
        print("based on your academic profile and recommends the best-fit schools.")
        print("="*80)

        # Load or train model
        self.load_or_train_model()

        # Get user profile
        user_profile = self.get_user_profile()

        print("\n" + "="*80)
        print("📊 YOUR PROFILE SUMMARY")
        print("="*80)
        print(f"GPA: {user_profile['gpa_normalized']:.2f}/10 ({user_profile['gpa_category']})")
        print(f"English: TOEFL {user_profile['toefl']:.0f} / IELTS {user_profile['ielts']:.1f} ({user_profile['english_proficiency']})")
        if user_profile['gre_missing'] == "False":
            print(f"GRE: V{user_profile['gre_verbal']:.0f} + Q{user_profile['gre_quant']:.0f} + AWA{user_profile['gre_awa']:.1f} = {user_profile['gre_total']:.0f} ({user_profile['gre_strength']})")
        else:
            print("GRE: Not provided")
        print(f"Experience: {user_profile['total_experience']:.0f} months ({user_profile['experience_category']})")
        print(f"Publications: {user_profile['publications']}")
        print(f"UG Major: {user_profile['undergrad_major']}")
        print(f"Target: {user_profile['course_name']} ({user_profile['target_degree']})")
        print(f"Term: {user_profile['application_term']} {user_profile['application_year']}")
        print("="*80)

        # Predict for universities
        results_df = self.predict_universities(user_profile, top_n=30)

        # Categorize into buckets
        results_df = self.categorize_into_buckets(results_df)

        # Display recommendations
        self.display_recommendations(results_df)

        # Ask if user wants to save results
        save = input("\nWould you like to save these results to a CSV file? (yes/no): ").strip().lower()
        if save in ['yes', 'y']:
            filename = f"university_recommendations_{user_profile['application_year']}.csv"
            results_df.to_csv(filename, index=False)
            print(f"✓ Results saved to {filename}")

        print("\nThank you for using the University Admission Recommender System!")
        print("Good luck with your applications! 🎓\n")


def main():
    recommender = UniversityRecommender(
        model_path='models/rf_admission_model.pkl',
        data_path='admissions_processed.csv'
    )
    recommender.run()


if __name__ == "__main__":
    main()
