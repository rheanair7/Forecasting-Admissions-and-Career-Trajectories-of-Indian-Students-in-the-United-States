#!/bin/bash
# Launch the University Recommender Web UI

cd "$(dirname "$0")"

echo "🎓 Starting University Admission Recommender Web UI..."
echo ""
echo "The UI will open in your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

source venv/bin/activate
streamlit run app.py
