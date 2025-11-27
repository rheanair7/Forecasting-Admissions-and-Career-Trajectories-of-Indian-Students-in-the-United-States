# /// script
# dependencies = [
#   "matplotlib>=3.10.0",
#   "seaborn>=0.13.0",
#   "pandas>=2.2.0",
#   "numpy>=1.26.0",
# ]
# ///

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("Loading data...")
# Load the JSONL data
data = []
with open('usa_decisions_cleaned_with_uuid.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line.strip()))

df = pd.DataFrame(data)
print(f"Total records loaded: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Create output directories
Path("analysis_graphs").mkdir(exist_ok=True)
Path("analysis_graphs/raj").mkdir(exist_ok=True)
Path("analysis_graphs/adwait").mkdir(exist_ok=True)
Path("analysis_graphs/reha").mkdir(exist_ok=True)
Path("analysis_graphs/cross_analysis").mkdir(exist_ok=True)

print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# ============================================================================
# RAJ'S ANALYSIS - Student Demographics & Application Details
# ============================================================================
print("\n📊 RAJ's Analysis - Student Demographics & Applications")

# 1. Student Type Distribution
plt.figure(figsize=(10, 6))
student_type_counts = df['student_type'].value_counts()
colors = ['#3498db', '#e74c3c']
plt.pie(student_type_counts.values, labels=student_type_counts.index, autopct='%1.1f%%',
        colors=colors, startangle=90)
plt.title('Student Type Distribution\n(International vs Domestic)', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/raj/1_student_type_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Student type pie chart")

# 2. Top 20 Universities
plt.figure(figsize=(14, 10))
top_unis = df['university_name'].value_counts().head(20)
plt.barh(range(len(top_unis)), top_unis.values, color='steelblue')
plt.yticks(range(len(top_unis)), top_unis.index, fontsize=9)
plt.xlabel('Number of Applications', fontsize=12)
plt.title('Top 20 Most Applied Universities', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
for i, v in enumerate(top_unis.values):
    plt.text(v + 50, i, str(v), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('analysis_graphs/raj/2_top_universities_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Top 20 universities bar chart")

# 3. Top 15 Programs
plt.figure(figsize=(14, 9))
top_programs = df['course_name'].value_counts().head(15)
plt.barh(range(len(top_programs)), top_programs.values, color='mediumseagreen')
plt.yticks(range(len(top_programs)), top_programs.index, fontsize=10)
plt.xlabel('Number of Applications', fontsize=12)
plt.title('Top 15 Most Applied Programs', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
for i, v in enumerate(top_programs.values):
    plt.text(v + 50, i, str(v), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('analysis_graphs/raj/3_top_programs_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Top 15 programs bar chart")

# 4. Credential Type Distribution
plt.figure(figsize=(10, 6))
credential_counts = df['credential'].value_counts()
colors_cred = sns.color_palette("Set2", len(credential_counts))
plt.pie(credential_counts.values, labels=credential_counts.index, autopct='%1.1f%%',
        colors=colors_cred, startangle=45)
plt.title('Credential Type Distribution', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/raj/4_credential_type_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Credential type pie chart")

# 5. Program Categories
plt.figure(figsize=(14, 10))
top_categories = df['categorical_course_name'].value_counts().head(15)
plt.barh(range(len(top_categories)), top_categories.values, color='coral')
plt.yticks(range(len(top_categories)), top_categories.index, fontsize=9)
plt.xlabel('Number of Applications', fontsize=12)
plt.title('Top 15 Program Categories', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('analysis_graphs/raj/5_program_categories_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Program categories bar chart")

# 6. Target Degree Distribution
plt.figure(figsize=(10, 6))
target_degree_counts = df['target_degree'].value_counts()
colors_degree = ['#FF6B6B', '#4ECDC4', '#45B7D1']
wedges, texts, autotexts = plt.pie(target_degree_counts.values, labels=target_degree_counts.index,
                                     autopct='%1.1f%%', colors=colors_degree, startangle=90,
                                     wedgeprops=dict(width=0.5))
plt.title('Target Degree Distribution', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/raj/6_target_degree_donut.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Target degree donut chart")

# 7. Admission Result
plt.figure(figsize=(10, 6))
admission_counts = df['admission_result'].value_counts()
labels = ['Rejected', 'Admitted']
colors_admission = ['#e74c3c', '#2ecc71']
plt.pie(admission_counts.values, labels=labels, autopct='%1.1f%%',
        colors=colors_admission, startangle=90)
plt.title('Admission Results Distribution', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/raj/7_admission_result_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Admission result pie chart")

# 8. Application Term (excluding 'nd')
plt.figure(figsize=(10, 6))
term_data = df[df['application_term'] != 'nd']  # Filter out 'nd' values
term_counts = term_data['application_term'].value_counts()
plt.bar(term_counts.index, term_counts.values, color=['#3498db', '#e67e22', '#9b59b6'])
plt.xlabel('Application Term', fontsize=12)
plt.ylabel('Number of Applications', fontsize=12)
plt.title('Application Term Distribution', fontsize=14, fontweight='bold')
for i, v in enumerate(term_counts.values):
    plt.text(i, v + 1000, str(v), ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('analysis_graphs/raj/8_application_term_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Application term bar chart (excluding 'nd')")

# 9. Application Year Trend
plt.figure(figsize=(12, 6))
year_counts = df['application_year'].value_counts().sort_index()
plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=2, markersize=8, color='darkblue')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Applications', fontsize=12)
plt.title('Application Trend Over Years', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
for x, y in zip(year_counts.index, year_counts.values):
    plt.text(x, y + 500, str(y), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('analysis_graphs/raj/9_application_trend_line.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Application trend line chart")

# 10. Application Status
plt.figure(figsize=(10, 6))
status_counts = df['application_status'].value_counts().sort_index()
plt.bar(status_counts.index, status_counts.values, color='teal')
plt.xlabel('Application Status Code', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Application Status Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/raj/10_application_status_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Application status bar chart")

# ============================================================================
# ADWAIT'S ANALYSIS - Academic Performance & Test Scores
# ============================================================================
print("\n📊 ADWAIT's Analysis - Academic Performance & Test Scores")

# 1. GPA Distribution
plt.figure(figsize=(12, 6))
gpa_data = df['gpa_normalized'].dropna()
plt.hist(gpa_data, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.xlabel('Normalized GPA', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('GPA Distribution (Normalized)', fontsize=14, fontweight='bold')
plt.axvline(gpa_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {gpa_data.mean():.2f}')
plt.legend()
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/1_gpa_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GPA histogram")

# 2. GPA by Admission Result (Box Plot)
plt.figure(figsize=(10, 6))
df_gpa = df[df['gpa_normalized'].notna()].copy()
df_gpa['admission_result_label'] = df_gpa['admission_result'].map({0: 'Rejected', 1: 'Admitted'})
sns.boxplot(data=df_gpa, x='admission_result_label', y='gpa_normalized', palette=['#e74c3c', '#2ecc71'])
plt.xlabel('Admission Result', fontsize=12)
plt.ylabel('Normalized GPA', fontsize=12)
plt.title('GPA Distribution by Admission Result', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/2_gpa_by_admission_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GPA by admission box plot")

# 3. GPA Scale Distribution
plt.figure(figsize=(10, 6))
scale_counts = df['gpa_scale'].value_counts()
plt.pie(scale_counts.values, labels=scale_counts.index, autopct='%1.1f%%', startangle=45)
plt.title('GPA Scale Distribution', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/adwait/3_gpa_scale_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GPA scale pie chart")

# 4. Top 20 Undergraduate Majors
plt.figure(figsize=(14, 10))
top_majors = df['undergrad_major'].value_counts().head(20)
plt.barh(range(len(top_majors)), top_majors.values, color='lightcoral')
plt.yticks(range(len(top_majors)), top_majors.index, fontsize=9)
plt.xlabel('Number of Students', fontsize=12)
plt.title('Top 20 Undergraduate Majors', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/4_undergrad_majors_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Undergrad majors bar chart")

# 5. UG Major Bucket Distribution
plt.figure(figsize=(14, 8))
major_buckets = df['ug_major_bucket'].value_counts().head(10)
plt.bar(range(len(major_buckets)), major_buckets.values, color='mediumorchid')
plt.xticks(range(len(major_buckets)), major_buckets.index, rotation=45, ha='right', fontsize=9)
plt.ylabel('Number of Students', fontsize=12)
plt.title('Top 10 Undergraduate Major Categories', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/5_ug_major_bucket_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ UG major bucket bar chart")

# 6. Major Alignment
plt.figure(figsize=(10, 6))
alignment_counts = df['major_alignment'].value_counts()
labels = ['Aligned', 'Not Aligned']
colors_align = ['#27ae60', '#e67e22']
plt.pie(alignment_counts.values, labels=labels, autopct='%1.1f%%',
        colors=colors_align, startangle=90)
plt.title('Major Alignment Distribution\n(Undergrad to Grad)', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/adwait/6_major_alignment_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Major alignment pie chart")

# 7. TOEFL Score Distribution
plt.figure(figsize=(12, 6))
toefl_data = df['toefl'].dropna()
plt.hist(toefl_data, bins=40, color='lightgreen', edgecolor='black', alpha=0.7)
plt.xlabel('TOEFL Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('TOEFL Score Distribution', fontsize=14, fontweight='bold')
plt.axvline(toefl_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {toefl_data.mean():.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/7_toefl_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ TOEFL histogram")

# 8. IELTS Score Distribution
plt.figure(figsize=(12, 6))
ielts_data = df['ielts'].dropna()
plt.hist(ielts_data, bins=30, color='lightsalmon', edgecolor='black', alpha=0.7)
plt.xlabel('IELTS Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('IELTS Score Distribution', fontsize=14, fontweight='bold')
plt.axvline(ielts_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {ielts_data.mean():.2f}')
plt.legend()
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/8_ielts_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ IELTS histogram")

# 9. English Score by Admission Result
plt.figure(figsize=(10, 6))
df_eng = df[df['english_test_normalized'].notna()].copy()
df_eng['admission_result_label'] = df_eng['admission_result'].map({0: 'Rejected', 1: 'Admitted'})
sns.boxplot(data=df_eng, x='admission_result_label', y='english_test_normalized', palette=['#e74c3c', '#2ecc71'])
plt.xlabel('Admission Result', fontsize=12)
plt.ylabel('Normalized English Score', fontsize=12)
plt.title('English Test Score by Admission Result', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/9_english_score_by_admission_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ English score by admission box plot")

# 10. GRE Total Score Distribution
plt.figure(figsize=(12, 6))
gre_data = df['gre_total'].dropna()
plt.hist(gre_data, bins=40, color='mediumpurple', edgecolor='black', alpha=0.7)
plt.xlabel('GRE Total Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('GRE Total Score Distribution', fontsize=14, fontweight='bold')
plt.axvline(gre_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {gre_data.mean():.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/10_gre_total_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GRE total histogram")

# 11. GRE Verbal vs Admission
plt.figure(figsize=(10, 6))
df_gre_v = df[df['gre_verbal'].notna()].copy()
df_gre_v['admission_result_label'] = df_gre_v['admission_result'].map({0: 'Rejected', 1: 'Admitted'})
sns.violinplot(data=df_gre_v, x='admission_result_label', y='gre_verbal', palette=['#e74c3c', '#2ecc71'])
plt.xlabel('Admission Result', fontsize=12)
plt.ylabel('GRE Verbal Score', fontsize=12)
plt.title('GRE Verbal Score by Admission Result', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/11_gre_verbal_by_admission_violin.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GRE verbal by admission violin plot")

# 12. GRE Quant vs Admission
plt.figure(figsize=(10, 6))
df_gre_q = df[df['gre_quant'].notna()].copy()
df_gre_q['admission_result_label'] = df_gre_q['admission_result'].map({0: 'Rejected', 1: 'Admitted'})
sns.violinplot(data=df_gre_q, x='admission_result_label', y='gre_quant', palette=['#e74c3c', '#2ecc71'])
plt.xlabel('Admission Result', fontsize=12)
plt.ylabel('GRE Quantitative Score', fontsize=12)
plt.title('GRE Quantitative Score by Admission Result', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/adwait/12_gre_quant_by_admission_violin.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GRE quant by admission violin plot")

# ============================================================================
# REHA'S ANALYSIS - Experience, Research & Rankings
# ============================================================================
print("\n📊 REHA's Analysis - Experience, Research & Rankings")

# 1. GRE AWA Distribution
plt.figure(figsize=(12, 6))
awa_data = df['gre_awa'].dropna()
plt.hist(awa_data, bins=20, color='gold', edgecolor='black', alpha=0.7)
plt.xlabel('GRE AWA Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('GRE Analytical Writing Score Distribution', fontsize=14, fontweight='bold')
plt.axvline(awa_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {awa_data.mean():.2f}')
plt.legend()
plt.tight_layout()
plt.savefig('analysis_graphs/reha/1_gre_awa_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GRE AWA histogram")

# 2. Work Experience Distribution
plt.figure(figsize=(12, 6))
work_exp_data = df['work_experience'].dropna()
work_exp_data = work_exp_data[work_exp_data <= 120]  # Filter outliers for better visualization
plt.hist(work_exp_data, bins=50, color='teal', edgecolor='black', alpha=0.7)
plt.xlabel('Work Experience (months)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Work Experience Distribution', fontsize=14, fontweight='bold')
plt.axvline(work_exp_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {work_exp_data.mean():.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('analysis_graphs/reha/2_work_experience_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Work experience histogram")

# 3. Work Experience by Admission
plt.figure(figsize=(10, 6))
df_work = df[df['work_experience'].notna()].copy()
df_work = df_work[df_work['work_experience'] <= 120]
df_work['admission_result_label'] = df_work['admission_result'].map({0: 'Rejected', 1: 'Admitted'})
sns.boxplot(data=df_work, x='admission_result_label', y='work_experience', palette=['#e74c3c', '#2ecc71'])
plt.xlabel('Admission Result', fontsize=12)
plt.ylabel('Work Experience (months)', fontsize=12)
plt.title('Work Experience Impact on Admission', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/reha/3_work_exp_by_admission_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Work experience by admission box plot")

# 4. Relevant Work Experience
plt.figure(figsize=(12, 6))
rel_work_data = df['relevant_work_experience'].dropna()
rel_work_data = rel_work_data[rel_work_data <= 120]
plt.hist(rel_work_data, bins=50, color='darkseagreen', edgecolor='black', alpha=0.7)
plt.xlabel('Relevant Work Experience (months)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Relevant Work Experience Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/reha/4_relevant_work_exp_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Relevant work experience histogram")

# 5. Internship Experience
plt.figure(figsize=(12, 6))
intern_data = df['internship_experience'].dropna()
intern_data = intern_data[intern_data <= 60]
plt.hist(intern_data, bins=40, color='plum', edgecolor='black', alpha=0.7)
plt.xlabel('Internship Experience (months)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Internship Experience Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/reha/5_internship_exp_histogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Internship experience histogram")

# 6. Publications Distribution
plt.figure(figsize=(12, 6))
pub_data = df['publications'].value_counts().sort_index().head(15)
plt.bar(pub_data.index, pub_data.values, color='indianred')
plt.xlabel('Number of Publications', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.title('Research Publications Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis_graphs/reha/6_publications_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Publications bar chart")

# 7. Scholarship Distribution
plt.figure(figsize=(10, 6))
scholarship_counts = df['has_scholarship'].value_counts()
labels = ['No Scholarship', 'Has Scholarship']
colors_sch = ['#e74c3c', '#2ecc71']
plt.pie(scholarship_counts.values, labels=labels, autopct='%1.1f%%',
        colors=colors_sch, startangle=90)
plt.title('Scholarship Distribution', fontsize=14, fontweight='bold')
plt.savefig('analysis_graphs/reha/7_scholarship_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Scholarship pie chart")

# 8. Scholarship Amount Distribution
plt.figure(figsize=(12, 6))
scholarship_amt = df[df['scholarship_amount'].notna() & (df['scholarship_amount'] > 0)]['scholarship_amount']
if len(scholarship_amt) > 0:
    plt.hist(scholarship_amt, bins=50, color='goldenrod', edgecolor='black', alpha=0.7)
    plt.xlabel('Scholarship Amount (USD)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Scholarship Amount Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('analysis_graphs/reha/8_scholarship_amount_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Scholarship amount histogram")
else:
    print("  ⚠ No scholarship amount data available")

# 9. General Rank Distribution
plt.figure(figsize=(10, 6))
df_rank = df[df['gen_rank'].notna()].copy()
df_rank['admission_result_label'] = df_rank['admission_result'].map({0: 'Rejected', 1: 'Admitted'})
sns.boxplot(data=df_rank, x='admission_result_label', y='gen_rank', palette=['#e74c3c', '#2ecc71'])
plt.xlabel('Admission Result', fontsize=12)
plt.ylabel('University General Ranking', fontsize=12)
plt.title('University Ranking by Admission Result', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()  # Lower rank number = better
plt.tight_layout()
plt.savefig('analysis_graphs/reha/9_gen_rank_by_admission_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ General rank by admission box plot")

# 10. CS Rank vs Admission
plt.figure(figsize=(10, 6))
df_cs = df[(df['cs_rank'].notna()) & (df['cs_rank'] <= 200)].copy()
if len(df_cs) > 100:
    colors_scatter = df_cs['admission_result'].map({0: '#e74c3c', 1: '#2ecc71'})
    plt.scatter(df_cs['cs_rank'], df_cs['admission_result'], alpha=0.5, c=colors_scatter, s=20)
    plt.xlabel('CS Program Ranking', fontsize=12)
    plt.ylabel('Admission Result (0=Reject, 1=Admit)', fontsize=12)
    plt.title('CS Ranking vs Admission Result', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('analysis_graphs/reha/10_cs_rank_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ CS rank scatter plot")
else:
    print("  ⚠ Insufficient CS rank data")

# 11. Engineering Rank vs Admission
plt.figure(figsize=(10, 6))
df_eng_rank = df[(df['eng_rank'].notna()) & (df['eng_rank'] <= 200)].copy()
if len(df_eng_rank) > 100:
    colors_scatter = df_eng_rank['admission_result'].map({0: '#e74c3c', 1: '#2ecc71'})
    plt.scatter(df_eng_rank['eng_rank'], df_eng_rank['admission_result'], alpha=0.5, c=colors_scatter, s=20)
    plt.xlabel('Engineering Program Ranking', fontsize=12)
    plt.ylabel('Admission Result (0=Reject, 1=Admit)', fontsize=12)
    plt.title('Engineering Ranking vs Admission Result', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('analysis_graphs/reha/11_eng_rank_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Engineering rank scatter plot")
else:
    print("  ⚠ Insufficient Engineering rank data")

# ============================================================================
# CROSS-ANALYSIS - Multi-variable insights
# ============================================================================
print("\n📊 CROSS-ANALYSIS - Multi-variable Insights")

# 1. Correlation Matrix
plt.figure(figsize=(14, 12))
numeric_cols = ['gpa_normalized', 'english_test_normalized', 'gre_total', 'gre_verbal',
                'gre_quant', 'gre_awa', 'work_experience', 'relevant_work_experience',
                'internship_experience', 'publications', 'gen_rank', 'admission_result']
corr_data = df[numeric_cols].corr()
sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Key Variables', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/1_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Correlation matrix")

# 2. GPA vs GRE by Admission Result
plt.figure(figsize=(12, 8))
df_scatter = df[(df['gpa_normalized'].notna()) & (df['gre_total'].notna())].copy()
admitted = df_scatter[df_scatter['admission_result'] == 1]
rejected = df_scatter[df_scatter['admission_result'] == 0]
plt.scatter(rejected['gpa_normalized'], rejected['gre_total'], alpha=0.3, c='red',
            label='Rejected', s=30)
plt.scatter(admitted['gpa_normalized'], admitted['gre_total'], alpha=0.3, c='green',
            label='Admitted', s=30)
plt.xlabel('Normalized GPA', fontsize=12)
plt.ylabel('GRE Total Score', fontsize=12)
plt.title('GPA vs GRE by Admission Result', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/2_gpa_vs_gre_scatter.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ GPA vs GRE scatter plot")

# 3. Admission Rate by Top Universities
plt.figure(figsize=(14, 10))
top_unis_list = df['university_name'].value_counts().head(20).index
df_top_unis = df[df['university_name'].isin(top_unis_list)]
admission_rates = df_top_unis.groupby('university_name')['admission_result'].agg(['mean', 'count'])
admission_rates = admission_rates[admission_rates['count'] >= 100].sort_values('mean', ascending=False)
plt.barh(range(len(admission_rates)), admission_rates['mean'] * 100, color='steelblue')
plt.yticks(range(len(admission_rates)), admission_rates.index, fontsize=9)
plt.xlabel('Admission Rate (%)', fontsize=12)
plt.title('Admission Rates by Top Universities', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
for i, v in enumerate(admission_rates['mean'] * 100):
    plt.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/3_admission_rates_by_university.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Admission rates by university")

# 4. Admission Rate by Work Experience Bins
plt.figure(figsize=(12, 7))
df_work_bins = df[df['work_experience'].notna()].copy()
df_work_bins['work_exp_bin'] = pd.cut(df_work_bins['work_experience'],
                                        bins=[0, 12, 24, 36, 60, 200],
                                        labels=['0-12 months', '12-24 months', '24-36 months',
                                               '36-60 months', '60+ months'])
admission_by_exp = df_work_bins.groupby('work_exp_bin')['admission_result'].agg(['mean', 'count'])
admission_by_exp = admission_by_exp[admission_by_exp['count'] >= 100]
plt.bar(range(len(admission_by_exp)), admission_by_exp['mean'] * 100, color='darkorange')
plt.xticks(range(len(admission_by_exp)), admission_by_exp.index, rotation=45, ha='right')
plt.ylabel('Admission Rate (%)', fontsize=12)
plt.xlabel('Work Experience Range', fontsize=12)
plt.title('Admission Rate by Work Experience', fontsize=14, fontweight='bold')
for i, v in enumerate(admission_by_exp['mean'] * 100):
    plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/4_admission_by_work_exp.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Admission rate by work experience")

# 5. Publications Impact
plt.figure(figsize=(12, 7))
df_pub = df[df['publications'] <= 10].copy()
pub_impact = df_pub.groupby('publications')['admission_result'].agg(['mean', 'count'])
pub_impact = pub_impact[pub_impact['count'] >= 100]
plt.bar(pub_impact.index, pub_impact['mean'] * 100, color='mediumseagreen')
plt.xlabel('Number of Publications', fontsize=12)
plt.ylabel('Admission Rate (%)', fontsize=12)
plt.title('Admission Rate by Number of Publications', fontsize=14, fontweight='bold')
for i, (idx, v) in enumerate(zip(pub_impact.index, pub_impact['mean'] * 100)):
    plt.text(idx, v + 0.5, f'{v:.1f}%', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/5_admission_by_publications.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Admission rate by publications")

# 6. Score Distribution by Student Type
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Test Score Distributions: International vs Domestic Students',
             fontsize=16, fontweight='bold')

# GPA
df_gpa_type = df[df['gpa_normalized'].notna()]
for student_type in ['International', 'Domestic']:
    data = df_gpa_type[df_gpa_type['student_type'] == student_type]['gpa_normalized']
    axes[0, 0].hist(data, bins=30, alpha=0.6, label=student_type)
axes[0, 0].set_xlabel('Normalized GPA')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('GPA Distribution')
axes[0, 0].legend()

# GRE
df_gre_type = df[df['gre_total'].notna()]
for student_type in ['International', 'Domestic']:
    data = df_gre_type[df_gre_type['student_type'] == student_type]['gre_total']
    axes[0, 1].hist(data, bins=30, alpha=0.6, label=student_type)
axes[0, 1].set_xlabel('GRE Total Score')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('GRE Distribution')
axes[0, 1].legend()

# TOEFL
df_toefl_type = df[df['toefl'].notna()]
for student_type in ['International', 'Domestic']:
    data = df_toefl_type[df_toefl_type['student_type'] == student_type]['toefl']
    if len(data) > 10:
        axes[1, 0].hist(data, bins=30, alpha=0.6, label=student_type)
axes[1, 0].set_xlabel('TOEFL Score')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('TOEFL Distribution')
axes[1, 0].legend()

# Work Experience
df_work_type = df[df['work_experience'].notna() & (df['work_experience'] <= 120)]
for student_type in ['International', 'Domestic']:
    data = df_work_type[df_work_type['student_type'] == student_type]['work_experience']
    axes[1, 1].hist(data, bins=30, alpha=0.6, label=student_type)
axes[1, 1].set_xlabel('Work Experience (months)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Work Experience Distribution')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/6_scores_by_student_type.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Score distributions by student type")

# 7. Admission Rate by GRE Score Bins
plt.figure(figsize=(12, 7))
df_gre_bins = df[df['gre_total'].notna()].copy()
df_gre_bins['gre_bin'] = pd.cut(df_gre_bins['gre_total'],
                                 bins=[0, 300, 310, 320, 330, 340],
                                 labels=['<300', '300-310', '310-320', '320-330', '330-340'])
admission_by_gre = df_gre_bins.groupby('gre_bin')['admission_result'].agg(['mean', 'count'])
admission_by_gre = admission_by_gre[admission_by_gre['count'] >= 100]
plt.bar(range(len(admission_by_gre)), admission_by_gre['mean'] * 100, color='mediumpurple')
plt.xticks(range(len(admission_by_gre)), admission_by_gre.index)
plt.ylabel('Admission Rate (%)', fontsize=12)
plt.xlabel('GRE Score Range', fontsize=12)
plt.title('Admission Rate by GRE Score Range', fontsize=14, fontweight='bold')
for i, v in enumerate(admission_by_gre['mean'] * 100):
    plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/7_admission_by_gre_bins.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Admission rate by GRE bins")

# 8. Top Programs Admission Rates
plt.figure(figsize=(14, 10))
top_programs_list = df['course_name'].value_counts().head(20).index
df_top_programs = df[df['course_name'].isin(top_programs_list)]
program_admission = df_top_programs.groupby('course_name')['admission_result'].agg(['mean', 'count'])
program_admission = program_admission[program_admission['count'] >= 100].sort_values('mean', ascending=False)
plt.barh(range(len(program_admission)), program_admission['mean'] * 100, color='coral')
plt.yticks(range(len(program_admission)), program_admission.index, fontsize=9)
plt.xlabel('Admission Rate (%)', fontsize=12)
plt.title('Admission Rates by Top Programs', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
for i, v in enumerate(program_admission['mean'] * 100):
    plt.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('analysis_graphs/cross_analysis/8_admission_by_program.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Admission rates by program")

# ============================================================================
# GENERATE SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*80)
print("GENERATING SUMMARY STATISTICS")
print("="*80)

summary_stats = {
    "Total Records": len(df),
    "Total Students": df['student_id'].nunique(),
    "International Students": (df['student_type'] == 'International').sum(),
    "Domestic Students": (df['student_type'] == 'Domestic').sum(),
    "Total Admitted": (df['admission_result'] == 1).sum(),
    "Total Rejected": (df['admission_result'] == 0).sum(),
    "Overall Admission Rate (%)": (df['admission_result'].mean() * 100),
    "Avg GPA (Normalized)": df['gpa_normalized'].mean(),
    "Avg GRE Total": df['gre_total'].mean(),
    "Avg TOEFL": df['toefl'].mean(),
    "Avg IELTS": df['ielts'].mean(),
    "Avg Work Experience (months)": df['work_experience'].mean(),
    "Avg Publications": df['publications'].mean(),
    "Students with Scholarships": (df['has_scholarship'] == True).sum(),
    "Unique Universities": df['university_name'].nunique(),
    "Unique Programs": df['course_name'].nunique(),
}

# Save summary statistics
with open('analysis_graphs/summary_statistics.txt', 'w') as f:
    f.write("="*80 + "\n")
    f.write("SUMMARY STATISTICS\n")
    f.write("="*80 + "\n\n")
    for key, value in summary_stats.items():
        if isinstance(value, float):
            f.write(f"{key}: {value:.2f}\n")
        else:
            f.write(f"{key}: {value}\n")

    f.write("\n" + "="*80 + "\n")
    f.write("TOP 10 UNIVERSITIES BY APPLICATION COUNT\n")
    f.write("="*80 + "\n")
    top_unis = df['university_name'].value_counts().head(10)
    for i, (uni, count) in enumerate(top_unis.items(), 1):
        f.write(f"{i}. {uni}: {count}\n")

    f.write("\n" + "="*80 + "\n")
    f.write("TOP 10 PROGRAMS BY APPLICATION COUNT\n")
    f.write("="*80 + "\n")
    top_programs = df['course_name'].value_counts().head(10)
    for i, (prog, count) in enumerate(top_programs.items(), 1):
        f.write(f"{i}. {prog}: {count}\n")

print("\n✅ Summary statistics saved to: analysis_graphs/summary_statistics.txt")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nTotal graphs generated:")
print(f"  - Raj's folder: 10 graphs")
print(f"  - Adwait's folder: 12 graphs")
print(f"  - Reha's folder: 11 graphs")
print(f"  - Cross-analysis folder: 8 graphs")
print(f"\nAll visualizations saved in: analysis_graphs/")
print("="*80)
