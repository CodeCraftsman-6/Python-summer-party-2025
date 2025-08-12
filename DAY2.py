import pandas as pd

# -------------------------
# Data (dataset)
# -------------------------
dim_product = pd.DataFrame({
    'product_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'product_name': [
        'Smart TV', 'Wireless Earbuds', 'Refrigerator', 'Bestselling Novel',
        'Designer Jeans', 'Blender', 'Tent', 'Smart Home Hub',
        'Phone Charger', 'Skincare Set'
    ],
    'product_category': [
        'Home Electronics', 'Electronics & Gadgets', 'Electronics Appliances',
        'Books', 'Fashion', 'Kitchen', 'Outdoor',
        'Home Electronics', 'Electronics Accessories', 'Health & Beauty'
    ]
})

fct_ad_performance = pd.DataFrame({
    'ad_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
    'clicks': [10, 15, 20, 18, 5, 12, 50, 8, 14, 22, 30, 7, 13],
    'product_id': [1, 1, 2, 2, 3, 3, 4, 5, 6, 8, 9, 11, 11],
    'impressions': [200, 300, 250, 230, 150, 180, 500, 250, 200, 220, 300, 120, 150],
    'recorded_date': pd.to_datetime([
        '2024-10-02', '2024-10-12', '2024-10-05', '2024-10-20', '2024-10-15',
        '2024-10-25', '2024-10-07', '2024-10-18', '2024-10-10', '2024-10-30',
        '2024-10-08', '2024-10-22', '2024-10-28'
    ])
})

# -------------------------
# Merge + filter October 2024
# -------------------------
merged = fct_ad_performance.merge(dim_product, on='product_id', how='left')

oct_data = merged[
    (merged['recorded_date'].dt.year == 2024) &
    (merged['recorded_date'].dt.month == 10)
].copy()

# -------------------------
# Safe CTR calculation
# -------------------------
# avoid divide-by-zero: if impressions == 0, set CTR to NaN
oct_data['CTR'] = oct_data.apply(
    lambda r: (r['clicks'] / r['impressions']) if r['impressions'] and r['impressions'] > 0 else float('nan'),
    axis=1
)

# Drop rows where product_category is missing for category-level aggregations
oct_with_category = oct_data[oct_data['product_category'].notna()].copy()

# -------------------------
# Q1: Average CTR for categories with substring 'Electronics'
# -------------------------
electronics_df = oct_with_category[
    oct_with_category['product_category'].str.contains('Electronics', case=False, na=False)
].copy()

q1_result = electronics_df.groupby('product_category', as_index=False)['CTR'].mean()
q1_result['CTR'] = q1_result['CTR'].round(6)  # rounding for readability

# -------------------------
# Q2: Categories with CTR > overall average (all categories)
# -------------------------
category_avg = oct_with_category.groupby('product_category', as_index=False)['CTR'].mean()
overall_avg = oct_with_category['CTR'].mean()

high_perf = category_avg[category_avg['CTR'] > overall_avg].copy()
high_perf['CTR'] = high_perf['CTR'].round(6)

# -------------------------
# Q3: Percentage difference vs overall average for high-performing categories
# -------------------------
high_perf['Pct_Diff'] = ((high_perf['CTR'] - overall_avg) / overall_avg) * 100
high_perf['Pct_Diff'] = high_perf['Pct_Diff'].round(2)

# -------------------------
# Print outputs neatly
# -------------------------
print("QUESTION 1 — Average CTR for categories containing 'Electronics' (Oct 2024):")
if q1_result.empty:
    print("No categories found containing 'Electronics'.")
else:
    print(q1_result.to_string(index=False))

print("\nQUESTION 2 — Overall average CTR (Oct 2024) and categories with above-average CTR:")
print(f"Overall average CTR (all categories): {overall_avg:.6f}\n")
if high_perf.empty:
    print("No categories have average CTR above the overall average.")
else:
    print(high_perf[['product_category', 'CTR']].to_string(index=False))

print("\nQUESTION 3 — Percentage difference vs overall average for the high-performing categories:")
if high_perf.empty:
    print("No categories to show.")
else:
    print(high_perf[['product_category', 'CTR', 'Pct_Diff']].to_string(index=False))

