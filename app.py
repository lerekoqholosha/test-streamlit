import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Takelot vs Makro Comparison", layout="wide")
st.title("📊 Takelot vs Makro Product Comparison")

# --- Hardcoded Product Data ---
takelot_data = [
    {"Product": "Laptop X", "Category": "Electronics", "Price": 1200, "Stock": 15},
    {"Product": "Smartphone Y", "Category": "Electronics", "Price": 800, "Stock": 30},
    {"Product": "Office Chair", "Category": "Furniture", "Price": 150, "Stock": 20},
    {"Product": "Notebook", "Category": "Stationery", "Price": 5, "Stock": 100},
]

makro_data = [
    {"Product": "Laptop X", "Category": "Electronics", "Price": 1150, "Stock": 10},
    {"Product": "Smartphone Y", "Category": "Electronics", "Price": 820, "Stock": 25},
    {"Product": "Office Chair", "Category": "Furniture", "Price": 140, "Stock": 15},
    {"Product": "Notebook", "Category": "Stationery", "Price": 6, "Stock": 120},
]

takelot_df = pd.DataFrame(takelot_data)
makro_df = pd.DataFrame(makro_data)

# --- Show Tables Side by Side ---
st.subheader("Product Data")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Takelot**")
    st.dataframe(takelot_df)
with col2:
    st.markdown("**Makro**")
    st.dataframe(makro_df)

# --- Merge for Comparison ---
comparison_df = pd.merge(
    takelot_df, makro_df, on="Product", suffixes=("_Takelot", "_Makro")
)
comparison_df["Price Difference"] = comparison_df["Price_Takelot"] - comparison_df["Price_Makro"]
comparison_df["Stock Difference"] = comparison_df["Stock_Takelot"] - comparison_df["Stock_Makro"]

st.subheader("Comparison")
st.dataframe(comparison_df)

# --- Visualizations ---
st.subheader("📉 Price Difference per Product")
plt.figure(figsize=(10,5))
sns.barplot(
    x="Product",
    y="Price Difference",
    data=comparison_df,
    palette="coolwarm"
)
plt.axhline(0, color='gray', linestyle='--')
plt.ylabel("Takelot Price - Makro Price")
st.pyplot(plt)

st.subheader("📦 Stock Difference per Product")
plt.figure(figsize=(10,5))
sns.barplot(
    x="Product",
    y="Stock Difference",
    data=comparison_df,
    palette="viridis"
)
plt.axhline(0, color='gray', linestyle='--')
plt.ylabel("Takelot Stock - Makro Stock")
st.pyplot(plt)

# --- Export Option ---
if st.button("Export Comparison CSV"):
    comparison_df.to_csv("product_comparison.csv", index=False)
    st.success("✅ Comparison exported as product_comparison.csv")
