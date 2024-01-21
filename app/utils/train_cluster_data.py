from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import sessionmaker
from app.utils.modelImpl import profile_texts, job_texts, candidate_profiles, job_details
from sklearn.cluster import KMeans
import pandas as pd
from app.config.dbconfig import SessionLocal
import joblib

# Create the database engine and session
engine = SessionLocal().bind
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Combine profile and job description texts
all_texts = profile_texts + job_texts

# Use TF-IDF vectorizer to convert texts to TF-IDF matrices
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_texts)

# Save the fitted vectorizer to a file
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

# Choose the number of clusters (you may need to experiment with this)
num_clusters = 5

# Apply K-means clustering
kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
cluster_labels = kmeans.fit_predict(tfidf_matrix)

# Save the fitted KMeans model to a file
joblib.dump(kmeans, 'kmeans_model.joblib')

# Assign cluster labels to profiles and job descriptions
result_data = pd.DataFrame({
    'Profile_ID': [profile.candidate_id for profile in candidate_profiles] + [-1] * len(job_details),
    'Job_ID': [-1] * len(candidate_profiles) + [job.id for job in job_details],
    'Cluster_Label': cluster_labels
})

result_data.to_sql('cluster_data', con=engine, index=False, if_exists='replace')

# Save the DataFrame to a CSV file
result_data.to_csv('clustering_results.csv', index=False)


# Load the saved TF-IDF vectorizer
loaded_vectorizer = joblib.load('tfidf_vectorizer.joblib')

# Load the saved KMeans model
loaded_kmeans = joblib.load('kmeans_model.joblib')

# Example of using the loaded models
new_profile_text = """Skills: Java, Python, C++
"""

new_profile_tfidf = loaded_vectorizer.transform([new_profile_text])

if new_profile_tfidf is not None:
    cluster_label = loaded_kmeans.predict(new_profile_tfidf)
    print(f"Cluster label for the new profile: {cluster_label}")
