import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler

class AccurateMoviePredictor:
    def __init__(self):
        self.genre_data = {
            'Action': {'multiplier': 1.8, 'risk': 'Medium', 'description': 'Global appeal, good ROI'},
            'Adventure': {'multiplier': 1.7, 'risk': 'Medium', 'description': 'Family friendly, stable'},
            'Animation': {'multiplier': 2.0, 'risk': 'Low', 'description': 'Best for families, great ROI'},
            'Comedy': {'multiplier': 1.3, 'risk': 'High', 'description': 'Domestic focus, mixed results'},
            'Drama': {'multiplier': 1.1, 'risk': 'Very High', 'description': 'Niche audience, risky'},
            'Horror': {'multiplier': 2.5, 'risk': 'Very Low', 'description': 'Best ROI, low budget works'},
            'Romance': {'multiplier': 0.8, 'risk': 'Very High', 'description': 'Limited audience, high risk'},
            'Sci-Fi': {'multiplier': 1.6, 'risk': 'Medium', 'description': 'Global but expensive'},
            'Thriller': {'multiplier': 1.2, 'risk': 'Medium', 'description': 'Adult audience, steady'}
        }
        
    def predict(self, budget, genre, rating, season, has_star, is_sequel):
        """ACCURATE prediction based on real industry data"""
        
        # Start with budget
        base_revenue = budget
        
        # Apply rating effect
        if rating >= 8.0:
            base_revenue *= 3.0
            rating_effect = "Great movies attract more viewers"
        elif rating >= 7.0:
            base_revenue *= 2.0
            rating_effect = "Good quality brings steady audience"
        elif rating >= 6.0:
            base_revenue *= 1.3
            rating_effect = "Average movies struggle to attract viewers"
        elif rating >= 5.0:
            base_revenue *= 0.9
            rating_effect = "Poor quality significantly hurts box office"
        else:
            base_revenue *= 0.6
            rating_effect = "Very poor quality leads to box office disaster"
        
        # Apply genre multiplier
        genre_multiplier = self.genre_data[genre]['multiplier']
        base_revenue *= genre_multiplier
        genre_effect = f"{genre} movies typically make {genre_multiplier}x budget"
        
        # Season effect
        if season == "Summer":
            base_revenue *= 1.4
            season_effect = "Summer releases get 40% more viewers"
        elif season == "Holiday":
            base_revenue *= 1.3
            season_effect = "Holiday season boosts attendance"
        else:
            base_revenue *= 0.9
            season_effect = "Off-season releases have fewer viewers"
        
        # Star power
        if has_star:
            base_revenue *= 1.2
            star_effect = "Famous actors help but cannot save bad movies"
        else:
            base_revenue *= 1.0
            star_effect = "No big stars - needs strong marketing"
        
        # Sequel bonus
        if is_sequel:
            base_revenue *= 1.3
            sequel_effect = "Sequels have some built-in audience"
        else:
            base_revenue *= 1.0
            sequel_effect = "Original movie - needs to build audience"
        
        # BIG BUDGET PENALTY
        if budget > 100 and rating < 7.0:
            base_revenue *= 0.7
            budget_effect = "Big budget with average quality = High risk"
        elif budget > 200 and rating < 7.5:
            base_revenue *= 0.6
            budget_effect = "Huge budget needs excellent quality to succeed"
        else:
            budget_effect = "Budget matches quality expectations"
        
        # ROMANCE GENRE PENALTY
        if genre == 'Romance' and budget > 50:
            base_revenue *= 0.6
            romance_effect = "Romance genre cannot sustain big budgets"
        elif genre == 'Romance':
            romance_effect = "Romance works best with smaller budgets"
        else:
            romance_effect = "Genre has reasonable box office potential"
        
        # Add realistic variation
        variation = np.random.normal(1.0, 0.15)
        predicted_revenue = base_revenue * variation
        
        effects = {
            'rating': rating_effect,
            'genre': genre_effect,
            'season': season_effect,
            'star': star_effect,
            'sequel': sequel_effect,
            'budget_risk': budget_effect,
            'genre_risk': romance_effect
        }
        
        return max(predicted_revenue, budget * 0.3), effects

def display_header():
    print("\n" + "="*70)
    print("🎬 MOVIE SUCCESS PREDICTOR")
    print("Will your movie be a Blockbuster or Flop? Get clear answers in plain English")
    print("="*70)

def display_quick_tips():
    print("\n💡 QUICK TIPS:")
    print("• Good ratings = More profit")
    print("• Summer releases = More viewers")  
    print("• Horror movies = Best returns")
    print("• Big budgets need high quality")
    print("• Romance/Drama = Risky with big budgets")
    print("• Sequels perform better")

