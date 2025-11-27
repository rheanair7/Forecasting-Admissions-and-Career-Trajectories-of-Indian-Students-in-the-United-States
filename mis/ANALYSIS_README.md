# Comprehensive Data Analysis - USA Graduate Admissions

## 📊 Overview

This analysis covers **250,795 graduate admission records** from **519 universities** across **1,941 programs**.

## 🎯 Key Statistics

- **Total Students**: 80,130
- **International Students**: 248,035 (98.9%)
- **Domestic Students**: 2,760 (1.1%)
- **Overall Admission Rate**: 65.77%
- **Average GPA**: 7.88/10
- **Average GRE Total**: 309.96/340
- **Average TOEFL**: 99.84/120
- **Average IELTS**: 7.17/9
- **Average Work Experience**: 16.73 months
- **Students with Scholarships**: 1,667

## 📁 Project Structure

```
analysis_graphs/
├── raj/                    # 10 visualizations - Demographics & Applications
├── adwait/                 # 12 visualizations - Academic Performance & Tests
├── reha/                   # 11 visualizations - Experience & Rankings
├── cross_analysis/         # 8 visualizations - Multi-variable insights
└── summary_statistics.txt  # Detailed summary statistics
```

## 👥 Team Responsibilities

### 🔵 RAJ - Student Demographics & Application Patterns
**10 Visualizations**

1. **Student Type Distribution** - Pie chart showing International vs Domestic
2. **Top 20 Universities** - Bar chart of most applied universities
3. **Top 15 Programs** - Bar chart of most popular programs
4. **Credential Type** - Pie chart of degree types (Masters/PhD/Bachelors)
5. **Program Categories** - Bar chart of academic categories
6. **Target Degree Distribution** - Donut chart of degree levels
7. **Admission Results** - Pie chart (65.77% admission rate)
8. **Application Terms** - Bar chart (Fall/Spring/Summer)
9. **Application Trends** - Line chart showing trends over years
10. **Application Status** - Bar chart of status codes

**Key Insights**:
- Northeastern University has the most applications (13,113)
- Computer Science is the most popular program (77,428 applications)
- Fall semester is overwhelmingly preferred (90%+)
- Overall admission rate is 65.77%

---

### 🟢 ADWAIT - Academic Performance & Test Scores
**12 Visualizations**

1. **GPA Distribution** - Histogram of normalized GPAs
2. **GPA by Admission** - Box plot comparing admitted vs rejected
3. **GPA Scale Distribution** - Pie chart of grading scales
4. **Top 20 Undergrad Majors** - Bar chart
5. **UG Major Categories** - Bar chart of major buckets
6. **Major Alignment** - Pie chart (70% have aligned majors)
7. **TOEFL Distribution** - Histogram (avg 99.84)
8. **IELTS Distribution** - Histogram (avg 7.17)
9. **English Score by Admission** - Box plot comparison
10. **GRE Total Distribution** - Histogram (avg 309.96)
11. **GRE Verbal by Admission** - Violin plot
12. **GRE Quant by Admission** - Violin plot

**Key Insights**:
- Average GPA: 7.88/10 (normalized)
- Average GRE: 309.96/340
- Average TOEFL: 99.84/120
- 70% of students have undergraduate majors aligned with graduate programs
- Admitted students show higher GPA and test scores on average

---

### 🟡 REHA - Experience, Research & University Rankings
**11 Visualizations**

1. **GRE AWA Distribution** - Histogram of writing scores
2. **Work Experience Distribution** - Histogram (avg 16.73 months)
3. **Work Experience by Admission** - Box plot showing impact
4. **Relevant Work Experience** - Histogram
5. **Internship Experience** - Histogram
6. **Publications Distribution** - Bar chart (avg 0.24 papers)
7. **Scholarship Distribution** - Pie chart (0.66% receive scholarships)
8. **Scholarship Amount** - Histogram of scholarship values
9. **University Ranking by Admission** - Box plot
10. **CS Ranking vs Admission** - Scatter plot
11. **Engineering Ranking vs Admission** - Scatter plot

**Key Insights**:
- Average work experience: 16.73 months (~1.4 years)
- Average publications: 0.24 per student
- Only 1,667 students (0.66%) receive scholarships
- Higher-ranked universities show more selective admissions
- Work experience shows positive correlation with admission

---

