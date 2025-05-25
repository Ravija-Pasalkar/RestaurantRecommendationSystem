import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = joblib.load('restaurant_df.pkl')
vectorizer = joblib.load('vectorizer.pkl')
feature_matrix = joblib.load('feature_matrix.pkl')

currency_conversion = {
    "Dollar($)": 83,
    "Pounds(£)": 105,
    "Brazilian Real(R$)": 17,
    "Emirati Diram(AED)": 22,
    "Indian Rupees(Rs.)": 1
}

df['Cost_INR'] = df.apply(lambda row: row['Average Cost for two'] * currency_conversion.get(row['Currency'], 1), axis=1)

def get_recommendations(user_input, top_n=5):
    user_cost_inr = user_input['Average Cost for two'] * currency_conversion.get("Indian Rupees(Rs.)", 1)
    min_rating = float(user_input['Aggregate rating'])

    filtered_df = df[
        (df['City'].str.lower() == user_input['City'].lower()) &
        (df['Cost_INR'] <= user_cost_inr + 200) &
        (df['Aggregate rating'] >= min_rating)
    ]

    if filtered_df.empty:
        return pd.DataFrame(columns=[
            'Restaurant Name', 'Cuisines', 'City',
            'Average Cost for two', 'Currency', 'Aggregate rating'
        ])

    query = f"{user_input['City']} {user_input['Cuisines']} PriceRange{user_input['Price range']} Cost{user_input['Average Cost for two']} Rating{user_input['Aggregate rating']}"
    query_vec = vectorizer.transform([query])

    filtered_indices = filtered_df.index
    filtered_feature_matrix = feature_matrix[filtered_indices]

    sim_scores = cosine_similarity(query_vec, filtered_feature_matrix).flatten()
    top_indices_relative = np.argsort(sim_scores)[-top_n:][::-1]
    top_indices = filtered_indices[top_indices_relative]

    recommended_df = df.loc[top_indices][[
        'Restaurant Name', 'Cuisines', 'City', 'Average Cost for two', 'Currency', 'Aggregate rating'
    ]]

    return recommended_df.sort_values(by='Aggregate rating', ascending=False).reset_index(drop=True)