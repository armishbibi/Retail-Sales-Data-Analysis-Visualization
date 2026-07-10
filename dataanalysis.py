import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


#setting up visualization style
plt.style.use('seaborn-v0_8')
sns.set_palette('husl')

df = pd.read_csv('retail_sales.csv')

invalid_strings = ['Null', 'NaN?', 'Nan', 'null', 'nan']
df = df.replace(invalid_strings, np.nan)

df.head(10)



#Basic Data Information adn Structure
print("DATASET BASIC INFORMATION")
print(f'Dataset Dimensions: {df.shape[0]} rows x {df.shape[1]} columns')
print('\nColumn Names and Data Types')
print(df.dtypes)

print('\nMissing Values:')
print(df.isnull().sum())
print('\nDataset Summary:')
df.info()

#Data type conversion and cleaning
print('\nDATA CLEANING AND TYPE CONVERSION')

#convert Date to datetime format
df['Date'] = pd.to_datetime(df['Date'])

#extraxt additional time features
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter
df['DayOfWeek'] = df['Date'].dt.day_name()
df['MonthName'] = df['Date'].dt.month_name()

#ensure numeric columns are properly formatted
numeric_columns = ['Sales', 'Quantity', 'Profit']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

print('Data type after conversion:')
print(df.dtypes)
print(f'\nDate Range" {df['Date'].min()} to {df['Date'].max()}')

#Basic Statistical Summary 
print('\nSTATISTICAL SUMMARY')
print('Descriptive Statistics for Numerical Columns:')
print(df[['Sales', 'Quantity', 'Profit']].describe())

print('\nCategory Wise Summary')
category_summary = df.groupby('Category').agg({
    'Sales' : ['count', 'sum', 'mean', 'std'],
    'Profit' : ['sum', 'mean'],
    'Quantity' : ['sum', 'mean']
}).round(2)
print(category_summary)

print('\nRegion Wise Summary: ')
region_summary = df.groupby('Region').agg({
    'Sales' : ['sum', 'mean'],
    'Profit' : ['sum', 'mean']
}).round(2)
print(region_summary)

#Monthly sales trend analysis
print('\nMONTHLY SALES TREND ANALYSIS')

#Calculate monhtly sales
monthly_sales = df.groupby(['Month', 'MonthName']).agg({
    'Sales'  : 'sum',
    'Profit' : 'sum',
    'Quantity' : 'sum'
}).reset_index()

monthly_sales = monthly_sales.sort_values('Month')
print('Monthly Sales Summary')
print(monthly_sales)

#Visualizations: Monthly Sales Trend
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales['MonthName'], monthly_sales['Sales'],
         marker = 'o', linewidth=2, markersize=8, label='Total Sales')
plt.plot(monthly_sales['MonthName'] , monthly_sales['Profit'],
         marker = 's', linewidth=2, markersize=8, label = 'Total Profit')
