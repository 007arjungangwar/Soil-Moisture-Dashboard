import streamlit as st
import os
from PIL import Image
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(layout="wide", page_title="Root Zone Soil Moisture Analysis")

# Custom CSS for better styling
st.markdown("""
<style>
    .header-style {
        font-size: 24px;
        font-weight: bold;
        color: #2e86ab;
        margin-bottom: 10px;
    }
    .subheader-style {
        font-size: 20px;
        font-weight: bold;
        color: #3a7ca5;
        margin-bottom: 8px;
    }
    .card {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f8f9fa;
    }
    .image-caption {
        font-size: 14px;
        text-align: center;
        color: #6c757d;
        margin-top: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        background-color: #e9ecef;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #dee2e6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2e86ab;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Page Header
st.title("🌱 Root Zone Soil Moisture Analysis")
st.markdown("""
<div style="background-color:#e8f4f8; padding:15px; border-radius:10px; margin-bottom:20px;">
    <p style="font-size:16px;">This dashboard provides comprehensive analysis of root zone soil moisture patterns, 
    model performance, and feature importance across different temporal and spatial scales.</p>
</div>
""", unsafe_allow_html=True)

# Image directory
image_dir = f"images/root_zone"

def show_image(file, caption, col=None):
    path = os.path.join(image_dir, file)
    if os.path.exists(path):
        img = Image.open(path)
        if col:
            with col:
                st.image(img, caption=caption, use_column_width=True)
                st.markdown(f'<p class="image-caption">{caption}</p>', unsafe_allow_html=True)
        else:
            st.image(img, caption=caption, use_column_width=True)
            st.markdown(f'<p class="image-caption">{caption}</p>', unsafe_allow_html=True)
    else:
        st.warning(f"Image not found: {file}")

# Model Performance Summary Card
with st.container():
    st.markdown('<div class="header-style">📊 Model Performance Summary</div>', unsafe_allow_html=True)
    
    # Sample data - replace with your actual model performance metrics
    model_data = {
        "Model": ["XGBoost", "Gradient Boosting", "Random Forest", "Decision Tree", "Linear Regression"],
        "RMSE": [0.03132, 0.03421, 0.05028, 0.05258, 0.06915],
        "R²": [0.90477, 0.88641, 0.75459, 0.73157, 0.53577]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="subheader-style">Performance Metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(model_data)
            .style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'})
            .highlight_max(subset=['R²'], color='#d4edda')
            .highlight_min(subset=['RMSE'], color='#d4edda'),
            use_container_width=True
        )
    
    with col2:
        st.markdown('<div class="subheader-style">R² Score Comparison</div>', unsafe_allow_html=True)
        fig = px.bar(
            pd.DataFrame(model_data),
            x='Model', 
            y='R²',
            color='Model',
            text='R²',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(showlegend=False, yaxis_title="R² Score")
        st.plotly_chart(fig, use_column_width=True)

# XGBoost Monthly Performance Section - Root Zone Soil Moisture
with st.container():
    st.markdown('<div class="section-header">📅 XGBoost Monthly Performance (Root Zone Soil Moisture)</div>', unsafe_allow_html=True)
    
    monthly_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Mean"],
        "RMSE": [0.02517, 0.0234, 0.02182, 0.02261, 0.02765, 0.0335,
                0.04522, 0.03431, 0.03085, 0.02935, 0.02825, 0.02808, 0.0292],
        "R²": [0.8715, 0.8927, 0.9163, 0.9267, 0.9065, 0.8949,
              0.8155, 0.8644, 0.8878, 0.888, 0.863, 0.8548, 0.8818]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="subsection-header">Monthly Metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(monthly_data)
            .style.format({'RMSE': '{:.5f}', 'R²': '{:.4f}'})  # Adjusted decimal places
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
                yaxis_range=[0.8, 0.94]  # Adjusted range for root zone moisture
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
                texttemplate='%{text:.5f}', 
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="RMSE",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.02, 0.047]  # Adjusted range for root zone moisture
            )
            st.plotly_chart(fig, use_container_width=True)

# XGBoost Yearly Performance Section - Root Zone Soil Moisture
with st.container():
    st.markdown('<div class="section-header">📅 XGBoost Yearly Performance (Root Zone Soil Moisture)</div>', unsafe_allow_html=True)
    
    yearly_data = {
        "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, "Mean"],
        "RMSE": [0.04654, 0.04667, 0.04548, 0.04418, 0.04526, 0.04891, 
                0.04634, 0.04423, 0.04557, 0.04176, 0.0455],
        "R²": [0.6731, 0.6281, 0.7047, 0.6821, 0.7195, 0.6516,
              0.6851, 0.6745, 0.6583, 0.7201, 0.6797]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="subsection-header">Yearly Metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(yearly_data)
            .style.format({'RMSE': '{:.5f}', 'R²': '{:.4f}'})  # Adjusted decimal places
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
                yaxis_range=[0.6, 0.75]  # Adjusted range for root zone moisture
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
                yaxis_range=[0.04, 0.05]  # Adjusted range for root zone moisture
            )
            st.plotly_chart(fig, use_container_width=True)
            
# Main Analysis Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Feature Importance", 
    "📈 Actual vs. Predicted", 
    "🗓️ Yearly Analysis", 
    "📅 Monthly Analysis",
    "🔍 SHAP Interpretation", 
    "🌐 Spatial Patterns"
])

with tab1:
    st.markdown('<div class="header-style">Feature Importance Analysis</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="header-style">Actual vs. Predicted Values</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subheader-style">XGBoost Model Performance</div>', unsafe_allow_html=True)
    feature_sets = [
        ("All Features", "xgboost_actual_vs_pred_28.png"),
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
    st.markdown('<div class="header-style">Yearly Feature Patterns</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    show_image("top15_yearly_bar.png", "Top 15 Features - Bar Chart", cols[0])
    show_image("top10_yearly_pie.png", "Top 10 Features - Pie Chart", cols[1])
    
    cols = st.columns(2)
    show_image("yearly_heatmap.png", "Yearly Feature Importance Heatmap", cols[0])
    show_image("yearly_stacked_bar.png", "Top 10 Feature Contributions", cols[1])

with tab4:
    st.markdown('<div class="header-style">Monthly Feature Patterns</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    show_image("top15_monthly_bar.png", "Top 15 Features - Bar Chart", cols[0])
    show_image("top10_monthly_pie.png", "Top 10 Features - Pie Chart", cols[1])
    
    cols = st.columns(2)
    show_image("monthly_heatmap.png", "Monthly Feature Importance Heatmap", cols[0])
    show_image("monthly_stacked_bar.png", "Top 10 Feature Contributions", cols[1])

with tab5:
    st.markdown('<div class="header-style">SHAP Value Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subheader-style">Model Interpretability</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    show_image("shap_with_10year_Summary_Plot.png", "SHAP Summary Plot (10 Years)", cols[0])
    show_image("shap_with_10year_Waterfall_Plot.png", "SHAP Waterfall Plot (10 Years)", cols[1])
    
    st.markdown('<div class="subheader-style">Temporal Patterns</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    show_image("shap_yearly.png", "Yearly SHAP Values", cols[0])
    show_image("shap_monthly.png", "Monthly SHAP Values", cols[1])

with tab6:
    st.markdown('<div class="header-style">Spatial Performance Patterns</div>', unsafe_allow_html=True)
    
    models = [
        ("XGBoost", "Grid_wise_Plot_XGboost"),
        ("Gradient Boosting", "Grid_wise_Plot_GBR"),
        ("Random Forest", "Grid_wise_Plot_RF"),
        ("Decision Tree", "Grid_wise_Plot_DT"),
        ("Linear Regression", "Grid_wise_Plot_LR")
    ]
    
    for model_name, model_key in models:
        with st.expander(f"### {model_name} Spatial Performance", expanded=True):
            show_image(f"{model_key} R2score Performance (root_zone_soil_moisture).png", 
                      f"{model_name} R² Spatial Distribution")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 14px;">
    Root Zone Soil Moisture Analysis Dashboard | Created with Streamlit
</div>
""", unsafe_allow_html=True)