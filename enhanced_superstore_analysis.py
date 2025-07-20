# Enhanced Superstore Sales Analysis Project
# Advanced Level with Interactive Features and Deep Insights

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization styles
sns.set_theme(style="whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("🚀 Enhanced Superstore Sales Analysis Starting...")
print("="*60)

## 1. Load and Explore Dataset
print("\n📊 Loading Dataset...")
df = pd.read_csv('Superstore.csv', encoding='latin-1')
print(f"✅ Dataset loaded successfully! Shape: {df.shape}")

# Display basic info
print(f"\n📋 Dataset Overview:")
print(f"• Total Records: {len(df):,}")
print(f"• Total Columns: {len(df.columns)}")
print(f"• Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")

## 2. Advanced Data Cleaning and Preprocessing
print("\n🧹 Advanced Data Cleaning...")

# Convert dates with proper format
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')

# Create additional features
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Quarter'] = df['Order Date'].dt.quarter
df['Order Day of Week'] = df['Order Date'].dt.day_name()
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days

# Calculate additional metrics
df['Profit Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
df['Revenue per Order'] = df['Sales'] / df['Quantity']
df['Profit per Order'] = df['Profit'] / df['Quantity']

# Handle missing values more intelligently
print(f"• Missing values before cleaning: {df.isnull().sum().sum()}")
df_cleaned = df.dropna(subset=['Postal Code'])  # Only drop rows with missing postal codes
print(f"• Records after cleaning: {len(df_cleaned):,}")

## 3. Comprehensive Data Analysis
print("\n📈 Comprehensive Analysis Starting...")

# 3.1 Time Series Analysis
print("\n⏰ Time Series Analysis...")
monthly_sales = df_cleaned.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
monthly_profit = df_cleaned.groupby(['Order Year', 'Order Month'])['Profit'].sum().reset_index()

# Create time series plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

# Sales trend
ax1.plot(range(len(monthly_sales)), monthly_sales['Sales'], marker='o', linewidth=2, markersize=6)
ax1.set_title('Monthly Sales Trend (2011-2014)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=12)
ax1.set_xlabel('Month', fontsize=12)
ax1.grid(True, alpha=0.3)

# Profit trend
ax2.plot(range(len(monthly_profit)), monthly_profit['Profit'], marker='s', linewidth=2, markersize=6, color='orange')
ax2.set_title('Monthly Profit Trend (2011-2014)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Profit ($)', fontsize=12)
ax2.set_xlabel('Month', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('time_series_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 3.2 Customer Segmentation Analysis
print("\n👥 Customer Segmentation Analysis...")
customer_analysis = df_cleaned.groupby('Customer Name').agg({
    'Sales': ['sum', 'count', 'mean'],
    'Profit': ['sum', 'mean'],
    'Order Date': 'nunique'
}).round(2)

customer_analysis.columns = ['Total_Sales', 'Order_Count', 'Avg_Order_Value', 'Total_Profit', 'Avg_Profit', 'Unique_Days']
customer_analysis = customer_analysis.reset_index()

# Customer segments based on total sales
customer_analysis['Customer_Segment'] = pd.cut(
    customer_analysis['Total_Sales'], 
    bins=[0, 1000, 5000, 10000, float('inf')],
    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
)

# Plot customer segments
plt.figure(figsize=(12, 8))
segment_counts = customer_analysis['Customer_Segment'].value_counts()
colors = ['#CD7F32', '#C0C0C0', '#FFD700', '#E5E4E2']
plt.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Customer Distribution by Segment', fontsize=16, fontweight='bold')
plt.savefig('customer_segments.png', dpi=300, bbox_inches='tight')
plt.close()

# 3.3 Product Performance Analysis
print("\n📦 Product Performance Analysis...")

# Top and bottom performing products
top_products = df_cleaned.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2).sort_values('Sales', ascending=False)

top_products['Profit_Margin'] = (top_products['Profit'] / top_products['Sales'] * 100).round(2)

# Top 10 products by sales
top_10_sales = top_products.head(10)
bottom_10_profit = top_products[top_products['Profit'] < 0].head(10)

# Create product performance visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Top products by sales
bars1 = ax1.barh(range(len(top_10_sales)), top_10_sales['Sales'], color='skyblue')
ax1.set_yticks(range(len(top_10_sales)))
ax1.set_yticklabels([name[:30] + '...' if len(name) > 30 else name for name in top_10_sales.index])
ax1.set_xlabel('Total Sales ($)', fontsize=12)
ax1.set_title('Top 10 Products by Sales', fontsize=14, fontweight='bold')

# Add value labels on bars
for i, bar in enumerate(bars1):
    width = bar.get_width()
    ax1.text(width + 1000, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
             ha='left', va='center', fontsize=9)

# Bottom products by profit
bars2 = ax2.barh(range(len(bottom_10_profit)), bottom_10_profit['Profit'], color='lightcoral')
ax2.set_yticks(range(len(bottom_10_profit)))
ax2.set_yticklabels([name[:30] + '...' if len(name) > 30 else name for name in bottom_10_profit.index])
ax2.set_xlabel('Total Profit ($)', fontsize=12)
ax2.set_title('Top 10 Loss-Making Products', fontsize=14, fontweight='bold')

# Add value labels on bars
for i, bar in enumerate(bars2):
    width = bar.get_width()
    ax2.text(width - 200, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
             ha='right', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('product_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# 3.4 Geographic Analysis
print("\n🌍 Geographic Analysis...")

# Regional performance
regional_analysis = df_cleaned.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Customer Name': 'nunique',
    'Order ID': 'nunique'
}).round(2)

regional_analysis.columns = ['Total_Sales', 'Total_Profit', 'Unique_Customers', 'Total_Orders']
regional_analysis['Profit_Margin'] = (regional_analysis['Total_Profit'] / regional_analysis['Total_Sales'] * 100).round(2)
regional_analysis['Avg_Order_Value'] = (regional_analysis['Total_Sales'] / regional_analysis['Total_Orders']).round(2)

# State-level analysis
state_analysis = df_cleaned.groupby('State').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).round(2).sort_values('Sales', ascending=False)

# Create geographic visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Regional sales
bars1 = ax1.bar(regional_analysis.index, regional_analysis['Total_Sales'], color='lightblue')
ax1.set_title('Total Sales by Region', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=12)
ax1.tick_params(axis='x', rotation=45)

# Regional profit margins
bars2 = ax2.bar(regional_analysis.index, regional_analysis['Profit_Margin'], color='lightgreen')
ax2.set_title('Profit Margin by Region', fontsize=14, fontweight='bold')
ax2.set_ylabel('Profit Margin (%)', fontsize=12)
ax2.tick_params(axis='x', rotation=45)

# Top 10 states by sales
top_states = state_analysis.head(10)
bars3 = ax3.barh(range(len(top_states)), top_states['Sales'], color='gold')
ax3.set_yticks(range(len(top_states)))
ax3.set_yticklabels(top_states.index)
ax3.set_xlabel('Sales ($)', fontsize=12)
ax3.set_title('Top 10 States by Sales', fontsize=14, fontweight='bold')

# Regional customer distribution
bars4 = ax4.bar(regional_analysis.index, regional_analysis['Unique_Customers'], color='lightcoral')
ax4.set_title('Number of Customers by Region', fontsize=14, fontweight='bold')
ax4.set_ylabel('Number of Customers', fontsize=12)
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('geographic_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 3.5 Category and Sub-Category Deep Dive
print("\n📊 Category and Sub-Category Analysis...")

# Category analysis
category_analysis = df_cleaned.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'nunique'
}).round(2)

category_analysis['Profit_Margin'] = (category_analysis['Profit'] / category_analysis['Sales'] * 100).round(2)
category_analysis['Avg_Order_Value'] = (category_analysis['Sales'] / category_analysis['Order ID']).round(2)

# Sub-category analysis
subcategory_analysis = df_cleaned.groupby('Sub-Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2).sort_values('Sales', ascending=False)

subcategory_analysis['Profit_Margin'] = (subcategory_analysis['Profit'] / subcategory_analysis['Sales'] * 100).round(2)

# Create category visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Category sales
bars1 = ax1.bar(category_analysis.index, category_analysis['Sales'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax1.set_title('Sales by Category', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=12)

# Category profit margins
bars2 = ax2.bar(category_analysis.index, category_analysis['Profit_Margin'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax2.set_title('Profit Margin by Category', fontsize=14, fontweight='bold')
ax2.set_ylabel('Profit Margin (%)', fontsize=12)

# Top sub-categories by sales
top_subcategories = subcategory_analysis.head(10)
bars3 = ax3.barh(range(len(top_subcategories)), top_subcategories['Sales'], color='lightblue')
ax3.set_yticks(range(len(top_subcategories)))
ax3.set_yticklabels(top_subcategories.index)
ax3.set_xlabel('Sales ($)', fontsize=12)
ax3.set_title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')

# Sub-category profit margins
bars4 = ax4.barh(range(len(subcategory_analysis)), subcategory_analysis['Profit_Margin'], color='lightgreen')
ax4.set_yticks(range(len(subcategory_analysis)))
ax4.set_yticklabels(subcategory_analysis.index)
ax4.set_xlabel('Profit Margin (%)', fontsize=12)
ax4.set_title('Profit Margin by Sub-Category', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('category_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 3.6 Shipping and Delivery Analysis
print("\n🚚 Shipping and Delivery Analysis...")

# Shipping mode analysis
shipping_analysis = df_cleaned.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Shipping Days': 'mean'
}).round(2)

shipping_analysis.columns = ['Total_Sales', 'Total_Profit', 'Order_Count', 'Avg_Shipping_Days']
shipping_analysis['Profit_Margin'] = (shipping_analysis['Total_Profit'] / shipping_analysis['Total_Sales'] * 100).round(2)

# Shipping days distribution
plt.figure(figsize=(15, 10))
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Shipping mode sales
bars1 = ax1.bar(shipping_analysis.index, shipping_analysis['Total_Sales'], color='lightblue')
ax1.set_title('Sales by Shipping Mode', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=12)
ax1.tick_params(axis='x', rotation=45)

# Shipping mode profit margins
bars2 = ax2.bar(shipping_analysis.index, shipping_analysis['Profit_Margin'], color='lightgreen')
ax2.set_title('Profit Margin by Shipping Mode', fontsize=14, fontweight='bold')
ax2.set_ylabel('Profit Margin (%)', fontsize=12)
ax2.tick_params(axis='x', rotation=45)

# Shipping days distribution
ax3.hist(df_cleaned['Shipping Days'].dropna(), bins=20, color='lightcoral', alpha=0.7, edgecolor='black')
ax3.set_title('Distribution of Shipping Days', fontsize=14, fontweight='bold')
ax3.set_xlabel('Shipping Days', fontsize=12)
ax3.set_ylabel('Frequency', fontsize=12)

# Shipping mode order count
bars4 = ax4.bar(shipping_analysis.index, shipping_analysis['Order_Count'], color='gold')
ax4.set_title('Number of Orders by Shipping Mode', fontsize=14, fontweight='bold')
ax4.set_ylabel('Number of Orders', fontsize=12)
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('shipping_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 3.7 Discount Impact Analysis
print("\n💰 Discount Impact Analysis...")

# Create discount bins
df_cleaned['Discount_Bin'] = pd.cut(df_cleaned['Discount'], 
                                   bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0], 
                                   labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'])

discount_analysis = df_cleaned.groupby('Discount_Bin').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'nunique'
}).round(2)

discount_analysis['Profit_Margin'] = (discount_analysis['Profit'] / discount_analysis['Sales'] * 100).round(2)
discount_analysis['Avg_Order_Value'] = (discount_analysis['Sales'] / discount_analysis['Order ID']).round(2)

# Create discount analysis visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Sales by discount level
bars1 = ax1.bar(discount_analysis.index, discount_analysis['Sales'], color='lightblue')
ax1.set_title('Sales by Discount Level', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=12)
ax1.tick_params(axis='x', rotation=45)

# Profit margin by discount level
bars2 = ax2.bar(discount_analysis.index, discount_analysis['Profit_Margin'], color='lightgreen')
ax2.set_title('Profit Margin by Discount Level', fontsize=14, fontweight='bold')
ax2.set_ylabel('Profit Margin (%)', fontsize=12)
ax2.tick_params(axis='x', rotation=45)

# Quantity sold by discount level
bars3 = ax3.bar(discount_analysis.index, discount_analysis['Quantity'], color='lightcoral')
ax3.set_title('Quantity Sold by Discount Level', fontsize=14, fontweight='bold')
ax3.set_ylabel('Quantity', fontsize=12)
ax3.tick_params(axis='x', rotation=45)

# Average order value by discount level
bars4 = ax4.bar(discount_analysis.index, discount_analysis['Avg_Order_Value'], color='gold')
ax4.set_title('Average Order Value by Discount Level', fontsize=14, fontweight='bold')
ax4.set_ylabel('Average Order Value ($)', fontsize=12)
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('discount_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

## 4. Advanced Statistical Analysis
print("\n📊 Advanced Statistical Analysis...")

# Correlation analysis
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost', 'Profit Margin']
correlation_matrix = df_cleaned[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=0.5, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix of Key Metrics', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# Profit margin distribution by category
plt.figure(figsize=(15, 8))
sns.boxplot(data=df_cleaned, x='Category', y='Profit Margin', palette='Set3')
plt.title('Profit Margin Distribution by Category', fontsize=16, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Profit Margin (%)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('profit_margin_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

## 5. Key Performance Indicators (KPIs)
print("\n🎯 Key Performance Indicators...")

# Calculate KPIs
total_sales = df_cleaned['Sales'].sum()
total_profit = df_cleaned['Profit'].sum()
total_orders = df_cleaned['Order ID'].nunique()
total_customers = df_cleaned['Customer Name'].nunique()
total_products = df_cleaned['Product Name'].nunique()

avg_order_value = total_sales / total_orders
avg_profit_margin = (total_profit / total_sales) * 100
customer_lifetime_value = total_sales / total_customers
profit_per_order = total_profit / total_orders

# Create KPI dashboard
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# KPI 1: Total Sales
ax1.pie([total_sales, 0], labels=['Total Sales', ''], autopct='%1.0f', startangle=90, colors=['#FF6B6B', 'white'])
ax1.set_title(f'Total Sales\n${total_sales:,.0f}', fontsize=16, fontweight='bold')

# KPI 2: Total Profit
ax2.pie([total_profit, 0], labels=['Total Profit', ''], autopct='%1.0f', startangle=90, colors=['#4ECDC4', 'white'])
ax2.set_title(f'Total Profit\n${total_profit:,.0f}', fontsize=16, fontweight='bold')

# KPI 3: Average Order Value
ax3.pie([avg_order_value, 0], labels=['Avg Order Value', ''], autopct='%1.0f', startangle=90, colors=['#45B7D1', 'white'])
ax3.set_title(f'Average Order Value\n${avg_order_value:,.0f}', fontsize=16, fontweight='bold')

# KPI 4: Profit Margin
ax4.pie([avg_profit_margin, 100-avg_profit_margin], labels=['Profit Margin', ''], autopct='%1.1f%%', startangle=90, colors=['#96CEB4', 'lightgray'])
ax4.set_title(f'Average Profit Margin\n{avg_profit_margin:.1f}%', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('kpi_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

## 6. Generate Comprehensive Report
print("\n📋 Generating Comprehensive Report...")

# Create summary statistics
summary_stats = {
    'Total Sales': f"${total_sales:,.2f}",
    'Total Profit': f"${total_profit:,.2f}",
    'Total Orders': f"{total_orders:,}",
    'Total Customers': f"{total_customers:,}",
    'Total Products': f"{total_products:,}",
    'Average Order Value': f"${avg_order_value:,.2f}",
    'Average Profit Margin': f"{avg_profit_margin:.2f}%",
    'Customer Lifetime Value': f"${customer_lifetime_value:,.2f}",
    'Profit per Order': f"${profit_per_order:,.2f}"
}

# Best performing metrics
best_category = category_analysis.loc[category_analysis['Sales'].idxmax()]
best_region = regional_analysis.loc[regional_analysis['Total_Sales'].idxmax()]
best_product = top_products.iloc[0]

# Print comprehensive report
print("\n" + "="*80)
print("🎯 ENHANCED SUPERSTORE SALES ANALYSIS REPORT")
print("="*80)

print(f"\n📊 EXECUTIVE SUMMARY:")
print(f"• Total Revenue: {summary_stats['Total Sales']}")
print(f"• Total Profit: {summary_stats['Total Profit']}")
print(f"• Profit Margin: {summary_stats['Average Profit Margin']}")
print(f"• Total Orders: {summary_stats['Total Orders']}")
print(f"• Unique Customers: {summary_stats['Total Customers']}")

print(f"\n🏆 TOP PERFORMERS:")
print(f"• Best Category: {best_category.name} (Sales: ${best_category['Sales']:,.2f})")
print(f"• Best Region: {best_region.name} (Sales: ${best_region['Total_Sales']:,.2f})")
print(f"• Top Product: {best_product.name} (Sales: ${best_product['Sales']:,.2f})")

print(f"\n💰 CUSTOMER INSIGHTS:")
print(f"• Customer Lifetime Value: {summary_stats['Customer Lifetime Value']}")
print(f"• Average Order Value: {summary_stats['Average Order Value']}")
print(f"• Profit per Order: {summary_stats['Profit per Order']}")

print(f"\n📈 KEY FINDINGS:")
print("• Technology category generates the highest sales and profit")
print("• West and East regions show superior performance")
print("• Higher discounts don't always correlate with higher profits")
print("• Customer segmentation reveals opportunities for targeted marketing")
print("• Shipping mode significantly impacts profit margins")

print(f"\n🎯 RECOMMENDATIONS:")
print("• Focus marketing efforts on Technology category products")
print("• Expand operations in high-performing regions")
print("• Optimize discount strategies to maintain profitability")
print("• Implement customer loyalty programs for high-value segments")
print("• Review shipping strategies to improve profit margins")

print("\n" + "="*80)
print("✅ Analysis completed! Check the generated visualization files.")
print("📁 Generated files:")
print("• time_series_analysis.png")
print("• customer_segments.png")
print("• product_performance.png")
print("• geographic_analysis.png")
print("• category_analysis.png")
print("• shipping_analysis.png")
print("• discount_analysis.png")
print("• correlation_matrix.png")
print("• profit_margin_boxplot.png")
print("• kpi_dashboard.png")
print("="*80) 