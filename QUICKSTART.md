# Quick Start Guide - University Recommender

## 🚀 Run in 3 Steps

### Step 1: Navigate to Project
```bash
cd /Users/raj/Sem1/Data_Mining/Project
```

### Step 2: Activate Environment
```bash
source venv/bin/activate
```

### Step 3: Run the Tool
```bash
python3 university_recommender.py
```

## 📝 Sample Quick Input

For a **strong Computer Science applicant**:
- Year: `2025`
- Term: `Fall`
- GPA: `8.5`
- Test: `1` (TOEFL)
- TOEFL: `105`
- GRE: `yes`
- Verbal: `162`
- Quant: `168`
- AWA: `4.0`
- Work: `12`
- Intern: `3`
- Pubs: `0`
- Major: `Computer Science`
- Uni: `IIT Bombay`
- Program: `1` (CS)
- Degree: `Masters`

## 📊 What You'll Get

1. **Profile Summary** - Your normalized scores
2. **30 Universities** - Analyzed for admission probability
3. **4 Buckets**:
   - 🟢 **Safe** (>70% probability)
   - 🟡 **Target** (40-70% probability)
   - 🟠 **Reach** (35-65% for Top schools)
   - 🔴 **Ambitious** (<40% probability)
4. **Application Strategy** - Recommended school mix
5. **Export Option** - Save to CSV

## ⏱️ First Run
- **First time**: ~3-5 minutes (trains model)
- **Subsequent runs**: ~30 seconds (loads saved model)

## 💾 Save Your Results
When prompted:
```
Would you like to save these results to a CSV file? (yes/no): yes
```
Results saved to `university_recommendations_2025.csv`

## 🆘 Need Help?
See `RECOMMENDER_GUIDE.md` for detailed documentation.

---
**Ready? Let's find your perfect university matches!** 🎓
