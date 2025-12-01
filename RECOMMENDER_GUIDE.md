# University Admission Recommender System - User Guide

## Overview
This terminal-based tool predicts your admission chances at top US universities based on your academic profile and recommends universities categorized into Safe, Target, and Ambitious buckets.

## Features
- **Profile-based predictions**: Enter your GPA, test scores, experience, and background
- **Top 30 universities analyzed**: Get predictions for the most popular universities
- **Smart bucketing**: Universities categorized as Safe/Target/Ambitious based on:
  - Your admission probability
  - University tier (Top 20, Top 50, etc.)
  - Model confidence (ROC-AUC ~0.83)
- **Personalized recommendations**: Application strategy tailored to your profile
- **Export results**: Save recommendations to CSV for future reference

## Installation

### Prerequisites
```bash
# Ensure you have Python 3.7+ installed
python3 --version

# Navigate to the project directory
cd /Users/raj/Sem1/Data_Mining/Project

# Activate virtual environment
source venv/bin/activate
```

### Required Files
- `admissions_processed.csv` - Training data (must be in project root)
- `university_recommender.py` - Main script

## Usage

### Basic Usage
```bash
# Run the recommender
python3 university_recommender.py

# Or if made executable
./university_recommender.py
```

### Input Fields

The script will prompt you for the following information:

#### 1. Basic Information
- **Application Year**: e.g., 2025
- **Application Term**: Fall, Spring, Summer, or Winter

#### 2. Academic Scores
- **GPA**: Out of 10 (e.g., 8.5)
- **English Test**: Choose TOEFL or IELTS
  - TOEFL: 0-120 (e.g., 105)
  - IELTS: 0-9 (e.g., 7.5)

#### 3. GRE Scores (Optional)
- **GRE Verbal**: 0-170 (e.g., 162)
- **GRE Quantitative**: 0-170 (e.g., 168)
- **GRE AWA**: 0-6 (e.g., 4.0)

#### 4. Professional Experience
- **Work Experience**: In months (e.g., 24)
- **Internship Experience**: In months (e.g., 6)
- **Publications**: Number of research papers/publications

#### 5. Academic Background
- **Undergraduate Major**: e.g., Computer Science
- **Undergraduate University**: Your university name

#### 6. Target Program
Choose from predefined programs or enter custom:
1. Computer Science
2. Data Science / AI / Machine Learning
3. Electrical Engineering
4. Mechanical Engineering
5. Business / MBA
6. Other (custom)

## Sample Input Session

```
=================================================================================
                          STUDENT PROFILE INPUT
=================================================================================

--- Basic Information ---
Application Year (e.g., 2025): 2025
Application Term (Fall/Spring/Summer/Winter): Fall

--- Academic Scores ---
GPA (out of 10, e.g., 8.5): 8.5

--- English Proficiency (Enter one) ---
Which test? (1) TOEFL (2) IELTS: 1
TOEFL Score (out of 120, e.g., 100): 105

--- GRE Scores (Optional - press Enter to skip) ---
Do you have GRE scores? (yes/no): yes
GRE Verbal (out of 170, e.g., 160): 162
GRE Quant (out of 170, e.g., 165): 168
GRE AWA (out of 6, e.g., 4.0): 4.0

--- Professional Experience (in months) ---
Work Experience (months, e.g., 24): 12
Internship Experience (months, e.g., 6): 3

Number of Publications/Research Papers: 0

--- Academic Background ---
Undergraduate Major (e.g., Computer Science): Computer Science
Undergraduate University: IIT Bombay

--- Target Program ---
Common programs:
1. Computer Science
2. Data Science / AI / Machine Learning
3. Electrical Engineering
4. Mechanical Engineering
5. Business / MBA
6. Other

Choose program (1-6) or type custom: 1

Target Degree (Masters/PhD/Graduate Certificate): Masters
```

## Output Explanation

### Profile Summary
Shows your normalized scores and categories:
```
📊 YOUR PROFILE SUMMARY
==================================================================================
GPA: 8.50/10 (Very High)
English: TOEFL 105 / IELTS 0.0 (High)
GRE: V162 + Q168 + AWA4.0 = 330 (High)
Experience: 15 months (Medium)
Publications: 0
UG Major: Computer Science
Target: Computer Science (Masters)
Term: Fall 2025
==================================================================================
```

### University Buckets

#### 🎯 SAFE SCHOOLS (Probability ≥ 70%)
Universities where you have strong admission chances based on your profile.

#### 🎯 TARGET SCHOOLS (Probability 40-70%)
Good matches for your profile - realistic chances with competitive application.

#### 🎯 REACH/TARGET SCHOOLS (Probability 35-65% for Top 20)
Competitive schools - may need stronger profile elements.

#### 🎯 AMBITIOUS SCHOOLS (Probability < 40%)
Highly competitive reach schools - consider as stretch applications.

### Sample Output
```
==================================================================================
🎯 SAFE SCHOOLS (8 universities)
==================================================================================
These universities have high admission probability for your profile.

Rank  University                                        Tier           Probability
------------------------------------------------------------------------------------
1     University at Buffalo SUNY                        Top_100        78.5%
2     Arizona State University                          Top_100        76.2%
3     The University of Texas at Dallas                 Top_100        75.8%
...

==================================================================================
🎯 TARGET SCHOOLS (12 universities)
==================================================================================
These universities are good matches for your profile.

Rank  University                                        Tier           Probability
------------------------------------------------------------------------------------
1     Northeastern University, Boston                   Top_50         65.3%
2     University of Southern California                 Top_50         62.7%
...
```

