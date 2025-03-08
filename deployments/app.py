import streamlit as st
import pandas as pd
from qwen import get_recommendations

# Update the file path to point to the data folder
file_path = '../data/prepared.csv'
df = pd.read_csv(file_path)

def main():
    st.title('Skincare Products Recommendation System')

    # Input fields
    skin_type = st.selectbox('Select your skin type:', ('Combination', 'Dry', 'Normal', 'Oily', 'Sensitive'))
    min_price, max_price = st.slider('Select your price range:', 0, 400, (15, 30))  # Slider for price range
    product_type = st.selectbox('Select product type:', ('Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye Cream', 'Sun Protect'))
    brand_pref = st.text_input("Enter your preferred brand (optional):", "")

    if st.button('Get Recommendations'):
        # Prepare user input
        # Use the description column directly for candidate_text
        candidate_text = "\n".join(df['description'].tolist())

        # Generate recommendations
        recommendations = get_recommendations(skin_type, (min_price, max_price), product_type, brand_pref, candidate_text)
        
        # Display recommendations
        st.subheader("Recommendations")
        if recommendations.strip():
            st.write(recommendations)
        else:
            st.write("No recommendations generated. Please try again with different inputs.")

if __name__ == '__main__':
    main()