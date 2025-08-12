import pandas as pd

# -------------------------
# DATA
# -------------------------
fct_guest_spending = pd.DataFrame({
    'guest_id': [1,2,3,4,1,5,6,1,1,2,2,7,3,3,1,8,9,10,1],
    'visit_date': pd.to_datetime([
        '2024-07-05','2024-07-06','2024-07-10','2024-07-12','2024-07-15',
        '2024-07-20','2024-07-25','2024-08-03','2024-08-15','2024-08-05',
        '2024-08-20','2024-08-10','2024-08-25','2024-08-27','2024-09-02',
        '2024-09-05','2024-09-15','2024-09-20','2024-09-25'
    ]),
    'amount_spent': [
        50,30,20.5,40,35,60,25,55,45,22,38,15,28,32,65,50,40,70,35
    ],
    'park_experience_type': [
        'Attraction','Dining','Retail','Entertainment','Dining','Attraction',
        'Retail','Attraction','Dining','Retail','Entertainment','Character Meet',
        'Retail','Dining','Attraction','Retail','Dining','Entertainment','Dining'
    ]
})

# -------------------------
# Q1: July 2024 average spending per type
# -------------------------
all_types = pd.DataFrame({'park_experience_type': fct_guest_spending['park_experience_type'].unique()})
july_data = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 7)
]
july_avg = july_data.groupby('park_experience_type', as_index=False)['amount_spent'].mean()
q1_result = all_types.merge(july_avg, on='park_experience_type', how='left')
q1_result['amount_spent'] = q1_result['amount_spent'].fillna(0.0).round(2)

print("\nQ1: Average spending per guest per visit for each park experience type — July 2024:")
print(q1_result)

# -------------------------
# Q2: August 2024 first vs last visit spending difference
# -------------------------
august_df = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 8)
].copy()

august_df['visit_rank'] = august_df.groupby('guest_id')['visit_date'].rank(method='first')
multi_visitors = august_df.groupby('guest_id').filter(lambda x: len(x) > 1)

first_visits = multi_visitors[multi_visitors['visit_rank'] == 1][['guest_id', 'amount_spent']]
last_visits = multi_visitors[multi_visitors['visit_rank'] == multi_visitors.groupby('guest_id')['visit_rank'].transform('max')][['guest_id', 'amount_spent']]

merged = pd.merge(first_visits, last_visits, on='guest_id', suffixes=('_first', '_last'))
merged['spending_diff'] = merged['amount_spent_last'] - merged['amount_spent_first']

print("\nQ2: Spending difference (last - first visit) for multi-visit guests — August 2024:")
print(merged[['guest_id', 'spending_diff']])

# -------------------------
# Q3: September 2024 spending segments
# -------------------------
sept_df = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 9)
]
guest_totals = sept_df.groupby("guest_id")["amount_spent"].sum().reset_index()
guest_totals = guest_totals[guest_totals["amount_spent"] > 0]

def categorize_spending(amount):
    if amount < 50:
        return "Low"
    elif amount < 100:
        return "Medium"
    else:
        return "High"

guest_totals["spending_category"] = guest_totals["amount_spent"].apply(categorize_spending)

print("\nQ3: September 2024 spending categories:")
print(guest_totals)
