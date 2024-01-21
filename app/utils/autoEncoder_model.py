import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

from app.utils.fetchProfileList import your_profile_id_list
from app.utils.train_cluster_data import cluster_labels, tfidf_matrix

# Split the data into train and test sets
X_train, X_test, _, _ = train_test_split(tfidf_matrix, cluster_labels, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.toarray())
X_test_scaled = scaler.transform(X_test.toarray())

# Simple autoencoder model
model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=X_train_scaled.shape[1]))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=X_train_scaled.shape[1], activation='linear'))

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_scaled, X_train_scaled, epochs=10, batch_size=32, shuffle=True, validation_data=(X_test_scaled, X_test_scaled))

# Use the encoder part of the model to get the learned representation
encoder_model = Sequential(model.layers[:-1])  # Exclude the last layer (decoder)

# Transform the TF-IDF matrix to the learned representation
learned_representation = encoder_model.predict(X_test_scaled)

# Assuming you have a new profile or job description
vectorizer = joblib.load('tfidf_vectorizer.joblib')  # Load the saved TF-IDF vectorizer
new_profile_text = "Machine Learning, Data Science"
new_profile_tfidf = vectorizer.transform([new_profile_text]).toarray()  # Convert to dense array
new_profile_scaled = scaler.transform(new_profile_tfidf)

# Transform the new profile to the learned representation
new_profile_representation = encoder_model.predict(new_profile_scaled)

# Calculate similarity between the new profile and existing profiles
similarity_scores = np.dot(learned_representation, new_profile_representation.T)

# Normalize similarity scores
normalized_scores = (similarity_scores - similarity_scores.min()) / (similarity_scores.max() - similarity_scores.min())

# Get the most similar profiles
most_similar_indices = np.argsort(normalized_scores[:, 0])[::-1]

# Print the most similar profiles
for idx in most_similar_indices[:5]:
    profile_id = your_profile_id_list[idx]  # Replace with your actual profile ID list
    print(f"Profile ID: {profile_id}, Similarity Score: {normalized_scores[idx, 0]}, Cluster Label: {cluster_labels[idx]}")
