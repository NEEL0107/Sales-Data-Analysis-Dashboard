# Interactive Superstore Sales Dashboard
# Using Streamlit for interactive visualizations

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Superstore.csv', encoding='latin-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')
    
    # Create additional features
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order Quarter'] = df['Order Date'].dt.quarter
    df['Order Day of Week'] = df['Order Date'].dt.day_name()
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Profit Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
    
    return df.dropna(subset=['Postal Code'])

# Load data
df = load_data()

# Header
st.markdown('<h1 class="main-header">📊 Superstore Sales Dashboard</h1>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Category filter
categories = ['All'] + list(df['Category'].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Region filter
regions = ['All'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Apply filters
filtered_df = df.copy()
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Order Date'].dt.date >= date_range[0]) &
        (filtered_df['Order Date'].dt.date <= date_range[1])
    ]

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['Sales'].sum()
    st.metric("💰 Total Sales", f"${total_sales:,.0f}")

with col2:
    total_profit = filtered_df['Profit'].sum()
    st.metric("📈 Total Profit", f"${total_profit:,.0f}")

with col3:
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    st.metric("🎯 Profit Margin", f"{profit_margin:.1f}%")

with col4:
    total_orders = filtered_df['Order ID'].nunique()
    st.metric("📦 Total Orders", f"{total_orders:,}")

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Sales Overview", "👥 Customers", "📦 Products", "🌍 Geography", "🚚 Operations"])

with tab1:
    st.header("📈 Sales Overview")
    
    # Time series analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly sales trend
        monthly_sales = filtered_df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
        monthly_sales['Period'] = monthly_sales['Order Year'].astype(str) + '-' + monthly_sales['Order Month'].astype(str).str.zfill(2)
        
        fig = px.line(monthly_sales, x='Period', y='Sales', 
                     title='Monthly Sales Trend',
                     labels={'Sales': 'Sales ($)', 'Period': 'Month'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales by category
        category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig = px.pie(category_sales, values='Sales', names='Category',
                    title='Sales Distribution by Category')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Profit analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit margin by category
        category_profit = filtered_df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        category_profit['Profit_Margin'] = (category_profit['Profit'] / category_profit['Sales'] * 100)
        
        fig = px.bar(category_profit, x='Category', y='Profit_Margin',
                    title='Profit Margin by Category',
                    labels={'Profit_Margin': 'Profit Margin (%)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales vs Profit scatter
        fig = px.scatter(filtered_df, x='Sales', y='Profit', color='Category',
                        title='Sales vs Profit by Category',
                        labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("👥 Customer Analysis")
    
    # Customer segmentation
    customer_analysis = filtered_df.groupby('Customer Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    customer_analysis['Customer_Segment'] = pd.cut(
        customer_analysis['Sales'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['Bronze', 'Silver', 'Gold', 'Platinum']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer segments
        segment_counts = customer_analysis['Customer_Segment'].value_counts()
        fig = px.pie(values=segment_counts.values, names=segment_counts.index,
                    title='Customer Distribution by Segment')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top customers
        top_customers = customer_analysis.nlargest(10, 'Sales')
        fig = px.bar(top_customers, x='Customer Name', y='Sales',
                    title='Top 10 Customers by Sales',
                    labels={'Sales': 'Sales ($)'})
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_customers = filtered_df['Customer Name'].nunique()
        st.metric("👥 Total Customers", f"{total_customers:,}")
    
    with col2:
        avg_order_value = filtered_df['Sales'].sum() / filtered_df['Order ID'].nunique()
        st.metric("💰 Avg Order Value", f"${avg_order_value:,.0f}")
    
    with col3:
        customer_lifetime_value = filtered_df['Sales'].sum() / total_customers
        st.metric("💎 Customer LTV", f"${customer_lifetime_value:,.0f}")

with tab3:
    st.header("📦 Product Analysis")
    
    # Product performance
    product_analysis = filtered_df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    product_analysis['Profit_Margin'] = (product_analysis['Profit'] / product_analysis['Sales'] * 100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top products by sales
        top_products = product_analysis.nlargest(10, 'Sales')
        fig = px.bar(top_products, x='Sales', y='Product Name', orientation='h',
                    title='Top 10 Products by Sales',
                    labels={'Sales': 'Sales ($)'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sub-category analysis
        subcategory_analysis = filtered_df.groupby('Sub-Category').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        subcategory_analysis['Profit_Margin'] = (subcategory_analysis['Profit'] / subcategory_analysis['Sales'] * 100)
        
        fig = px.bar(subcategory_analysis, x='Sub-Category', y='Profit_Margin',
                    title='Profit Margin by Sub-Category',
                    labels={'Profit_Margin': 'Profit Margin (%)'})
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Product metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_products = filtered_df['Product Name'].nunique()
        st.metric("📦 Total Products", f"{total_products:,}")
    
    with col2:
        best_product = product_analysis.loc[product_analysis['Sales'].idxmax()]
        st.metric("🏆 Best Product", best_product['Product Name'][:30] + "...")
    
    with col3:
        avg_profit_margin = product_analysis['Profit_Margin'].mean()
        st.metric("📊 Avg Profit Margin", f"{avg_profit_margin:.1f}%")

with tab4:
    st.header("🌍 Geographic Analysis")
    
    # Regional analysis
    regional_analysis = filtered_df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Customer Name': 'nunique',
        'Order ID': 'nunique'
    }).reset_index()
    
    regional_analysis['Profit_Margin'] = (regional_analysis['Profit'] / regional_analysis['Sales'] * 100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Regional sales
        fig = px.bar(regional_analysis, x='Region', y='Sales',
                    title='Sales by Region',
                    labels={'Sales': 'Sales ($)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional profit margins
        fig = px.bar(regional_analysis, x='Region', y='Profit_Margin',
                    title='Profit Margin by Region',
                    labels={'Profit_Margin': 'Profit Margin (%)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # State analysis
    state_analysis = filtered_df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index().sort_values('Sales', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top states by sales
        top_states = state_analysis.head(10)
        fig = px.bar(top_states, x='State', y='Sales',
                    title='Top 10 States by Sales',
                    labels={'Sales': 'Sales ($)'})
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # State profit margins
        state_analysis['Profit_Margin'] = (state_analysis['Profit'] / state_analysis['Sales'] * 100)
        top_profit_states = state_analysis.nlargest(10, 'Profit_Margin')
        fig = px.bar(top_profit_states, x='State', y='Profit_Margin',
                    title='Top 10 States by Profit Margin',
                    labels={'Profit_Margin': 'Profit Margin (%)'})
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("🚚 Operations Analysis")
    
    # Shipping analysis
    shipping_analysis = filtered_df.groupby('Ship Mode').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Shipping Days': 'mean'
    }).reset_index()
    
    shipping_analysis['Profit_Margin'] = (shipping_analysis['Profit'] / shipping_analysis['Sales'] * 100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Shipping mode sales
        fig = px.bar(shipping_analysis, x='Ship Mode', y='Sales',
                    title='Sales by Shipping Mode',
                    labels={'Sales': 'Sales ($)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Shipping mode profit margins
        fig = px.bar(shipping_analysis, x='Ship Mode', y='Profit_Margin',
                    title='Profit Margin by Shipping Mode',
                    labels={'Profit_Margin': 'Profit Margin (%)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Discount analysis
    filtered_df['Discount_Bin'] = pd.cut(filtered_df['Discount'],
                                        bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0],
                                        labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'])
    
    discount_analysis = filtered_df.groupby('Discount_Bin').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    discount_analysis['Profit_Margin'] = (discount_analysis['Profit'] / discount_analysis['Sales'] * 100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by discount level
        fig = px.bar(discount_analysis, x='Discount_Bin', y='Sales',
                    title='Sales by Discount Level',
                    labels={'Sales': 'Sales ($)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit margin by discount level
        fig = px.bar(discount_analysis, x='Discount_Bin', y='Profit_Margin',
                    title='Profit Margin by Discount Level',
                    labels={'Profit_Margin': 'Profit Margin (%)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 Enhanced Superstore Sales Analysis Dashboard | Built with Streamlit and Plotly</p>
    <p>Data Source: Superstore Sales Dataset | Analysis Period: 2011-2014</p>
</div>
""", unsafe_allow_html=True) 