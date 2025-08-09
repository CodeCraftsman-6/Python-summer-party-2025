"""
Day 1 – WhatsApp Group Messaging Analysis
-----------------------------------------
Objective:
Analyze WhatsApp groups created in October 2024 to find:
1. Maximum participants in any group.
2. Average participants across all groups.
3. Average number of messages in groups with more than 50 participants.
"""

# Import pandas library for data analysis
import pandas as pd

# -------------------------------------------------
# Step 1: Load the dataset
# -------------------------------------------------
# In a real project, this would come from a CSV, database, or API.
# For example:
# dim_groups = pd.read_csv('dim_groups.csv')

# For demo purposes, let's create a sample DataFrame:
data = {
    'group_id': [1, 2, 3, 4, 5],
    'created_date': ['2024-10-05', '2024-10-15', '2024-10-20', '2024-09-25', '2024-10-30'],
    'participant_count': [120, 45, 200, 30, 75],
    'total_messages': [1500, 800, 3000, 400, 1800]
}
dim_groups = pd.DataFrame(data)

# -------------------------------------------------
# Step 2: Convert 'created_date' column to datetime
# -------------------------------------------------
# This ensures we can filter by year and month easily.
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# -------------------------------------------------
# Step 3: Filter for groups created in October 2024
# -------------------------------------------------
october_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10)
]

# -------------------------------------------------
# Step 4: Q1 – Find the maximum number of participants
# -------------------------------------------------
max_participants = october_groups['participant_count'].max()

# -------------------------------------------------
# Step 5: Q2 – Find the average number of participants
# -------------------------------------------------
avg_participants = october_groups['participant_count'].mean()

# -------------------------------------------------
# Step 6: Q3 – Average messages in groups with > 50 participants
# -------------------------------------------------
# First filter October 2024 groups with more than 50 participants
filtered_groups = october_groups[october_groups['participant_count'] > 50]

# Then calculate average messages
avg_messages = filtered_groups['total_messages'].mean()

# -------------------------------------------------
# Step 7: Print the results
# -------------------------------------------------
print("WhatsApp Group Messaging Analysis – October 2024")
print("------------------------------------------------")
print(f"Q1) Maximum participants: {max_participants}")
print(f"Q2) Average participants: {round(avg_participants, 2)}")
print(f"Q3) Average messages in groups >50 participants: {round(avg_messages, 2)}")
