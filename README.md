# RestaurantRecommendationSystem
A content-based restaurant recommender app built using NLP techniques like TF-IDF vectorization and cosine similarity. Developed and deployed using Streamlit.

## Objective
Recommend top-rated restaurants to users based on preferences like:
- City
- Cuisine
- Average Cost for Two
- Price Range
- Minimum Aggregate Rating

## How It Works
### 1. **Data Preprocessing**
- Loaded and cleaned restaurant dataset
- Combined features (City, Cuisine, Price, Rating) into textual descriptions
- Converted all costs to INR for consistent filtering

### 2. **Vectorization**
- Applied **TF-IDF Vectorizer** to transform text into numeric feature vectors

### 3. **Similarity Calculation**
- Filtered results based on city, cost & rating criteria
- Used cosine similarity between user input and restaurant vectors
- Returned top 5 most similar restaurants

## Streamlit App Features
- Select City, Cuisine, Price Range
- Set Cost and Minimum Rating
- Click "Get Recommendations" to view results
