import json

# Read the JSON file
with open('all_profiles.json', 'r') as f:
    profiles = json.load(f)

# Dictionary to store N/A counts for each key
na_counts = {}

# Get all possible keys from the first profile
if profiles:
    for key in profiles[0].keys():
        na_counts[key] = 0

# Count N/A values for each key
for profile in profiles:
    for key, value in profile.items():
        if value == "N/A":
            na_counts[key] += 1

# Print results
print("N/A Value Counts by Field:")
print("-" * 50)
total_profiles = len(profiles)
print(f"Total Profiles: {total_profiles}\n")

# Sort by count (descending) for better readability
sorted_counts = sorted(na_counts.items(), key=lambda x: x[1], reverse=True)

for key, count in sorted_counts:
    percentage = (count / total_profiles) * 100
    print(f"{key:40s}: {count:4d} ({percentage:5.2f}%)")

print("\n" + "-" * 50)
print(f"Total N/A values across all fields: {sum(na_counts.values())}")
