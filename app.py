import streamlit as st
import joblib
from recommender import get_recommendations

df = joblib.load('restaurant_df.pkl')

st.set_page_config(page_title="Restaurant Recommender", layout="centered")
st.title("🍽️ Restaurant Recommendation System")

st.subheader("Choose your preferences:")

city_options = sorted(df['City'].dropna().unique())
cuisine_options = sorted(df['Cuisines'].dropna().unique())
price_range_options = sorted(df['Price range'].dropna().unique())
rating_options = sorted(df['Aggregate rating'].dropna().unique())

city = st.selectbox("Select City", city_options)
cuisine = st.selectbox("Select Cuisine", cuisine_options)
price_range = st.selectbox("Select Price Range (1–4)", price_range_options)
avg_cost = st.slider("Approx. Average Cost for Two", 
                    min_value=int(df['Average Cost for two'].min()), 
                    max_value=5000, 
                    value=int(df['Average Cost for two'].min()), 
                    step=50)
rating = st.select_slider("Minimum Aggregate Rating", 
                        options=sorted(df['Aggregate rating'].unique().round(1)), 
                        value=4.0)

if st.button("Get Recommendations"):
    user_input = {
        'City': city,
        'Cuisines': cuisine,
        'Price range': price_range,
        'Average Cost for two': avg_cost,
        'Aggregate rating': rating
    }

    recommendations = get_recommendations(user_input)

    if recommendations.empty:
        st.warning("No matching restaurants found.")
    else:
        st.subheader("Top Recommendations")
        for _, row in recommendations.iterrows():
            st.markdown(f"**🍴 {row['Restaurant Name']}**")
            st.markdown(f"📍 City: {row['City']}")
            st.markdown(f"🍽️ Cuisine: {row['Cuisines']}")
            st.markdown(f"💰 Cost for Two: {row['Currency']} {row['Average Cost for two']}")
            st.markdown(f"⭐ Rating: {row['Aggregate rating']}")
            st.markdown("---")