### Application Strategy
The tool provides a recommended mix:
- **40%** Safe schools (4-6 applications)
- **40%** Target schools (5-7 applications)
- **20%** Ambitious schools (2-4 applications)

## Understanding the Model

### Model Details
- **Algorithm**: Random Forest Classifier
- **Performance**: ROC-AUC ~0.83 on test set
- **Training Data**: 250,000+ real admission records
- **Features**: 80+ academic, demographic, and experiential factors

### Key Factors Influencing Admissions
1. **GPA** (normalized)
2. **English proficiency** (TOEFL/IELTS)
3. **GRE scores** (if applicable)
4. **University tier** (Top 20, Top 50, etc.)
5. **Major alignment** (UG major vs. target program)
6. **Professional experience**
7. **Research publications**

### Probability Thresholds

The bucketing varies by university tier:

**Top 20 Universities:**
- Safe: Not typical (≥65% treated as Target)
- Target: ≥65%
- Reach/Target: 35-65%
- Ambitious: <35%

**Top 50 Universities:**
- Safe: ≥70%
- Target: 45-70%
- Ambitious: <45%

**Other Universities:**
- Safe: ≥70%
- Target: 40-70%
- Ambitious: <40%

## Tips for Best Results

### Input Accuracy
1. **Be honest** - Accurate inputs lead to accurate predictions
2. **Use 10-point GPA scale** - Convert if needed (e.g., 4.0 → 10.0 scale)
3. **Include all experience** - Work + internships in months
4. **Count publications carefully** - Only peer-reviewed or conference papers

### Interpreting Results
1. **Probabilities are estimates** - Based on historical data, not guarantees
2. **Consider holistic factors** - Model doesn't account for:
   - Statement of Purpose quality
   - Letters of recommendation strength
   - Unique extracurriculars
   - Interview performance (if applicable)
3. **Research each university** - Beyond probability:
   - Program curriculum fit
   - Faculty research areas
   - Location preferences
   - Cost and funding opportunities
   - Career placement statistics

### Application Strategy
1. **Apply to 10-15 schools** - Balance across buckets
2. **Prioritize targets** - Highest chance + good fit
3. **Include safety schools** - Ensure you have solid options
4. **Dream big** - A few ambitious schools are okay
5. **Tailor applications** - Customize for each school

## Saving Results

After viewing recommendations, you can save to CSV:
```
Would you like to save these results to a CSV file? (yes/no): yes
✓ Results saved to university_recommendations_2025.csv
```

The CSV includes:
- University name
- University tier
- Admission probability
- Bucket category

## Troubleshooting

### Model Training Takes Too Long
- First run trains the model (2-5 minutes)
- Subsequent runs load saved model (instant)
- Model saved to: `models/rf_admission_model.pkl`

### Missing Data File
```
Error: FileNotFoundError: admissions_processed.csv
```
**Solution**: Ensure `admissions_processed.csv` is in the project root directory

### Virtual Environment Issues
```bash
# Recreate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy scikit-learn
```

### Low Probabilities Across All Schools
- Review your input accuracy
- Consider strengthening your profile:
  - Retake GRE/TOEFL if below thresholds
  - Gain more relevant experience
  - Pursue research opportunities
  - Improve GPA if still in undergrad

## Advanced Usage

### Batch Mode (For Counselors/Multiple Profiles)
You can modify the script to read from a CSV file for batch processing.

### Custom University List
Edit the script to change the university list:
```python
# In predict_universities method
universities = ['MIT', 'Stanford', 'CMU', ...]  # Your custom list
```

### Adjusting Thresholds
Modify bucketing logic in `categorize_into_buckets()` method.

## Technical Details

### Model Architecture
```
Pipeline:
  1. Preprocessing
     - Numeric: Median imputation → StandardScaler
     - Categorical: Mode imputation → OneHotEncoder
  2. Random Forest Classifier
     - n_estimators: 300
     - max_depth: None
     - min_samples_split: 5
     - min_samples_leaf: 2
     - class_weight: balanced
```

### Feature Engineering
The script automatically derives:
- GPA category (Very High/High/Medium/Low)
- English proficiency level
- GRE strength category
- Experience category
- Major alignment score
- Composite academic score

## Limitations

1. **Historical data based**: Predictions based on past admissions, trends may change
2. **Incomplete factors**: Doesn't consider:
   - Essays and SOP quality
   - Recommendation letters
   - Interview performance
   - Extracurricular achievements
   - Diversity factors
3. **Model uncertainty**: ~83% accuracy means 17% predictions may be off
4. **University-specific nuances**: Each program has unique criteria
5. **Year-to-year variation**: Acceptance rates fluctuate

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Ensure all prerequisites are installed
4. Verify data file availability

## Updates and Maintenance

To retrain with new data:
1. Replace `admissions_processed.csv` with updated data
2. Delete `models/rf_admission_model.pkl`
3. Run the script - it will retrain automatically

## License

This tool is for educational and personal use. Predictions are estimates only and should not be the sole basis for application decisions.

---

**Good luck with your applications!** 🎓
