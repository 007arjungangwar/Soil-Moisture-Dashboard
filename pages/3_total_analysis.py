import streamlit as st
import os
from PIL import Image
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="Total Soil Moisture Analysis",
    page_icon="💧"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main headers */
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #1a5276;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #3498db;
    }
    
    /* Section headers */
    .section-header {
        font-size: 22px;
        font-weight: 600;
        color: #2874a6;
        margin: 20px 0 12px 0;
    }
    
    /* Subsection headers */
    .subsection-header {
        font-size: 18px;
        font-weight: 500;
        color: #3498db;
        margin: 15px 0 10px 0;
    }
    
    /* Cards for visualizations */
    .visual-card {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        padding: 16px;
        margin-bottom: 24px;
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
    }
    
    /* Image captions */
    .image-caption {
        font-size: 14px;
        text-align: center;
        color: #5d6d7e;
        margin-top: 8px;
        font-style: italic;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        padding: 8px 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        background-color: #ebf5fb;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #d6eaf8;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: 500;
        color: #2874a6;
    }
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown('<div class="main-header">💧 Total Soil Moisture Analysis</div>', unsafe_allow_html=True)

# Introduction card
with st.container():
    st.markdown("""
    <div style="background-color:#eaf2f8; padding:20px; border-radius:12px; margin-bottom:25px;">
        <p style="font-size:16px; color:#154360;">
        This dashboard provides comprehensive insights into total soil moisture patterns, 
        model performance, and feature importance across different temporal and spatial scales.
        Analyze how different models perform and understand the key drivers of soil moisture variability.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Image directory
image_dir = f"images/total"

def show_image(file, caption, col=None):
    path = os.path.join(image_dir, file)
    if os.path.exists(path):
        img = Image.open(path)
        if col:
            with col:
                st.markdown(f'<div class="visual-card">', unsafe_allow_html=True)
                st.image(img, use_column_width=True)
                st.markdown(f'<p class="image-caption">{caption}</p>', unsafe_allow_html=True)
                st.markdown(f'</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="visual-card">', unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.markdown(f'<p class="image-caption">{caption}</p>', unsafe_allow_html=True)
            st.markdown(f'</div>', unsafe_allow_html=True)
    else:
        st.warning(f"Image not found: {file}")

# Model Performance Summary Section
with st.container():
    st.markdown('<div class="section-header">📊 Model Performance Summary</div>', unsafe_allow_html=True)
    
    # Performance data - replace with your actual metrics
    model_data = {
        "Model": ["XGBoost", "Gradient Boosting", "Random Forest", 
                 "Decision Tree", "Linear Regression", "CNN-LSTM"],
        "RMSE": [0.02694, 0.02991, 0.06261, 0.04772, 0.06615, 0.06882],
        "R²": [0.91110, 0.89046, 0.79556, 0.72112, 0.46417, 0.89974]
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="subsection-header">Performance Metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(model_data)
            .style.format({'RMSE': '{:.5f}', 'R²': '{:.5f}'})
            .highlight_max(subset=['R²'], color='#d5f5e3')
            .highlight_min(subset=['RMSE'], color='#d5f5e3')
            .set_properties(**{'background-color': '#f8f9fa', 'border': '1px solid #dee2e6'}),
            use_container_width=True,
            height=300
        )
    
    with col2:
        st.markdown('<div class="subsection-header">Performance Visualization</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["R² Score", "RMSE"])
        
        with tab1:
            fig = px.bar(
                pd.DataFrame(model_data),
                x='Model', 
                y='R²',
                color='Model',
                text='R²',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template='plotly_white'
            )
            fig.update_traces(
                texttemplate='%{text:.3f}', 
                textposition='outside',
                marker_line_color='rgb(8,48,107)',
                marker_line_width=1
            )
            fig.update_layout(
                showlegend=False, 
                yaxis_title="R² Score",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_column_width=True)
        
        with tab2:
            fig = px.bar(
                pd.DataFrame(model_data),
                x='Model', 
                y='RMSE',
                color='Model',
                text='RMSE',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template='plotly_white'
            )
            fig.update_traces(
                texttemplate='%{text:.4f}', 
                textposition='outside',
                marker_line_color='rgb(8,48,107)',
                marker_line_width=1
            )
            fig.update_layout(
                showlegend=False, 
                yaxis_title="RMSE",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_column_width=True)

# XGBoost Monthly Performance Section
with st.container():
    st.markdown('<div class="section-header">📅 XGBoost Monthly Performance</div>', unsafe_allow_html=True)
    
    monthly_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Mean"],
        "RMSE": [0.02361, 0.02271, 0.02156, 0.0211, 0.02315, 0.02509,
                0.0305, 0.03109, 0.03017, 0.02582, 0.02456, 0.02572, 0.0254],
        "R²": [0.91031, 0.91371, 0.92066, 0.92892, 0.91878, 0.91649,
              0.89804, 0.8973, 0.90285, 0.92343, 0.9166, 0.8967, 0.912]
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
                yaxis_range=[0.88, 0.94]  # Adjusted for better visualization
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
                texttemplate='%{text:.4f}', 
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="RMSE",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.02, 0.032]  # Adjusted for better visualization
            )
            st.plotly_chart(fig, use_container_width=True)

# XGBoost Yearly Performance Section
with st.container():
    st.markdown('<div class="section-header">📅 XGBoost Yearly Performance</div>', unsafe_allow_html=True)
    
    yearly_data = {
        "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, "Mean"],
        "RMSE": [0.0381, 0.03999, 0.03469, 0.03465, 0.03447, 0.03943, 
                0.03612, 0.03342, 0.03539, 0.03272, 0.0359],
        "R²": [0.7895, 0.78494, 0.84115, 0.83321, 0.85489, 0.80275,
              0.83417, 0.84762, 0.83013, 0.84774, 0.8266]
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
                yaxis_range=[0.75, 0.88]  # Adjusted for better visualization
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
                texttemplate='%{text:.4f}', 
                textposition='top center',
                line_width=2
            )
            fig.update_layout(
                yaxis_title="RMSE",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0.03, 0.042]  # Adjusted for better visualization
            )
            st.plotly_chart(fig, use_container_width=True)

# Main Analysis Tabs
tab_names = [
    "📊 Feature Importance", 
    "📈 Actual vs. Predicted", 
    "🗓️ Yearly Patterns", 
    "📅 Monthly Patterns",
    "🔍 Model Interpretation", 
    "🌍 Spatial Analysis"
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_names)

with tab1:
    st.markdown('<div class="section-header">Feature Importance Analysis</div>', unsafe_allow_html=True)
    
    models = [
        ("Linear Regression", "linear_regression"),
        ("Decision Tree", "decision_tree"),
        ("Random Forest", "random_forest"),
        ("Gradient Boosting", "gradient_boosting"),
        ("XGBoost", "xgboost")
    ]
    
    for model_name, model_key in models:
        with st.expander(f"### {model_name}", expanded=False):
            cols = st.columns(2)
            show_image(f"{model_key}_importance.png", f"{model_name} Feature Importance", cols[0])
            show_image(f"{model_key}_importance_%_pie_chart.png", f"{model_name} Feature Contribution", cols[1])

with tab2:
    st.markdown('<div class="section-header">Model Validation</div>', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">Actual vs. Predicted Values (XGBoost)</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="section-header">Temporal Analysis - Yearly Patterns</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    show_image("top15_yearly_bar.png", "Top 15 Features (Bar Chart)", cols[0])
    show_image("top10_yearly_pie.png", "Top 10 Features (Pie Chart)", cols[1])
    
    cols = st.columns(2)
    show_image("yearly_heatmap.png", "Feature Importance Heatmap", cols[0])
    show_image("yearly_stacked_bar.png", "Top Feature Contributions", cols[1])

with tab4:
    st.markdown('<div class="section-header">Temporal Analysis - Monthly Patterns</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    show_image("top15_monthly_bar.png", "Top 15 Features (Bar Chart)", cols[0])
    show_image("top10_monthly_pie.png", "Top 10 Features (Pie Chart)", cols[1])
    
    cols = st.columns(2)
    show_image("monthly_heatmap.png", "Feature Importance Heatmap", cols[0])
    show_image("monthly_stacked_bar.png", "Top Feature Contributions", cols[1])

with tab5:
    st.markdown('<div class="section-header">Model Interpretation</div>', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">SHAP Value Analysis</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    show_image("shap_with_10year_Summary_Plot.png", "SHAP Summary Plot (10 Years)", cols[0])
    show_image("shap_with_10year_Waterfall_Plot.png", "SHAP Waterfall Plot (10 Years)", cols[1])
    
    st.markdown('<div class="subsection-header">Temporal SHAP Patterns</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    show_image("shap_yearly.png", "Yearly SHAP Values", cols[0])
    show_image("shap_monthly.png", "Monthly SHAP Values", cols[1])

with tab6:
    st.markdown('<div class="section-header">Spatial Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">Grid-wise Model Performance</div>', unsafe_allow_html=True)
    
    models = [
        ("XGBoost", "Grid_wise_Plot_XGboost"),
        ("Gradient Boosting", "Grid_wise_Plot_GBR"),
        ("Random Forest", "Grid_wise_Plot_RF"),
        ("Decision Tree", "Grid_wise_Plot_DT"),
        ("Linear Regression", "Grid_wise_Plot_LR")
    ]
    
    for model_name, model_key in models:
        with st.expander(f"### {model_name} Spatial Performance", expanded=False):
            show_image(f"{model_key} R2score Performance (total_soil_moisture).png", 
                      f"{model_name} R² Spatial Distribution")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #5d6d7e; font-size: 14px; padding: 15px 0;">
    Total Soil Moisture Analysis Dashboard | Created with Streamlit | <span style="color:#3498db;">Soil Science Analytics</span>
</div>
""", unsafe_allow_html=True)