import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Revenue Predictor",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .feature-card {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4ECDC4;
    }
    .success-card {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #FF6B6B, #C44D4D);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-card {
        background: linear-gradient(135deg, #45B7D1, #4A90E2);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .progress-bar {
        height: 20px;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(45deg, #4ECDC4, #45B7D1);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎬 Movie Revenue Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Predict your movie's box office success with AI-powered insights")

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Quick Guide")
    st.info("""
    **How it works:**
    - Enter your movie details
    - AI analyzes patterns from successful films
    - Get instant revenue predictions
    - Optimize your budget and strategy
    """)
    
    st.markdown("## 💡 Pro Tips")
    st.success("""
    • **Budget**: Most important factor
    • **Score**: Aim for 7.0+ for best results  
    • **Votes**: More votes = more popularity
    • **Runtime**: 90-150 minutes is optimal
    """)

# Model training
@st.cache_resource
def train_model():
    df = pd.read_csv("revised_datasets/output.csv")
    df_clean = df[df['gross'] > df['budget'] * 1.2]
    df_clean = df_clean[df_clean['budget'] > 100000]
    
    features = ['budget', 'score', 'votes', 'runtime', 'year']
    X = df_clean[features].fillna(df_clean[features].median())
    y = np.log1p(df_clean['gross'])
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X, y)
    
    return model, features

# Load model
model, feature_columns = train_model()

# Main form
with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎭 Movie Details")
        
        with st.form("movie_form"):
            # Movie Info
            name = st.text_input("🎬 Movie Title", value="Avatar: The New World")
            genre = st.selectbox("📀 Genre", 
                               ["Action", "Adventure", "Comedy", "Drama", "Sci-Fi", 
                                "Horror", "Romance", "Thriller", "Fantasy", "Animation"])
            director = st.text_input("🎥 Director", value="James Cameron")
            
            # Key Factors
            st.markdown("### 💰 Key Factors")
            
            budget = st.number_input("🎯 Production Budget ($)", 
                                   min_value=1000, 
                                   value=250000000,
                                   step=1000000)
            
            score = st.slider("⭐ Expected IMDb Score", 
                            1.0, 10.0, 8.5, 0.1)
            
            votes = st.number_input("👥 Expected Votes", 
                                  min_value=100, 
                                  value=50000,
                                  step=1000)
            
            runtime = st.slider("⏱️ Runtime (minutes)", 
                              60, 240, 150)
            
            year = st.number_input("📅 Release Year", 
                                 min_value=2000, 
                                 max_value=2030, 
                                 value=2024)
            
            # Submit button
            submitted = st.form_submit_button("🚀 Predict Revenue", use_container_width=True)

    with col2:
        st.markdown("### 📊 Live Preview")
        
        # Real-time preview card
        if budget > 0:
            preview_data = pd.DataFrame([{
                'budget': budget, 'score': score, 'votes': votes, 
                'runtime': runtime, 'year': year
            }])
            
            with st.spinner('Calculating preview...'):
                preview_pred = np.expm1(model.predict(preview_data)[0])
                preview_roi = ((preview_pred - budget) / budget * 100)
            
            # Preview card
            st.markdown(f"""
            <div class="prediction-card">
                <h3 style='color: white; margin-bottom: 1rem;'>🎯 Quick Preview</h3>
                <div class="metric-card">
                    <strong>Budget:</strong> ${budget:,.0f}
                </div>
                <div class="metric-card">
                    <strong>Est. Revenue:</strong> ${preview_pred:,.0f}
                </div>
                <div class="metric-card">
                    <strong>ROI:</strong> {preview_roi:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Feature impact visualization (without plotly)
            st.markdown("#### 📈 Feature Impact")
            
            # Budget impact
            budget_percent = min(budget / 500000000 * 100, 100)
            st.markdown("**Budget Impact**")
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {budget_percent}%"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Score impact
            score_percent = (score / 10) * 100
            st.markdown("**Quality Score**")
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {score_percent}%"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Votes impact
            votes_percent = min(votes / 100000 * 100, 100)
            st.markdown("**Popularity**")
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {votes_percent}%"></div>
            </div>
            """, unsafe_allow_html=True)

# Prediction results
if submitted:
    st.markdown("---")
    
    # Make final prediction
    input_data = pd.DataFrame([{
        'budget': budget, 'score': score, 'votes': votes, 
        'runtime': runtime, 'year': year
    }])
    
    with st.spinner('🔄 Generating detailed analysis...'):
        log_prediction = model.predict(input_data)
        predicted_revenue = np.expm1(log_prediction[0])
        roi = ((predicted_revenue - budget) / budget * 100)
    
    # Results header
    st.markdown(f'<h2 style="text-align: center; color: #4ECDC4;">🎊 Prediction Results for "{name}"</h2>', unsafe_allow_html=True)
    
    # Main results cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="prediction-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h4>💰 Investment</h4>
            <h2>${budget:,.0f}</h2>
            <p>Production Budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="prediction-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h4>🎯 Prediction</h4>
            <h2>${predicted_revenue:,.0f}</h2>
            <p>Estimated Revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        roi_color = "#4ECDC4" if roi > 0 else "#FF6B6B"
        st.markdown(f"""
        <div class="prediction-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h4>📈 Return</h4>
            <h2 style="color: {roi_color}">{roi:.1f}%</h2>
            <p>Return on Investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Revenue range and analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Revenue Classification")
        
        ranges = [
            (10000000, "Low Revenue (<= $10M)", "#FF6B6B"),
            (40000000, "Medium-Low Revenue ($10M - $40M)", "#FFA726"),
            (70000000, "Medium Revenue ($40M - $70M)", "#FFD93D"),
            (120000000, "Medium-High Revenue ($70M - $120M)", "#6BCF7F"),
            (200000000, "High Revenue ($120M - $200M)", "#4ECDC4"),
            (float('inf'), "Ultra High Revenue (>= $200M)", "#667eea")
        ]
        
        current_range = next((text for limit, text, color in ranges if predicted_revenue <= limit), ranges[-1][1])
        current_color = next((color for limit, text, color in ranges if predicted_revenue <= limit), ranges[-1][2])
        
        st.markdown(f"""
        <div class="feature-card" style="border-left-color: {current_color};">
            <h4 style="color: {current_color}; margin: 0;">{current_range}</h4>
            <p>Based on industry standards and historical data</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Success probability
        success_prob = min(max(score * 8 + (roi / 10), 0), 100)
        st.markdown("### 🎯 Success Probability")
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {success_prob}%"></div>
        </div>
        <p style="text-align: center; margin-top: 0.5rem;"><strong>{success_prob:.1f}%</strong> chance of success</p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔍 Success Analysis")
        
        if roi < 0:
            st.markdown("""
            <div class="warning-card">
                <h4>⚠️ Risk Alert</h4>
                <p>Predicted to lose money. Consider:</p>
                <ul>
                    <li>Reducing production budget</li>
                    <li>Improving movie quality</li>
                    <li>Increasing marketing efforts</li>
                    <li>Re-evaluating release strategy</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif roi > 200:
            st.markdown("""
            <div class="success-card">
                <h4>🎉 Blockbuster Potential</h4>
                <p>Excellent ROI expected! This project shows:</p>
                <ul>
                    <li>Strong investment opportunity</li>
                    <li>High profit margins</li>
                    <li>Franchise potential</li>
                    <li>Market leadership position</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-card">
                <h4>✅ Profitable Project</h4>
                <p>Positive ROI expected with:</p>
                <ul>
                    <li>Solid investment returns</li>
                    <li>Good market positioning</li>
                    <li>Sustainable business model</li>
                    <li>Growth potential</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("### 💡 Optimization Recommendations")
    
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    
    with rec_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Budget Optimization</h4>
            <p><strong>Optimal range:</strong> ${budget*0.8:,.0f} - ${budget*1.2:,.0f}</p>
            <ul>
                <li>Consider co-production deals</li>
                <li>Explore tax incentives</li>
                <li>Phase production if needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>⭐ Quality Focus</h4>
            <p><strong>Target score:</strong> 7.5+</p>
            <ul>
                <li>Invest in strong screenplay</li>
                <li>Hire experienced director</li>
                <li>Conduct test screenings</li>
                <li>Focus on character development</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📢 Marketing Strategy</h4>
            <p><strong>Votes target:</strong> {votes*2:,}+</p>
            <ul>
                <li>Social media campaign</li>
                <li>Early buzz generation</li>
                <li>Film festival participation</li>
                <li>Strategic release date</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🎬 Powered by AI • 📊 Trained on successful movies • 💡 Data-driven insights"
    "</div>",
    unsafe_allow_html=True
)