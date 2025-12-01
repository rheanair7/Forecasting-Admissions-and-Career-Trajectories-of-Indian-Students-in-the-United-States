#!/bin/bash
# Test script for University Recommender
# Provides automated sample inputs for testing

cd "$(dirname "$0")"

echo "Testing University Recommender with sample profile..."
echo ""

# Sample input for a strong CS applicant
python3 university_recommender.py << EOF
2025
Fall
8.5
1
105
yes
162
168
4.0
12
3
0
Computer Science
Indian Institute of Technology
1
Masters
EOF
