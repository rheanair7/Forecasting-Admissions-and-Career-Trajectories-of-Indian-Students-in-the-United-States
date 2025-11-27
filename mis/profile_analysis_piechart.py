# /// script
# dependencies = [
#   "matplotlib>=3.10.0",
# ]
# ///

import json
import matplotlib.pyplot as plt
from collections import Counter
import math

# Load the JSONL data
profiles = []
with open('usa_decisions_cleaned_with_uuid.jsonl', 'r') as f:
    for line in f:
        profiles.append(json.loads(line.strip()))

print(f"Total profiles loaded: {len(profiles)}")
print("=" * 80)

# Get all keys from the first profile (excluding some that might not be useful)
if profiles:
    all_keys = list(profiles[0].keys())
    # Exclude these keys from analysis as they are unique identifiers or not useful for distribution
    exclude_keys = ['id', 'student_id', 'student_name', 'university_name_stripped', 'undergrad_canonical_stripped',
                    'stripped_name', 'undergrad_university', 'undergrad_canonical', 'scholarship_amount',
                    'scholarship_currency', 'gpa_scale']
    keys_to_analyze = [key for key in all_keys if key not in exclude_keys]
else:
    print("No profiles found!")
    exit()

# Analyze each key
results = {}
for key in keys_to_analyze:
    values = []
    for profile in profiles:
        value = profile.get(key, 'N/A')
        if value is not None:
            values.append(str(value))
        else:
            values.append('N/A')

    # Count occurrences
    value_counts = Counter(values)

    # Find majority (most common value)
    if value_counts:
        majority_value, majority_count = value_counts.most_common(1)[0]
        majority_percentage = (majority_count / len(values)) * 100

        results[key] = {
            'majority_value': majority_value,
            'majority_count': majority_count,
            'majority_percentage': majority_percentage,
            'value_counts': value_counts,
            'total_values': len(values)
        }

        print(f"\nKey: {key}")
        print(f"  Majority Value: {majority_value}")
        print(f"  Count: {majority_count} / {len(values)} ({majority_percentage:.2f}%)")
        print(f"  All values distribution:")
        for value, count in value_counts.most_common():
            percentage = (count / len(values)) * 100
            print(f"    {value}: {count} ({percentage:.2f}%)")

print("\n" + "=" * 80)
print("Creating pie charts for each key...")

# Create pie charts
num_keys = len(keys_to_analyze)
cols = 3  # 3 columns
rows = math.ceil(num_keys / cols)

fig, axes = plt.subplots(rows, cols, figsize=(18, 5 * rows))
fig.suptitle('Distribution of Profile Attributes', fontsize=16, fontweight='bold')

# Flatten axes array for easier indexing
if num_keys > 1:
    axes_flat = axes.flatten() if rows > 1 else [axes] if cols == 1 else axes
else:
    axes_flat = [axes]

for idx, key in enumerate(keys_to_analyze):
    ax = axes_flat[idx]

    value_counts = results[key]['value_counts']

    # Prepare data for pie chart
    # Show top 10 values, group others as "Other"
    top_items = value_counts.most_common(10)

    if len(value_counts) > 10:
        other_count = sum(count for value, count in value_counts.most_common()[10:])
        labels = [str(val)[:30] for val, _ in top_items] + ['Other']
        sizes = [count for _, count in top_items] + [other_count]
    else:
        labels = [str(val)[:30] for val, _ in top_items]
        sizes = [count for _, count in top_items]

    # Create pie chart
    colors = plt.cm.Set3(range(len(labels)))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors,
                                        textprops={'fontsize': 8})

    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(7)

    # Make labels smaller if there are many
    for text in texts:
        text.set_fontsize(7)

    ax.set_title(f'{key}\n(Majority: {results[key]["majority_value"][:30]})',
                 fontsize=10, fontweight='bold', pad=10)

# Hide any unused subplots
for idx in range(num_keys, len(axes_flat)):
    axes_flat[idx].axis('off')

plt.tight_layout()
plt.savefig('profile_analysis_piecharts.png', dpi=300, bbox_inches='tight')
print(f"\nPie charts saved as 'profile_analysis_piecharts.png'")

# Create individual pie charts for each key (optional - more detailed view)
print("\nCreating individual pie charts for each key...")
import os
os.makedirs('individual_piecharts', exist_ok=True)

for key in keys_to_analyze:
    fig, ax = plt.subplots(figsize=(10, 8))

    value_counts = results[key]['value_counts']

    # Prepare data for pie chart
    # Show top 15 values, group others as "Other"
    top_items = value_counts.most_common(15)

    if len(value_counts) > 15:
        other_count = sum(count for value, count in value_counts.most_common()[15:])
        labels = [str(val) for val, _ in top_items] + ['Other']
        sizes = [count for _, count in top_items] + [other_count]
    else:
        labels = [str(val) for val, _ in top_items]
        sizes = [count for _, count in top_items]

    # Create pie chart
    colors = plt.cm.Set3(range(len(labels)))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors,
                                        textprops={'fontsize': 9})

    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')

    ax.set_title(f'{key}\nMajority: {results[key]["majority_value"]} '
                 f'({results[key]["majority_percentage"]:.1f}%)',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    # Save with sanitized filename
    filename = key.replace('/', '_').replace(' ', '_').lower()
    plt.savefig(f'individual_piecharts/{filename}_piechart.png', dpi=300, bbox_inches='tight')
    plt.close()

print(f"Individual pie charts saved in 'individual_piecharts/' folder")
print("\nAnalysis complete!")
