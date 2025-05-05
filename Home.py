# File: Home.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Soil Moisture Dashboard", layout="wide")

st.title("🌱 Soil Moisture Prediction Dashboard")
st.markdown("""
Welcome to the Soil Moisture Prediction Dashboard. This project involves analysis of three key target variables:

* **Surface Soil Moisture**
* **Root Zone Soil Moisture**
* **Total Soil Moisture**

Each target variable has been analyzed using various machine learning and deep learning models.
""")

# --- Model Performance Section ---
st.header("🏆 Model Performance Comparison")

# Create tabs for each soil moisture type
tab1, tab2, tab3 = st.tabs(["Surface Soil Moisture", "Root Zone Soil Moisture", "Total Soil Moisture"])

with tab1:
    # Surface Soil Moisture
    model_data = pd.DataFrame({
        'Model': ['XGBoost', 'Gradient Boosting', 'Random Forest', 'Decision Tree', 
                'Linear Regression', 'CNN-LSTM', 'LSTM', 'CNN-GRU', 'CNN 1D'],
        'RMSE': [0.03359, 0.03649, 0.05272, 0.05309, 0.07063, 0.04525, 0.24283, 0.04335, 0.05829],
        'R²': [0.91766, 0.90287, 0.82486, 0.79442, 0.63607, 0.90377, 0.85773, 0.88479, 0.81874]
    })
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(model_data.style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'}), 
                    use_container_width=True)
    with col2:
        fig = px.bar(model_data, x='Model', y='R²', 
                    title='Surface Soil Moisture - Model Performance (R² Score)',
                    color='Model',
                    color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Root Zone Soil Moisture
    model_data = pd.DataFrame({
        'Model': ['XGBoost', 'Gradient Boosting', 'Random Forest', 'Decision Tree', 
                'Linear Regression', 'CNN-LSTM', 'LSTM', 'CNN-GRU', 'CNN 1D'],
        'RMSE': [0.03132, 0.03421, 0.05028, 0.05258, 0.06915, 0.03604, 0.22437, 0.04940, 0.04881],
        'R²': [0.90477, 0.88641, 0.75459, 0.73157, 0.53577, 0.89259, 0.87811, 0.88335, 0.87635]
    })
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(model_data.style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'}), 
                    use_container_width=True)
    with col2:
        fig = px.bar(model_data, x='Model', y='R²', 
                    title='Root Zone Soil Moisture - Model Performance (R² Score)',
                    color='Model',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Total Soil Moisture
    model_data = pd.DataFrame({
        'Model': ['XGBoost', 'Gradient Boosting', 'Random Forest', 'Decision Tree', 
                'Linear Regression', 'CNN-LSTM', 'LSTM', 'CNN-GRU', 'CNN 1D'],
        'RMSE': [0.02694, 0.02991, 0.06261, 0.04772, 0.06615, 0.06882, 0.24355, 0.06271, 0.05595],
        'R²': [0.91110, 0.89046, 0.79556, 0.72112, 0.46417, 0.89974, 0.83889, 0.87385, 0.85728]
    })
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(model_data.style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'}), 
                    use_container_width=True)
    with col2:
        fig = px.bar(model_data, x='Model', y='R²', 
                    title='Total Soil Moisture - Model Performance (R² Score)',
                    color='Model',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

# --- Clustering Analysis Section ---
st.header("📦 Clustering Analysis")

# Create tabs for clustering results
tab1, tab2, tab3 = st.tabs(["Surface Soil Moisture", "Root Zone Soil Moisture", "Total Soil Moisture"])

with tab1:
    cluster_data = pd.DataFrame({
        'Clustering Method': ['Hierarchical', 'GMM', 'HMM', 'K-Shape', 'TimeSeriesKMeans'],
        'Silhouette Score': [0.3016, 0.4127, 0.2494, 0.0932, 0.3039]
    })
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(cluster_data.style.format({'Silhouette Score': '{:.4f}'}), 
                    use_container_width=True)
    with col2:
        fig = px.bar(cluster_data, x='Clustering Method', y='Silhouette Score',
                    title='Surface Soil Moisture - Clustering Performance',
                    color='Clustering Method',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    cluster_data = pd.DataFrame({
        'Clustering Method': ['Hierarchical', 'GMM', 'HMM', 'K-Shape', 'TimeSeriesKMeans'],
        'Silhouette Score': [0.3016, 0.5211, 0.2842, -0.0544, 0.3466]
    })
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(cluster_data.style.format({'Silhouette Score': '{:.4f}'}), 
                    use_container_width=True)
    with col2:
        fig = px.bar(cluster_data, x='Clustering Method', y='Silhouette Score',
                    title='Root Zone Soil Moisture - Clustering Performance',
                    color='Clustering Method')
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    cluster_data = pd.DataFrame({
        'Clustering Method': ['Hierarchical', 'GMM', 'HMM', 'K-Shape', 'TimeSeriesKMeans'],
        'Silhouette Score': [0.3025, 0.4226, 0.3089, -0.0452, 0.2984]
    })
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(cluster_data.style.format({'Silhouette Score': '{:.4f}'}), 
                    use_container_width=True)
    with col2:
        fig = px.bar(cluster_data, x='Clustering Method', y='Silhouette Score',
                    title='Total Soil Moisture - Clustering Performance',
                    color='Clustering Method')
        st.plotly_chart(fig, use_container_width=True)

# --- Navigation ---
st.sidebar.title("Navigation")
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/1_surface_analysis.py", label="🔵 Detailed Surface Analysis")
st.sidebar.page_link("pages/2_root_zone_analysis.py", label="🟢 Detailed Root Zone Analysis")
st.sidebar.page_link("pages/3_total_analysis.py", label="🟠 Detailed Total Analysis")
st.sidebar.page_link("pages/5_cluster_analysis.py", label="📦 Advanced Clustering Analysis")

# Footer
st.markdown("---")
st.markdown("""
**Note:** Use the sidebar to navigate to detailed analysis pages for each soil moisture type.
""")