plt.title('Monthly Sales and Profit Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Amount ($)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Category Performance Analysis
print('\nCATEGORY PERFORMANCE ANALYSIS')

category_performance = df.groupby('Category').agg({
    'Sales' : 'sum',
    'Profit' : 'sum',
    'Quantity' : 'sum'
}).sort_values('Sales', ascending=False)

print('Category Performance (Sorted by Sales): ')
print(category_performance)

#Visualization: Top categories by sales
plt.figure(figsize=(10, 6))
colors = plt.cm.Set3(np.linspace(0, 1, len(category_performance)))
bars = plt.bar(category_performance.index, category_performance['Sales'],
               color=colors, alpha=0.8)

#Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}', ha='center', va='bottom')
    
plt.title('Total Sales by Product Category', fontsize=16, fontweight='bold')
plt.xlabel('Product Category', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

#Regional Performance Analysis
print('\nREGIONAL PERFORMANCE ANALYSIS')

regional_performance = df.groupby('Region').agg({
    'Sales' : ['sum', 'mean', 'count'],
    'Profit' : ['sum', 'mean']
}).round(2)

print('Regional Performance:')
print(regional_performance)

#Visualization: Regional Sales Distribution
plt.figure(figsize=(12, 8))
regional_data = df.groupby('Region')['Sales'].sum()
plt.pie(regional_data, labels=regional_data.index, autopct='%1.1f%%',
      startangle=90, colors=sns.color_palette('pastel'))
plt.title('Sales Distribution By Region', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

#Day of Week Analysis
print('\nDAY OF WEEK ANALYSIS')

#define proper order for days
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)

daily_performance = df.groupby('DayOfWeek').agg({
    'Sales' :'mean',
    'Profit' : 'mean',
    'Quantity' : 'mean'
}).round(2)

print('Average performance by Day Of Week')
print(daily_performance)

#Visualization: Daily Sales Pattern
plt.figure(figsize=(10, 6))
plt.plot(daily_performance.index, daily_performance['Sales'],
         marker = 'o', linewidth=2, markersize=8, label='Average Sales')
plt.plot(daily_performance.index, daily_performance['Profit'],
         marker='s', linewidth=2, markersize=8, label='Average Profit')
plt.title('Average Sales and Profit by Day of Week', fontsize=16, fontweight='bold')
plt.xlabel('Day Of Week', fontsize=12)
plt.ylabel('Amount($)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Correlation Analysis
print('\nCORRELATION ANALYSIS')

#select numerical column for correlation
numerical_df = df[['Sales', 'Quantity', 'Profit', 'Month']]
correlation_matrix = numerical_df.corr()

print('Correlation Matrix:')
print(correlation_matrix)

#Heatmap Visualization
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=0.5)
plt.title('Correlation Matrix of Numerical Variables', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

#4-Chart Mini Dashboard
print('\n4-CHART RETAIL SALES DASHBOARD')

#create a 2x2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(15,12), layout='constrained')
fig.suptitle('Retail Sales Analysis Dashboard', fontsize=20, fontweight='bold')

#Chart 1: Monthly Sales Trend (Top-Left)
axes[0, 0].plot(monthly_sales['MonthName'], monthly_sales['Sales'], 
                marker='o', linewidth=2, color='blue', label='Sales')
axes[0, 0].plot(monthly_sales['MonthName'], monthly_sales['Profit'],
                marker='s', linewidth=2, color='red', label='Profit')
axes[0, 0].set_title('Monthly Sales & Profit Trend', fontweight='bold')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Amount($)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

#Chart 2: Top Categories(Top-Right)
colors = plt.cm.viridis(np.linspace(0, 1, len(category_performance)))
bars = axes[0, 1].bar(category_performance.index, category_performance['Sales'],
                      color = colors, alpha = 0.8)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/.2, height,
             f'{height:.0f}', ha='center', va='bottom')
axes[0, 1].set_title('Sales by Product Category', fontweight='bold')
axes[0, 1].set_xlabel('Category')
axes[0, 1].set_ylabel('Total Sales($)')
axes[0, 1].tick_params(axis='x', rotation=45)

#Chart 3: Regional Sales Distribution(Bottom-Left)
axes[1, 0].pie(regional_data, labels=regional_data.index, autopct='%1.1f%%',
               startangle=90,colors=sns.color_palette('pastel'))
axes[1, 0].set_title('Sales Distribution By Region')
axes[1, 0].axis('equal')

#Chart 4: Days Of Week Sales(Bottom-Right)
axes[1, 1].plot(daily_performance.index, daily_performance['Sales'],
                marker = 'o', linewidth=2, markersize=8 )
axes[1, 1].set_title('Average Sales By Days of the Week', fontweight='bold')
axes[1, 1].set_xlabel('Day of Week')
axes[1, 1].set_ylabel('Average Sales($)')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.subplots_adjust(hspace=0.7, wspace=0.3)
plt.show()

#Key Insights and Recommendations

print('\nKEY INSIGHTS AND RECOMMENDATIONS')

print('\nKEY FINDINGS')
print('1.Top Performing Category: ', category_performance.index[0])
print('2. Best Performing Region: ', regional_data.idxmax())
print('3. Hgihest Sales Month: ', monthly_sales.loc[monthly_sales['Sales'].idxmax(), 'MonthName'])
print('4. Best Day Of Week: ', daily_performance['Sales'].idxmax())
print('5. Total Annual Sales: ${:,.2f}'.format(df['Sales'].sum()))
print('6. Total Annual Profit: ${:,.2f}'.format(df['Sales'].sum()))

print('\nBUSINESS RECOMMENDATION')
print('1. Focus marketing efforts on ', category_performance.index[0], 'category')
print('2. Investigate performance in lower-performing regions')
print('3. Plan promotion around ', daily_performance['Sales'].idxmax(), ' to maximize sales' )
print('4. Allocate Inventory based on monthly trend patterns')
print('5. Monitor correlation between quantity and profit for pricing strategy')

print('\nPROFITABILITY ANALYSIS')
profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100
print(f'Overall Profit Margin: {profit_margin:.2f}%')

#Category Profit Margin
category_margins = (category_performance['Profit'] / category_performance['Sales']) * 100
print('\nProfit Margins by Cateogry:')
for category, margin in category_margins.items():
    print(f' {category} : {margin:.2f}%')