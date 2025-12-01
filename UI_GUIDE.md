# University Admission Recommender - Web UI Guide

## 🌟 Overview

A beautiful, user-friendly web interface for the University Admission Recommender system built with **Streamlit**. No more terminal commands - just fill in a form and get instant recommendations!

---

## 🚀 Quick Start

### Launch the UI

```bash
# Method 1: Use the launch script
./run_ui.sh

# Method 2: Run directly
source venv/bin/activate
streamlit run app.py

# Method 3: From anywhere
cd /Users/raj/Sem1/Data_Mining/Project && ./run_ui.sh
```

The UI will automatically open in your browser at `http://localhost:8501`

---

## 📱 User Interface

### Main Sections

#### 1. **Sidebar - Profile Input**
Fill in your student profile with 14 fields organized into sections:

**Basic Information**
- Application Year (2024-2030)
- Application Term (Fall/Spring/Summer/Winter)

**Academic Scores**
- GPA (0-10 scale, slider)
- English Test (TOEFL or IELTS)
  - TOEFL: 0-120 slider
  - IELTS: 0-9 slider
- GRE Scores (optional)
  - Verbal: 130-170
  - Quantitative: 130-170
  - AWA: 0-6

**Professional Experience**
- Work Experience (months)
- Internship Experience (months)
- Research Publications (count)

**Academic Background**
- Undergraduate Major (text input)
- Undergraduate University (text input)
- UG Major Category (dropdown)

**Target Program**
- Target Program Name (text input)
- Program Category (dropdown)
- Degree Type (Masters/PhD/Certificate)

**Submit Button**: Click "🎯 Get Recommendations" to analyze

---

#### 2. **Main Area - Results Display**

**Profile Summary Cards**
Four metric cards showing:
- GPA with category (Very High/High/Medium/Low)
- English test score with proficiency level
- GRE score with strength level (if provided)
- Total experience with category

**Prediction Statistics**
- Total universities analyzed (30)
- Average admission probability
- Highest probability
- Lowest probability

**University Recommendations (Tabbed View)**
- 🟢 **Safe Tab** - Green cards for high-probability schools
- 🟡 **Target Tab** - Yellow cards for good-match schools
- 🔵 **Reach Tab** - Blue cards for competitive schools
- 🔴 **Ambitious Tab** - Red cards for dream schools
- 📊 **All Results Tab** - Sortable table + CSV download

Each university card shows:
- Rank within bucket
- University name
- Tier (Top 20/50/100/200/Others)
- Admission probability (large, color-coded)
- 💼 Top 3-4 recruiting companies with industry and location

**Application Strategy**
Four recommendation cards:
- Number of safe schools to apply to
- Number of target schools to apply to
- Number of reach schools to apply to
- Number of ambitious schools to apply to

**Tips Section**
Actionable advice for application strategy

---

## 🎨 Visual Design

### Color Scheme

**School Category Cards:**
- 🟢 **Safe** - Green background, green border
- 🟡 **Target** - Yellow background, yellow border
- 🔵 **Reach** - Blue background, blue border
- 🔴 **Ambitious** - Red background, red border

**Probability Colors:**
- **Green** - ≥65% (high probability)
- **Orange** - 50-65% (moderate probability)
- **Red** - <50% (low probability)

**Employer Tags:**
- Light gray background
- Inline display
- Small, readable font

### Layout
- **Wide mode** - Full browser width
- **Sidebar** - Sticky input form on left
- **Main area** - Scrollable results on right
- **Responsive** - Works on desktop and tablets

---

## 📊 Sample Workflow

### Example 1: Strong CS Applicant

**Input:**
```
GPA: 8.5/10
TOEFL: 105
GRE: V162 + Q168 (330 total)
Experience: 15 months
Publications: 0
UG Major: Computer Science
Target: MS in Computer Science
```

**Output:**
- 4 Safe schools (64-61% probability)
- 23 Target schools (61-52% probability)
- 3 Reach schools (52-50% probability)
- Each with 3-4 top recruiters

**Recommendations:**
- Apply to 3-4 safe schools
- Apply to 4-6 target schools
- Apply to 3-4 reach schools

---

### Example 2: Moderate EE Applicant

**Input:**
```
GPA: 7.5/10
IELTS: 7.0
No GRE
Experience: 6 months
Publications: 0
UG Major: Electrical Engineering
Target: MS in Electrical Engineering
```

**Expected Output:**
- 6-8 Safe schools
- 12-15 Target schools
- 5-7 Reach schools
- Mix of companies across industries

---

## 🔧 Features

### 1. **Real-Time Prediction**
- ML model loads once on startup (cached)
- Predictions in ~5 seconds
- No page refresh needed

### 2. **Smart Bucketing**
- Tier-aware categorization
- Top 50 schools have stricter thresholds
- Realistic probability ranges

### 3. **Career Insights**
- Random 3-4 companies per university
- Top employers by follower count
- Industry and location shown
- Changes each time you refresh

### 4. **Export Functionality**
- Download button in "All Results" tab
- CSV format with all data
- Filename includes year

### 5. **User-Friendly**
- No coding required
- Form validation
- Clear labels and tooltips
- Instant visual feedback

---

## 💡 Tips for Best Results

### Input Accuracy
1. **GPA Scale**: Use 10-point scale
   - 4.0 GPA ≈ 10.0
   - 3.5 GPA ≈ 8.75
   - 3.0 GPA ≈ 7.5

2. **English Scores**: Enter actual test scores
   - TOEFL: 0-120
   - IELTS: 0-9

3. **Experience**: Enter in months
   - 1 year = 12 months
   - 2 years = 24 months

4. **Major/Program**: Be specific
   - "Computer Science" not just "CS"
   - "Electrical Engineering" not "EE"

