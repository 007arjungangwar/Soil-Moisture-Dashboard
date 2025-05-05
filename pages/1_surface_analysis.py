import streamlit as st
import os
from PIL import Image
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(layout="wide", page_title="Soil Moisture Analysis")

# Set the target variable context for this page
target = "surface"  # change to "root_zone" or "total" in other pages
title_map = {
    "surface": "🌱 Surface Soil Moisture Analysis",
    "root_zone": "🌿 Root Zone Soil Moisture Analysis", 
    "total": "💧 Total Soil Moisture Analysis"
}
st.title(title_map[target])

# Custom CSS for better spacing
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px 4px 0 0;
    }
    .stImage {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .model-card {
        padding: 1rem;
        border-radius: 8px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

image_dir = f"images/{target}"

def show_image(file, caption, col=None):
    path = os.path.join(image_dir, file)
    if os.path.exists(path):
        img = Image.open(path)
        if col:
            with col:
                st.image(img, caption=caption, use_column_width=True)
        else:
            st.image(img, caption=caption, use_column_width=True)
    else:
        st.warning(f"Image not found: {file}")

# Model performance data (example - replace with your actual data)
model_performance = {
    "Model": ["XGBoost", "Gradient Boosting", "Random Forest", "Decision Tree", "Linear Regression"],
    "RMSE": [0.0336, 0.0365, 0.0527, 0.0531, 0.0706],
    "R²": [0.9177, 0.9029, 0.8249, 0.7944, 0.6361]
}

# Performance Summary at the top
with st.container():
    st.header("📊 Model Performance Summary")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(
            pd.DataFrame(model_performance)
            .style.format({'RMSE': '{:.4f}', 'R²': '{:.4f}'})
            .highlight_max(subset=['R²'], color='#d4edda')
            .highlight_min(subset=['RMSE'], color='#d4edda'),
            use_container_width=True
        )
    
    with col2:
        fig = px.bar(
            pd.DataFrame(model_performance),
            x='Model', 
            y='R²',
            title='Model Performance (R² Score)',
            color='Model',
            text='R²',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        st.plotly_chart(fig, use_column_width=True)

# XGBoost Monthly Performance Section - Surface Soil Moisture
with st.container():
    st.markdown('<div class="section-header">📅 XGBoost Monthly Performance (Surface Soil Moisture)</div>', unsafe_allow_html=True)
    
    monthly_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Mean"],
        "RMSE": [0.042857, 0.031591, 0.030722, 0.027974, 0.032437, 0.032745,
                0.027635, 0.027368, 0.029675, 0.032624, 0.035653, 0.037435, 0.0324],
        "R²": [0.748952, 0.870841, 0.886332, 0.913114, 0.905789, 0.925801,
              0.92377, 0.927474, 0.925191, 0.915619, 0.866626, 0.844909, 0.8879]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="subsection-header">Monthly Metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(monthly_data)
            .style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'})
            .highlight_max(subset=['R²'], color='#d5f5e3')
            .highlight_min(subset=['RMSE'], color='#d5f5e3')
            .set_properties(**{'background-color': '#f8f9fa', 'border': '1px solid #dee2e6'})
        )
    
    with col2:
        st.markdown('<div class="subsection-header">Monthly Performance Trends</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["R² Score", "RMSE"])
        
        with tab1:
            fig = px.line(
                pd.DataFrame(monthly_data).iloc[:-1],  # Exclude mean row
                x='Month', 
                y='R²',
                markers=True,
                text='R²',
                color_discrete_sequence=['#3498db'],
                template='plotly_white'
            )
            fig.update_traces(
                texttemplate='%{text:.3f}', 
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="R² Score",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.7, 0.95]  # Adjusted range for surface soil moisture
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = px.line(
                pd.DataFrame(monthly_data).iloc[:-1],  # Exclude mean row
                x='Month', 
                y='RMSE',
                markers=True,
                text='RMSE',
                color_discrete_sequence=['#e74c3c'],
                template='plotly_white'
            )
            fig.update_traces(
                texttemplate='%{text:.5f}',  # More decimal places for RMSE
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="RMSE",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.025, 0.045]  # Adjusted range for surface soil moisture
            )
            st.plotly_chart(fig, use_container_width=True)

# XGBoost Yearly Performance Section - Surface Soil Moisture
with st.container():
    st.markdown('<div class="section-header">📅 XGBoost Yearly Performance (Surface Soil Moisture)</div>', unsafe_allow_html=True)
    
    yearly_data = {
        "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, "Mean"],
        "RMSE": [0.06259, 0.047557, 0.047202, 0.049984, 0.055594, 0.068118, 
                0.056743, 0.071928, 0.052099, 0.048862, 0.0561],
        "R²": [0.596767, 0.693501, 0.764806, 0.714968, 0.713004, 0.513201,
              0.686846, 0.391223, 0.721574, 0.771139, 0.6567]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="subsection-header">Yearly Metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(yearly_data)
            .style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'})
            .highlight_max(subset=['R²'], color='#d5f5e3')
            .highlight_min(subset=['RMSE'], color='#d5f5e3')
            .set_properties(**{'background-color': '#f8f9fa', 'border': '1px solid #dee2e6'})
        )
    
    with col2:
        st.markdown('<div class="subsection-header">Yearly Performance Trends</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["R² Score", "RMSE"])
        
        with tab1:
            fig = px.line(
                pd.DataFrame(yearly_data).iloc[:-1],  # Exclude mean row
                x='Year', 
                y='R²',
                markers=True,
                text='R²',
                color_discrete_sequence=['#3498db'],
                template='plotly_white'
            )
            fig.update_traces(
                texttemplate='%{text:.3f}', 
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="R² Score",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.35, 0.8]  # Adjusted range for surface soil moisture
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = px.line(
                pd.DataFrame(yearly_data).iloc[:-1],  # Exclude mean row
                x='Year', 
                y='RMSE',
                markers=True,
                text='RMSE',
                color_discrete_sequence=['#e74c3c'],
                template='plotly_white'
            )
            fig.update_traces(
                texttemplate='%{text:.5f}', 
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="RMSE",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.045, 0.075]  # Adjusted range for surface soil moisture
            )
            st.plotly_chart(fig, use_container_width=True)

            
# Tabs for detailed analysis
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Feature Importance", 
    "📈 Actual vs. Predicted", 
    "🗓️ Yearly Features", 
    "📅 Monthly Features",
    "🔍 SHAP Analysis", 
    "🌐 Grid-wise Performance" 
])

