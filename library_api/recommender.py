import os
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'library_api', 'assets', 'models')
DATA_DIR = os.path.join(BASE_DIR, 'library_api', 'assets', 'data')


tfidf = joblib.load(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'))
knn = joblib.load(os.path.join(MODEL_DIR, 'knn_model.pkl'))

df = pd.read_csv(os.path.join(DATA_DIR, 'books_50K.csv'))

def get_combined_recommendations(titles, n_recommendations=5):
    # Transform input titles using the same TF-IDF vectorizer
    input_tfidf = tfidf.transform(titles)
    
    # Calculate the mean vector for all input titles to represent their combined features
    combined_vector = np.mean(input_tfidf.toarray(), axis=0).reshape(1, -1)
    
    # Find nearest neighbors for the combined vector using the KNN model
    distances, indices = knn.kneighbors(combined_vector, n_neighbors=n_recommendations + len(titles))
    
    # Collect recommended titles (excluding the input titles themselves)
    recommendations = []
    for idx in indices[0]:
        if df['title'].iloc[idx] not in titles:
            recommendations.append(df['title'].iloc[idx])
        if len(recommendations) >= n_recommendations:
            break
    
    return recommendations