### Interpreting Results

**Probability Ranges:**
- **60%+** → Very strong candidate
- **50-60%** → Competitive candidate
- **40-50%** → Below average, but possible
- **<40%** → Very challenging

**School Categories:**
- **Safe** → >70% chance, backup options
- **Target** → 50-70% chance, realistic goals
- **Reach** → 40-50% chance, competitive but achievable
- **Ambitious** → <40% chance, dream schools

---

## 🖥️ Technical Details

### Technology Stack
- **Framework**: Streamlit 1.51+
- **ML Model**: scikit-learn Random Forest
- **Data**: 250K+ admission records
- **Visualization**: Native Streamlit components
- **Styling**: Custom CSS

### System Requirements
- **Python**: 3.7+
- **RAM**: 2GB minimum
- **Browser**: Chrome, Firefox, Safari, Edge
- **Network**: Local only (no internet required after setup)

### Performance
- **Load time**: 2-3 seconds (model loading)
- **Prediction time**: 3-5 seconds (30 universities)
- **Memory usage**: ~500MB
- **Cached**: Model and employers data cached

---

## 🐛 Troubleshooting

### UI Won't Start
```bash
# Ensure Streamlit is installed
pip install streamlit

# Check if port is available
lsof -i :8501

# Try different port
streamlit run app.py --server.port 8502
```

### Model Not Found Error
```
Error: Model not found. Please train the model first.
```

**Solution:**
```bash
# Train the model first
python3 university_recommender.py
# (or)
python3 demo_run.py
```

### Employers Data Missing
UI will show warning but continue working without employer information.

**Solution:**
Ensure `Handshake_Events/handshake_employers_data.json` exists.

### Slow Performance
- First load is slower (model loading)
- Subsequent predictions are faster (cached)
- Close other browser tabs
- Refresh the page if stuck

---

## 📚 Keyboard Shortcuts

While UI is focused:
- `Ctrl + R` - Refresh page
- `Ctrl + Click` - Open link in new tab
- `Ctrl + C` (in terminal) - Stop server

---

## 🎯 Advanced Usage

### Custom Port
```bash
streamlit run app.py --server.port 8080
```

### Network Access
```bash
# Allow access from other devices on network
streamlit run app.py --server.address 0.0.0.0
```

### Dark Theme
Streamlit auto-detects system theme. Force dark mode:
```bash
streamlit run app.py --theme.base "dark"
```

### Disable Cache (for development)
```bash
streamlit run app.py --server.runOnSave true
```

---

## 🔄 Updating Data

### Retrain Model
1. Delete old model: `rm models/rf_admission_model.pkl`
2. Update `admissions_processed.csv` with new data
3. Run: `python3 university_recommender.py`
4. Restart UI: `./run_ui.sh`

### Update Employers
1. Replace `Handshake_Events/handshake_employers_data.json`
2. Restart UI (data is cached)

---

## 📊 Data Privacy

- **All processing**: Done locally on your machine
- **No data sent**: Nothing leaves your computer
- **No tracking**: No analytics or cookies
- **No accounts**: No login or registration required

---

## 🎓 Educational Use

This UI demonstrates:
- **Streamlit development**: Building ML web apps
- **User experience design**: Form design, visual hierarchy
- **Data visualization**: Cards, tabs, metrics
- **ML deployment**: Serving predictions via web
- **Caching strategies**: Performance optimization

---

## 🚀 Deployment Options

### Local (Current Setup)
```bash
./run_ui.sh
# Access at: http://localhost:8501
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy (automatic)

### Docker
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Heroku, AWS, GCP
Requires additional configuration for production deployment.

---

## 📝 Sample Screenshots (Described)

### Welcome Screen
- Clean header with title
- Info box explaining features
- "How It Works" section
- Sidebar ready for input

### Input Form (Sidebar)
- Organized sections with headers
- Sliders for numeric values
- Radio buttons for choices
- Dropdown for categories
- Large submit button at bottom

### Results View
- Four metric cards at top
- Tabbed interface for buckets
- Color-coded university cards
- Employer tags below each university
- Statistics and strategy at bottom

### All Results Tab
- Sortable data table
- All 30 universities listed
- Download CSV button
- Clean, readable format

---

## 🆘 Support

### Getting Help
1. Check this guide first
2. Try the terminal version: `python3 demo_run.py`
3. Verify all files are present
4. Check browser console for errors

### Common Questions

**Q: Can I use this offline?**
A: Yes! All processing is local.

**Q: How accurate are predictions?**
A: Model has 83% ROC-AUC on test data.

**Q: Can I save multiple profiles?**
A: Download CSV for each profile separately.

**Q: Does it work on mobile?**
A: Optimized for desktop, but works on tablets.

**Q: Can I change the university list?**
A: Yes, edit `predict_universities()` in app.py.

---

## ✅ Quick Reference

| Action | Command |
|--------|---------|
| Start UI | `./run_ui.sh` |
| Stop UI | `Ctrl+C` in terminal |
| Access UI | `http://localhost:8501` |
| Change port | `streamlit run app.py --server.port 8080` |
| View logs | Terminal output |
| Download results | Click button in "All Results" tab |

---

## 🎊 Summary

The Web UI provides a **professional, easy-to-use interface** for university admission predictions with:

✅ **Beautiful design** - Color-coded cards, clear hierarchy
✅ **Easy input** - Form-based, no coding needed
✅ **Instant results** - ML predictions in seconds
✅ **Career insights** - Top recruiters for each university
✅ **Export ready** - Download recommendations as CSV
✅ **Zero setup** - Just run and go!

**Launch now:** `./run_ui.sh` 🚀

---

*UI Version: 1.0*
*Last Updated: December 1, 2025*
*Built with Streamlit 1.51+*
