import pandas as pd
import ast
import os

def extract_title(item_str):
    try:
        items = ast.literal_eval(item_str)
        if isinstance(items, list) and len(items) > 0:
            return items[0].get('title', None)
    except (ValueError, SyntaxError):
        return None
    return None

def extract_price(item_str):
    try:
        items = ast.literal_eval(item_str)
        if isinstance(items, list) and len(items) > 0:
            return float(items[0].get('price', 0))
    except (ValueError, SyntaxError):
        return None
    return None

def merge_data():
    df_calls = pd.read_csv("data/call_data.csv")
    df_orders = pd.read_csv("data/shopify_orders.csv")

    # Merge on 'email'
    df_merged = df_calls.merge(df_orders, left_on="Email", right_on="email", how="left")

    # Extract product title and price
    if 'line_items' in df_merged.columns:
        df_merged['title'] = df_merged['line_items'].apply(extract_title)
        df_merged['Price'] = df_merged['line_items'].apply(extract_price)

        # Move 'Price' next to title
        cols = df_merged.columns.tolist()
        title_idx = cols.index('title')
        cols.insert(title_idx + 1, cols.pop(cols.index('Price')))
        df_merged = df_merged[cols]

    # Append mode: check if merged file exists
    merged_file = "data/merged_data.csv"
    if os.path.exists(merged_file):
        existing = pd.read_csv(merged_file)
        combined = pd.concat([existing, df_merged], ignore_index=True)

        # 🔁 Optional deduplication
        combined.drop_duplicates(subset=["Email", "created_at"], inplace=True, keep="last")
    else:
        combined = df_merged

    combined.to_csv(merged_file, index=False)
    print("✅ Appended and saved merged data.")

if __name__ == "__main__":
    merge_data()
