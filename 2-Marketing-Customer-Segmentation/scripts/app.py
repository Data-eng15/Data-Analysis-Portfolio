# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Streamlit Page Config
st.set_page_config(page_title="Customer Segmentation Analysis", layout="wide")

# Title
st.title("🛍️ Customer Segmentation Project – Mall Customers Dataset")

# Introduction Section
st.header("📌 Project Objective")
st.write("""
This project performs **Customer Segmentation** using the Mall Customers dataset to help the marketing team:
- Understand customer groups based on **Annual Income** and **Spending Score**
- Design targeted marketing strategies for each segment
""")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('D:/Data-Analysis-Portfolio/2-Marketing-Customer-Segmentation/scripts/data/Mall_Customers.csv')

df = load_data()

# Display Data Sample
st.subheader("🔍 Sample Data")
st.dataframe(df.head())

# Approach Explanation
st.header("📝 Project Approach")
st.write("""
1. **Data Understanding** – explored customer demographics and behaviour  
2. **Descriptive Analysis** – analysed age, gender, income, spending distributions  
3. **Behavioural Analysis** – visualised income vs spending behaviour  
4. **K-Means Segmentation** – segmented customers into distinct groups  
5. **Business Insights** – interpreted segments for marketing strategy
""")

# Descriptive Analysis
st.subheader("📊 Descriptive Analysis Visualisations")

# Age Distribution
st.write("**Age Distribution:**")
fig1, ax1 = plt.subplots()
sns.histplot(df['Age'], bins=15, kde=True, color='skyblue', ax=ax1)
ax1.set_title('Age Distribution')
st.pyplot(fig1)
st.write("✅ **Insight:** Majority customers are between 20-40 years, ideal for targeting fashion and lifestyle products.")

# Gender Distribution
st.write("**Gender Distribution:**")
fig2, ax2 = plt.subplots()
sns.countplot(x='Gender', data=df, palette='pastel', ax=ax2)
ax2.set_title('Gender Distribution')
st.pyplot(fig2)
st.write("✅ **Insight:** Female customers are slightly more, useful for designing gender-targeted campaigns.")

# Annual Income Distribution
st.write("**Annual Income Distribution:**")
fig3, ax3 = plt.subplots()
sns.histplot(df['Annual Income (k$)'], bins=15, kde=True, color='salmon', ax=ax3)
ax3.set_title('Annual Income Distribution')
st.pyplot(fig3)
st.write("✅ **Insight:** Income is widely distributed, indicating the need for different pricing strategies.")

# Spending Score Distribution
st.write("**Spending Score Distribution:**")
fig4, ax4 = plt.subplots()
sns.histplot(df['Spending Score (1-100)'], bins=15, kde=True, color='lightgreen', ax=ax4)
ax4.set_title('Spending Score Distribution')
st.pyplot(fig4)
st.write("✅ **Insight:** Spending scores are evenly distributed; some customers spend very low, some very high.")

# Income vs Spending Scatter Plot
st.write("**Annual Income vs Spending Score Scatter Plot:**")
fig5, ax5 = plt.subplots()
sns.scatterplot(x='Annual Income (k$)', y='Spending Score (1-100)', hue='Gender', data=df, palette='Set2', ax=ax5)
ax5.set_title('Income vs Spending Score by Gender')
st.pyplot(fig5)
st.write("✅ **Insight:** High income does not guarantee high spending; there are varied behaviour patterns.")

# K-Means Clustering Segmentation
st.header("🎯 K-Means Customer Segmentation")

# Selecting features
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# Elbow Method for optimal k
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Elbow Plot
st.write("**Elbow Method to find optimal clusters:**")
fig6, ax6 = plt.subplots()
ax6.plot(range(1,11), wcss, marker='o', linestyle='--')
ax6.set_title('Elbow Method For Optimal k')
ax6.set_xlabel('Number of Clusters')
ax6.set_ylabel('WCSS')
st.pyplot(fig6)
st.write("✅ **Insight:** Elbow bends at k=5, optimal for segmentation here.")

# Final KMeans with k=5
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# Cluster Visualisation
st.write("**Customer Segments Visualisation:**")
fig7, ax7 = plt.subplots()
sns.scatterplot(x='Annual Income (k$)', y='Spending Score (1-100)',
                hue='Cluster', palette='Set2', data=df, ax=ax7, s=100)
ax7.set_title('Customer Segments (K-Means)')
st.pyplot(fig7)

# Business Interpretation
st.subheader("💡 Business Insights & Recommendations")
st.write("""
- **Cluster 0:** High Income, Low Spending ➔ Promote premium loyalty programs  
- **Cluster 1:** Low Income, High Spending ➔ Retain with exclusive deals  
- **Cluster 2:** Average Income and Spending ➔ Upsell mid-range products  
- **Cluster 3:** Low Income, Low Spending ➔ Basic awareness campaigns  
- **Cluster 4:** High Income, High Spending ➔ Focus for premium high-value sales

✅ **Overall Recommendation:** Tailor marketing strategies for each segment to maximise ROI and customer satisfaction.
""")

# Final Note
st.header("🎉 Project Summary")
st.write("""
This app performed **Customer Segmentation** using K-Means Clustering on Mall Customers data to derive meaningful business insights.  
It showcased an **end-to-end data analysis approach** with clear interpretations for anyone starting out in Data Analysis or Marketing Analytics.
""")

# Footer
st.markdown("---")
st.write("✅ **Developed by Soham Dharne.**")
