import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. SETUP & ERROR HANDLING ---
def load_data(filename):
    try:
        data = pd.read_csv(filename)
        print(f"✅ Step 1: {filename} loaded successfully.")
        return data
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        exit()

# --- 2. DATA CLEANING PIPELINE ---
def clean_data(data):
    # Remove duplicates
    initial_count = len(data)
    data = data.drop_duplicates()
    
    # Handle missing values
    data = data.fillna({
        'Quantity': 0,
        'Price': data['Price'].mean(),
        'Total_Sales': 0
    })
    
    print(f"✅ Step 2: Cleaning complete. ({initial_count - len(data)} duplicates removed)")
    return data

# --- 3. ANALYSIS & VISUALIZATION ---
def generate_insights(data):
    # A. Sales by Product (Bar Chart)
    product_performance = data.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 5))
    product_performance.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Revenue by Product Category', fontsize=14)
    plt.ylabel('Revenue ($)')
    plt.tight_layout()
    plt.savefig('revenue_by_product.png')
    plt.show()

    # B. Regional Distribution (Pie Chart)
    region_share = data.groupby('Region')['Total_Sales'].sum()
    
    plt.figure(figsize=(8, 8))
    region_share.plot(kind='pie', autopct='%1.1f%%', startangle=140, colormap='viridis')
    plt.title('Market Share by Region')
    plt.ylabel('') # Hides the label for cleaner look
    plt.savefig('market_share_region.png')
    plt.show()

    return product_performance, region_share

# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    # Run Pipeline
    df = load_data('sales_data.csv')
    df = clean_data(df)
    prod_stats, region_stats = generate_insights(df)

    # Print Final Summary
    print("\n" + "="*40)
    print("      EXECUTIVE SUMMARY REPORT      ")
    print("="*40)
    print(f"Top Product: {prod_stats.idxmax()} (${prod_stats.max():,.2f})")
    print(f"Top Region:  {region_stats.idxmax()} (${region_stats.max():,.2f})")
    print("-" * 40)
    print("Insights Saved to: revenue_by_product.png & market_share_region.png")
    print("="*40)