with tab1:
    st.header("Feature Importance by Models")
    
    models = [
        ("Linear Regression", "linear_regression"),
        ("Decision Tree", "decision_tree"),
        ("Random Forest", "random_forest"),
        ("Gradient Boosting", "gradient_boosting"),
        ("XGBoost", "xgboost")
    ]
    
    for model_name, model_key in models:
        with st.expander(f"### {model_name}", expanded=True):
            cols = st.columns(2)
            show_image(f"{model_key}_importance.png", f"{model_name} Feature Importance", cols[0])
            show_image(f"{model_key}_importance_%_pie_chart.png", f"{model_name} Feature Contribution", cols[1])

with tab2:
    st.header("Actual vs. Predicted Values")
    
    st.subheader("XGBoost Model Performance with Different Feature Sets")
    feature_sets = [
        ("All 28 Features", "xgboost_actual_vs_pred_28.png"),
        ("Top 15 Features", "xgboost_actual_vs_pred_15.png"),
        ("Top 8 Features", "xgboost_actual_vs_pred_8.png"),
        ("Top 5 Features", "xgboost_actual_vs_pred_5.png"),
        ("Combined Analysis", "xgboost_actual_vs_pred_combined.png")
    ]
    
    for i in range(0, len(feature_sets), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(feature_sets):
                show_image(feature_sets[i+j][1], feature_sets[i+j][0], cols[j])

with tab3:
    st.header("Yearly Feature Analysis")
    
    st.subheader("Top Features Across Years (XGBoost)")
    cols = st.columns(2)
    show_image("top15_yearly_bar.png", "Top 15 Features - Bar Chart", cols[0])
    show_image("top10_yearly_pie.png", "Top 10 Features - Pie Chart", cols[1])
    
    st.subheader("Feature Importance Trends")
    cols = st.columns(2)
    show_image("yearly_heatmap.png", "Feature Importance Heatmap (Years)", cols[0])
    show_image("yearly_stacked_bar.png", "Top 10 Feature Contributions (Stacked Bar)", cols[1])

with tab4:
    st.header("Monthly Feature Analysis")
    
    st.subheader("Top Features Across Months (XGBoost)")
    cols = st.columns(2)
    show_image("top15_monthly_bar.png", "Top 15 Features - Bar Chart", cols[0])
    show_image("top10_monthly_pie.png", "Top 10 Features - Pie Chart", cols[1])
    
    st.subheader("Feature Importance Trends")
    cols = st.columns(2)
    show_image("monthly_heatmap.png", "Feature Importance Heatmap (Months)", cols[0])
    show_image("monthly_stacked_bar.png", "Top 10 Feature Contributions (Stacked Bar)", cols[1])

with tab5:
    st.header("SHAP Analysis")
    
    st.subheader("XGBoost Model Interpretability")
    cols = st.columns(2)
    show_image("shap_with_10year_Summary_Plot.png", "SHAP Summary Plot (10 Years Data)", cols[0])
    show_image("shap_with_10year_Waterfall_Plot.png", "SHAP Waterfall Plot (10 Years Data)", cols[1])
    
    st.subheader("Temporal SHAP Analysis")
    cols = st.columns(2)
    show_image("shap_yearly.png", "Yearly SHAP Values", cols[0])
    show_image("shap_monthly.png", "Monthly SHAP Values", cols[1])

with tab6:
    st.header("Grid-wise Performance Analysis")
    
    models = [
        ("XGBoost", "Grid_wise_Plot_XGboost"),
        ("Gradient Boosting", "Grid_wise_Plot_GBR"),
        ("Random Forest", "Grid_wise_Plot_RF"),
        ("Decision Tree", "Grid_wise_Plot_DT"),
        ("Linear Regression", "Grid_wise_Plot_LR")
    ]
    
    for model_name, model_key in models:
        with st.expander(f"### {model_name} Performance", expanded=True):
            show_image(f"{model_key} R2score Performance ({target}_soil_moisture).png", 
                     f"{model_name} R² Score Distribution")

# Footer
st.markdown("---")
st.caption("Soil Moisture Analysis Dashboard | Created with Streamlit")