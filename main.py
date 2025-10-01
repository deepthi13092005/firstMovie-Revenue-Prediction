import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler

def train_model():
    # Load and clean data
    df = pd.read_csv("revised datasets/output.csv")
    df_clean = df[df['gross'] > df['budget'] * 1.2]
    df_clean = df_clean[df_clean['budget'] > 100000]
    
    # Simple features
    features = ['budget', 'score', 'votes', 'runtime', 'year']
    X = df_clean[features].fillna(df_clean[features].median())
    y = np.log1p(df_clean['gross'])
    
    # Train model
    model = xgb.XGBRegressor(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X, y)
    
    return model, features

def predict_movie(model, features):
    print("\n" + "="*50)
    print("🎬 MOVIE REVENUE PREDICTION TERMINAL")
    print("="*50)
    
    # Get input
    print("\nEnter Movie Details:")
    name = input("Movie Name: ")
    budget = float(input("Budget ($): "))
    score = float(input("Expected IMDb Score (1-10): "))
    votes = int(input("Expected Votes: "))
    runtime = int(input("Runtime (minutes): "))
    year = int(input("Release Year: "))
    
    # Prepare input
    input_data = pd.DataFrame([{
        'budget': budget,
        'score': score, 
        'votes': votes,
        'runtime': runtime,
        'year': year
    }])
    
    # Predict
    log_pred = model.predict(input_data)
    revenue = np.expm1(log_pred[0])
    
    # Display results
    print("\n" + "="*50)
    print("📊 PREDICTION RESULTS")
    print("="*50)
    print(f"Movie: {name}")
    print(f"Budget: ${budget:,.2f}")
    print(f"Predicted Revenue: ${revenue:,.2f}")
    print(f"ROI: {((revenue - budget) / budget * 100):.1f}%")
    
    # Revenue range
    if revenue <= 10000000:
        range_text = "Low Revenue (<= $10M)"
    elif revenue <= 40000000:
        range_text = "Medium-Low Revenue ($10M - $40M)"
    elif revenue <= 70000000:
        range_text = "Medium Revenue ($40M - $70M)"
    elif revenue <= 120000000:
        range_text = "Medium-High Revenue ($70M - $120M)"
    elif revenue <= 200000000:
        range_text = "High Revenue ($120M - $200M)"
    else:
        range_text = "Ultra High Revenue (>= $200M)"
    
    print(f"Revenue Range: {range_text}")
    
    # Analysis
    if revenue < budget:
        print("❌ Warning: Predicted to LOSE money!")
    elif revenue > budget * 3:
        print("✅ Excellent! Predicted to be VERY profitable!")
    else:
        print("✅ Predicted to be profitable!")

# Main program
if __name__ == "__main__":
    print("Training model... Please wait...")
    model, features = train_model()
    print("Model trained successfully!")
    
    while True:
        predict_movie(model, features)
        
        again = input("\nPredict another movie? (y/n): ").lower()
        if again != 'y':
            print("Thank you for using Movie Revenue Predictor!")
            break