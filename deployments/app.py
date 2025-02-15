import streamlit as st
import pandas as pd
from distilgpt2_recommender import get_recommendations

# Update the file path to point to the data folder
file_path = '../data/cosmetics_prepared.csv'
df = pd.read_csv(file_path)

def main():
    st.title('Skincare Products Recommendation System with distilgpt2')
    
    # Input fields
    skin_type = st.selectbox('Select your skin type:', ('Combination', 'Dry', 'Normal', 'Oily', 'Sensitive'))
    price_range = st.text_input('Enter price range (e.g., "$15-$30"):', "$15-$30")
    ingredient_pref = st.text_input("Enter your preferred ingredient (optional):", "aloe")
    
    if st.button('Get Recommendations'):
        # Prepare user input
        candidate_text = "\n".join(df['description'].tolist()[:5])  # Use a subset for testing
        user_input = f"{skin_type} skin with {ingredient_pref} in the price range {price_range}"
        
        # Generate recommendations
        recommendations = get_recommendations(skin_type, price_range, ingredient_pref, candidate_text)
        
        # Display recommendations
        st.subheader("Recommendations")
        if recommendations.strip():
            st.write(recommendations)
        else:
            st.write("No recommendations generated. Please try again with different inputs.")

if __name__ == '__main__':
    main()