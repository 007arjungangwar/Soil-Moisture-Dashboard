import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("🌍 Clustering Analysis - All India Region")

# Define main variables
target_variables = {
    "Surface Soil Moisture": {
        "scores": {
            "Hierarchical": 0.3016,
            "GMM": 0.4127,
            "HMM": 0.2494,
            "K-Shape": 0.0932,
            "TS-KMeans": 0.3039,
        },
        "xgboost": [
            ("Without Cluster", 0.0336, 0.91766),
            ("Cluster 0", 0.02389, 0.94181),
            ("Cluster 1", 0.02917, 0.91871),
            ("Cluster 2", 0.03181, 0.92861),
            ("Cluster 3", 0.03088, 0.89771),
        ],
        "folder": "surface"
    },
    "Root Zone Soil Moisture": {
        "scores": {
            "Hierarchical": 0.3016,
            "GMM": 0.5211,
            "HMM": 0.2842,
            "K-Shape": -0.0544,
            "TS-KMeans": 0.3466,
        },
        "xgboost": [
            ("Without Cluster", 0.03132, 0.90477),
            ("Cluster 0", 0.02572, 0.95751),
            ("Cluster 1", 0.02808, 0.89228),
            ("Cluster 2", 0.02728, 0.9492),
            ("Cluster 3", 0.03084, 0.88797),
        ],
        "folder": "root_zone"
    },
    "Total Soil Moisture": {
        "scores": {
            "Hierarchical": 0.3025,
            "GMM": 0.4226,
            "HMM": 0.3089,
            "K-Shape": -0.0452,
            "TS-KMeans": 0.2984,
        },
        "xgboost": [
            ("Without Cluster", 0.02694, 0.9111),
            ("Cluster 0", 0.02297, 0.93182),
            ("Cluster 1", 0.0194, 0.96853),
            ("Cluster 2", 0.02638, 0.89768),
            ("Cluster 3", 0.03061, 0.89561),
        ],
        "folder": "total"
    },
}

# Create tabs for each target variable
tabs = st.tabs(list(target_variables.keys()))

for tab, (variable, data) in zip(tabs, target_variables.items()):
    with tab:
        # Section 1: Clustering Performance
        st.header("📊 Clustering Performance")
        
        # Convert scores to dataframe for better visualization
        scores_df = pd.DataFrame.from_dict(data["scores"], orient='index', columns=['Silhouette Score'])
        scores_df = scores_df.reset_index().rename(columns={'index': 'Method'})
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(
                scores_df.style.format({'Silhouette Score': '{:.4f}'})
                .highlight_max(subset=['Silhouette Score'], color='#90EE90')
                .highlight_min(subset=['Silhouette Score'], color='#FFCCCB'),
                use_container_width=True
            )
        
        with col2:
            fig = px.bar(
                scores_df, 
                x='Method', 
                y='Silhouette Score',
                title=f'Silhouette Scores - {variable}',
                color='Method',
                text='Silhouette Score',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_column_width=True)
        
        # Section 2: Cluster Maps
        st.header("🗺️ India Cluster Maps")
        image_folder = f"images/{data['folder']}/"
        
        # Display cluster maps in columns
        cols = st.columns(3)
        for i in range(1, 6):
            img_path = os.path.join(image_folder, f"{variable.split('(')[0].strip().replace(' ', '_').lower()}_cluster_{i}.png")
            with cols[(i-1)%3]:
                st.image(img_path, caption=f"Cluster {i-1}" if i>1 else "All India", use_column_width=True)
        
        # Section 3: XGBoost Performance by Cluster
        st.header("⚡ XGBoost Performance by Cluster")
        
        # Convert xgboost data to dataframe
        xgb_df = pd.DataFrame(data["xgboost"], columns=['Cluster', 'RMSE', 'R²'])
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(
                xgb_df.style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'})
                .highlight_max(subset=['R²'], color='#90EE90')
                .highlight_min(subset=['RMSE'], color='#90EE90'),
                use_container_width=True
            )
        
        with col2:
            fig = px.bar(
                xgb_df, 
                x='Cluster', 
                y='R²',
                title=f'XGBoost R² by Cluster - {variable}',
                color='Cluster',
                text='R²',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            st.plotly_chart(fig, use_column_width=True)
        
        # Section 4: Feature Importance
        st.header("🔍 Feature Contribution Analysis")
        
        # Create tabs for each cluster's feature importance
        cluster_tabs = st.tabs([f"Cluster {i}" for i in range(1, 5)])
        
        for i, cluster_tab in enumerate(cluster_tabs, 1):
            with cluster_tab:
                col1, col2 = st.columns(2)
                bar_path = os.path.join(image_folder, f"{variable.split('(')[0].strip().replace(' ', '_').lower()}_feature_bar_cluster_{i}.png")
                pie_path = os.path.join(image_folder, f"{variable.split('(')[0].strip().replace(' ', '_').lower()}_feature_pie_cluster_{i}.png")
                
                with col1:
                    st.image(bar_path, caption=f"Feature Importance (Bar) - Cluster {i-1}", use_column_width=True)
                with col2:
                    st.image(pie_path, caption=f"Feature Contribution (Pie) - Cluster {i-1}", use_column_width=True)

        st.markdown("---")