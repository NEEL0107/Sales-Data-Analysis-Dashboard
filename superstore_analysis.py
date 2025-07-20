# Superstore Sales Analysis Project (Advanced Level)

## 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization styles
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

## 2. Load Dataset
df = pd.read_csv('Superstore.csv', encoding='latin-1')
print("Dataset Loaded Successfully!")
print(df.head())

## 3. Initial Data Exploration
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Info:")
print(df.info())
print("Missing Values:")
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

## 4. Data Cleaning

# Convert dates to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')

# Drop duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.dropna(inplace=True)

print("Data cleaning completed!")
print("New shape after cleaning:", df.shape)

## 5. Univariate Analysis

# Sales Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Sales'], bins=50, kde=True, color='skyblue')
plt.title('Sales Distribution')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.savefig('sales_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Profit Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Profit'], bins=50, kde=True, color='lightgreen')
plt.title('Profit Distribution')
plt.xlabel('Profit')
plt.ylabel('Frequency')
plt.savefig('profit_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Top 10 Products by Sales
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')
plt.title('Top 10 Products by Total Sales')
plt.xlabel('Total Sales')
plt.ylabel('Product Name')
plt.savefig('top_products_sales.png', dpi=300, bbox_inches='tight')
plt.close()

## 6. Bivariate Analysis

# Sales vs Profit
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Sales', y='Profit', hue='Category', alpha=0.6)
plt.title('Sales vs Profit')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.legend(title='Category')
plt.savefig('sales_vs_profit.png', dpi=300, bbox_inches='tight')
plt.close()

# Discount vs Profit
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Sub-Category', alpha=0.6)
plt.title('Discount vs Profit')
plt.xlabel('Discount')
plt.ylabel('Profit')
plt.legend(title='Sub-Category')
plt.savefig('discount_vs_profit.png', dpi=300, bbox_inches='tight')
plt.close()

# Region vs Profit
region_profit = df.groupby('Region')['Profit'].sum().sort_values()
plt.figure(figsize=(10, 6))
sns.barplot(x=region_profit.index, y=region_profit.values, palette='mako')
plt.title('Total Profit by Region')
plt.xlabel('Region')
plt.ylabel('Total Profit')
plt.xticks(rotation=45)
plt.savefig('profit_by_region.png', dpi=300, bbox_inches='tight')
plt.close()

## 7. Advanced Insights

# Correlation Heatmap
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
plt.figure(figsize=(8, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# Category-wise Profit Analysis
cat_profit = df.groupby('Category')['Profit'].sum().sort_values()
plt.figure(figsize=(10, 6))
sns.barplot(x=cat_profit.index, y=cat_profit.values, palette='Set2')
plt.title("Total Profit by Category")
plt.ylabel("Profit")
plt.xlabel("Category")
plt.savefig('profit_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Sub-category level insights
sub_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()
sub_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values()
fig, ax = plt.subplots(1, 2, figsize=(18, 6))
sns.barplot(x=sub_profit.values, y=sub_profit.index, ax=ax[0], palette='cubehelix')
ax[0].set_title('Profit by Sub-Category')
sns.barplot(x=sub_sales.values, y=sub_sales.index, ax=ax[1], palette='plasma')
ax[1].set_title('Sales by Sub-Category')
plt.tight_layout()
plt.savefig('subcategory_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

## 8. Conclusion

print("\n" + "="*50)
print("KEY TAKEAWAYS:")
print("="*50)
print("- High discount does not always lead to higher profit.")
print("- Technology category yields highest profit on average.")
print("- Some sub-categories contribute negative profit (losses).")
print("- West and East regions show better profitability.")

# Additional insights
print("\n" + "="*50)
print("ADDITIONAL INSIGHTS:")
print("="*50)
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Average Profit Margin: {(df['Profit'].sum() / df['Sales'].sum() * 100):.2f}%")
print(f"Number of Orders: {len(df)}")
print(f"Number of Products: {df['Product Name'].nunique()}")
print(f"Number of Customers: {df['Customer Name'].nunique()}")

print("\nAnalysis completed! Check the generated PNG files for visualizations.") 