## 🔬 Cross-Analysis - Multi-Variable Insights
**8 Advanced Visualizations**

1. **Correlation Matrix** - Heatmap showing relationships between all numeric variables
2. **GPA vs GRE Scatter** - Color-coded by admission result
3. **Admission Rates by Top Universities** - Comparative bar chart
4. **Admission by Work Experience Bins** - Shows impact of experience levels
5. **Admission by Publications** - Impact of research output
6. **Score Distributions by Student Type** - 4-panel comparison (International vs Domestic)
7. **Admission by GRE Score Bins** - Clear threshold analysis
8. **Admission Rates by Top Programs** - Program selectivity comparison

**Key Cross-Variable Insights**:
- Strong positive correlation between GRE Quant and GRE Verbal
- Work experience beyond 36 months shows diminishing returns
- Publications significantly improve admission chances
- Higher GRE scores (320+) correlate with better admission rates
- International students have slightly lower average test scores but similar admission rates

---

## 📈 Top Insights Across All Data

### Most Selective Universities (Top 20)
1. University rankings show inverse relationship with admission rates
2. Top-tier universities (rank < 50) have ~40-50% admission rates
3. Mid-tier universities (rank 50-100) have ~60-70% admission rates

### Most Competitive Programs
1. **Computer Science**: 77,428 applications (most competitive)
2. **Data Science**: 12,677 applications
3. **Business Analytics**: 8,435 applications
4. **Electrical Engineering**: 8,277 applications

### Success Factors
**Strong Predictors of Admission**:
- GPA > 8.0/10 (normalized)
- GRE Total > 315/340
- TOEFL > 100/120 or IELTS > 7.0/9
- 12-36 months of relevant work experience
- 1+ research publications
- Aligned undergraduate major (70% success rate)

**Weak Predictors**:
- Excessive work experience (>60 months)
- Student type (International vs Domestic) - minimal difference
- Application term (Fall vs Spring)

---

## 🚀 How to Run the Analysis

### Run Complete Analysis
```bash
uv run comprehensive_analysis.py
```

### Run Original Pie Chart Analysis
```bash
uv run profile_analysis_piechart.py
```

### Requirements
- Python 3.9+
- pandas
- matplotlib
- seaborn
- numpy

Install with:
```bash
uv pip install pandas matplotlib seaborn numpy
```

---

## 📊 Graph Types Used

- **Pie Charts**: Categorical distributions (Student type, Admission results, Scholarships)
- **Bar Charts**: Counts and comparisons (Universities, Programs, Publications)
- **Histograms**: Continuous distributions (GPA, GRE, TOEFL, Work experience)
- **Box Plots**: Distribution comparisons (Scores by admission result)
- **Violin Plots**: Detailed distribution shapes (GRE scores)
- **Scatter Plots**: Relationships (GPA vs GRE, Rankings vs Admission)
- **Line Charts**: Trends over time (Application years)
- **Heatmaps**: Correlation matrices
- **Donut Charts**: Hierarchical categories

---

## 📝 Files Generated

- **summary_statistics.txt**: Comprehensive text summary
- **41 PNG graphs**: High-resolution (300 DPI) visualizations
- **Organized by team member**: Easy to navigate and present

---

## 💡 Recommendations for Applicants

Based on the data analysis:

1. **Target Score Ranges**:
   - GPA: Aim for 8.0+ (normalized)
   - GRE: Target 315+ (especially 320+ for top universities)
   - TOEFL: Score 100+ / IELTS: 7.0+

2. **Build Your Profile**:
   - Gain 12-36 months of relevant work experience
   - Publish at least 1 research paper if possible
   - Choose aligned undergraduate major when possible

3. **Strategic Applications**:
   - Apply to a mix of university rankings
   - Fall semester has most openings
   - Computer Science is highly competitive (30%+ rejection rate)

4. **University Selection**:
   - Top 3 by applications: Northeastern, ASU, UT Dallas
   - Consider mid-tier universities for better admission rates
   - Research program-specific admission rates

---

## 📧 Contributors

- **Raj**: Demographics & Application Analysis
- **Adwait**: Academic Performance & Test Score Analysis
- **Reha**: Experience, Research & Ranking Analysis

---

*Analysis Date: October 27, 2025*
*Dataset: usa_decisions_cleaned_with_uuid.jsonl*
*Records: 250,795*