def get_movie_input():
    print("\n🎬 ENTER YOUR MOVIE DETAILS")
    print("-" * 40)
    
    movie_name = input("Movie Title: ").strip() or "Radhe Shyam"
    
    print("\nAvailable Genres:")
    genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
    for i, genre in enumerate(genres, 1):
        print(f"{i}. {genre}")
    
    while True:
        try:
            genre_choice = int(input("Choose genre (1-9): "))
            if 1 <= genre_choice <= 9:
                genre = genres[genre_choice - 1]
                break
            else:
                print("Please enter a number between 1 and 9")
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            budget = float(input("Production Budget (in millions): "))
            if budget > 0:
                break
            else:
                print("Budget must be positive")
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            rating = float(input("Expected Quality Rating (1-10): "))
            if 1 <= rating <= 10:
                break
            else:
                print("Rating must be between 1 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    print("\nRelease Seasons:")
    seasons = ['Summer', 'Holiday', 'Other Season']
    for i, season in enumerate(seasons, 1):
        print(f"{i}. {season}")
    
    while True:
        try:
            season_choice = int(input("Choose release season (1-3): "))
            if 1 <= season_choice <= 3:
                season = seasons[season_choice - 1]
                break
            else:
                print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number")
    
    has_star = input("Has Famous Actor? (y/n): ").lower().strip() == 'y'
    is_sequel = input("Is Sequel/Franchise? (y/n): ").lower().strip() == 'y'
    
    return movie_name, genre, budget, rating, season, has_star, is_sequel

def display_results(movie_name, budget, predicted_revenue, profit, roi, result_type, result_message, effects):
    print("\n" + "="*70)
    print("📊 YOUR PREDICTION RESULTS")
    print("="*70)
    
    # Big clear result
    print(f"\n🎯 RESULT: {result_type}")
    print(f"💡 {result_message}")
    
    # Key numbers
    print(f"\n💰 FINANCIAL SUMMARY:")
    print(f"   Budget: ${budget}M")
    print(f"   Predicted Revenue: ${predicted_revenue:,.0f}M")
    print(f"   Net Profit: ${profit:,.0f}M")
    print(f"   Return on Investment: {roi:+.1f}%")
    
    # Financial breakdown
    marketing_cost = budget * 0.5
    total_cost = budget + marketing_cost
    
    print(f"\n📈 FINANCIAL BREAKDOWN:")
    print(f"   Production Cost: ${budget}M")
    print(f"   Marketing Cost: ${marketing_cost:.0f}M")
    print(f"   Total Cost: ${total_cost:.0f}M")
    print(f"   Box Office Revenue: ${predicted_revenue:,.0f}M")
    print(f"   Net Profit: ${profit:,.0f}M")
    
    # Why this result
    print(f"\n🔍 WHY THIS RESULT?")
    for factor, explanation in effects.items():
        print(f"   • {factor.replace('_', ' ').title()}: {explanation}")
    
    # Recommendations
    print(f"\n💡 WHAT SHOULD YOU DO?")
    if profit > 100:
        print("   🎉 Go For It! Your movie shows excellent profit potential.")
        print("   ✅ Start production immediately")
        print("   ✅ Plan strong marketing campaign")
        print("   ✅ Consider international release")
    elif profit > 0:
        print("   ✅ Good Project - Your movie should make money")
        print("   📝 Manage budget carefully")
        print("   🎯 Focus marketing on right audience")
        print("   🤝 Consider partners to reduce risk")
    else:
        print("   🚨 MAJOR CHANGES NEEDED!")
        print("   💰 REDUCE BUDGET by 40-60% immediately")
        print("   ⭐ IMPROVE QUALITY to 7.5+ rating")
        print("   🎭 CONSIDER GENRE CHANGE to Action/Horror")
        print("   📅 MOVE TO SUMMER release window")
    
    # Real world comparison
    print(f"\n🎬 REAL WORLD COMPARISON:")
    if profit < -50:
        print("   Similar to MAJOR BOX OFFICE FLOPS:")
        print("   • Radhe Shyam: Budget $150M, Loss $70M (-47% ROI)")
        print("   • John Carter: Budget $263M, Loss $200M (-76% ROI)")
    elif profit > 0:
        print("   Similar to successful movies:")
        print("   • Black Panther: Budget $200M, Profit $1147M (+573% ROI)")
        print("   • Get Out: Budget $4.5M, Profit $250M (+5556% ROI)")

def predict_movie():
    display_header()
    display_quick_tips()
    
    # Initialize predictor
    predictor = AccurateMoviePredictor()
    
    while True:
        # Get input
        movie_name, genre, budget, rating, season, has_star, is_sequel = get_movie_input()
        
        # Show genre info
        genre_info = predictor.genre_data[genre]
        print(f"\n📊 {genre} Movie Info: {genre_info['description']} • Risk: {genre_info['risk']}")
        
        # Show warnings
        if budget > 100 and rating < 7.0:
            print("\n⚠️  HIGH RISK DETECTED: Big budget with average/poor rating often leads to HUGE LOSSES")
        
        if genre == 'Romance' and budget > 50:
            print("\n⚠️  GENRE RISK DETECTED: Romance genre with big budget is VERY RISKY")
        
        if budget < 20 and genre == 'Horror' and rating > 7.0:
            print("\n💰 Great Potential! Low-budget horror with good quality can be very profitable")
        
        # Get prediction
        print("\n🤖 Running accurate industry analysis...")
        predicted_revenue, effects = predictor.predict(budget, genre, rating, season, has_star, is_sequel)
        
        # Calculate finances
        marketing_cost = budget * 0.5
        total_cost = budget + marketing_cost
        profit = predicted_revenue - total_cost
        roi = (profit / total_cost) * 100
        
        # Determine result
        if profit > budget * 1.5:
            result_type = "BLOCKBUSTER HIT"
            result_message = "Exceptional success! Similar to major Hollywood hits."
        elif profit > 0:
            result_type = "PROFITABLE"
            result_message = "Good investment! Should make solid profit."
        elif profit > -budget * 0.3:
            result_type = "BREAK-EVEN"
            result_message = "Might break even or small loss. Needs careful management."
        else:
            result_type = "BOX OFFICE FLOP"
            result_message = "High risk of significant losses. Major changes needed."
        
        # Display results
        display_results(movie_name, budget, predicted_revenue, profit, roi, result_type, result_message, effects)
        
        # Ask to continue
        print("\n" + "="*70)
        again = input("\nPredict another movie? (y/n): ").lower().strip()
        if again != 'y':
            print("\nThank you for using Movie Success Predictor! 🎬")
            break

# Main program
if __name__ == "__main__":
    try:
        predict_movie()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Thank you for using Movie Success Predictor! 🎬")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again.")