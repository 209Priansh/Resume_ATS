from sqlalchemy.orm import sessionmaker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.dbmodels import Job_Details, Candidate
from app.config.dbconfig import SessionLocal
import pandas as pd

# Create the database engine and session
engine = SessionLocal().bind
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Retrieve candidate profiles and job details from the database
candidate_profiles = session.query(Candidate).all()
job_details = session.query(Job_Details).all()

# Extract texts from the SQLAlchemy objects
profile_texts = [
    f"{profile.first_name} {profile.last_name} {profile.email} "
    f"{' '.join([edu.degree for edu in profile.education])} "
    f"{' '.join([exp.job_title for exp in profile.work_experience])} "
    f"{' '.join([skill.skill_name for skill in profile.skills])}" for profile in candidate_profiles
]

job_texts = [
    f"{job.title} {job.company} {job.job_description}" for job in job_details
]

# Use TF-IDF vectorizer to convert texts to TF-IDF matrices
vectorizer = TfidfVectorizer()
tfidf_matrix_profiles = vectorizer.fit_transform(profile_texts)
tfidf_matrix_jobs = vectorizer.transform(job_texts)

# Calculate cosine similarity between profiles and job details
cosine_similarities = cosine_similarity(tfidf_matrix_profiles, tfidf_matrix_jobs)

# For each profile, find the most similar job description
for i, profile in enumerate(candidate_profiles):
    profile_id = profile.candidate_id
    profile_similarity_scores = cosine_similarities[i]
    most_similar_job_index = profile_similarity_scores.argmax()
    most_similar_job_id = job_details[most_similar_job_index].id

    result_data = pd.DataFrame({
        'Profile_ID': [profile.candidate_id for profile in candidate_profiles],
        'Most_Similar_Job_ID': [job_details[similarity.argmax()].id for similarity in cosine_similarities],
        'Similarity_Score': [similarity.max() for similarity in cosine_similarities]
    })

    # Save the DataFrame to PostgreSQL in a table named 'job_matches'
    result_data.to_sql('job_matches', con=engine, index=False, if_exists='replace')


def predict(session, resume_text):
    # Retrieve candidate profiles and job details from the database
    candidate_profiles = session.query(Candidate).all()
    job_details = session.query(Job_Details).all()

    # Extract texts from the SQLAlchemy objects
    profile_texts = [
        f"{profile.first_name} {profile.last_name} {profile.email} "
        f"{' '.join([edu.degree for edu in profile.education])} "
        f"{' '.join([exp.job_title for exp in profile.work_experience])} "
        f"{' '.join([skill.skill_name for skill in profile.skills])}" for profile in candidate_profiles
    ]

    job_texts = [
        f"{job.title} {job.company} {job.job_description}" for job in job_details
    ]

    # Use TF-IDF vectorizer to convert texts to TF-IDF matrices
    vectorizer = TfidfVectorizer()
    tfidf_matrix_profiles = vectorizer.fit_transform(profile_texts)
    tfidf_matrix_jobs = vectorizer.transform(job_texts)

    # Calculate cosine similarity between profiles and job details
    cosine_similarities = cosine_similarity(tfidf_matrix_profiles, tfidf_matrix_jobs)

    # For the given resume text, find the most similar job descriptions
    resume_tfidf = vectorizer.transform([resume_text])
    resume_similarity_scores = cosine_similarity(resume_tfidf, tfidf_matrix_jobs)[0]
    most_similar_job_indices = resume_similarity_scores.argsort()[::-1]

    # Create a DataFrame with the most similar jobs
    result_data1 = pd.DataFrame({
        'Job_ID': [job_details[index].id for index in most_similar_job_indices],
        'Title': [job_details[index].title for index in most_similar_job_indices],
        'Company': [job_details[index].company for index in most_similar_job_indices],
        'Ratings': [job_details[index].ratings for index in most_similar_job_indices],
        'Job_Description': [job_details[index].job_description for index in most_similar_job_indices],
        'Salary': [job_details[index].salary for index in most_similar_job_indices],
        'Location': [job_details[index].location for index in most_similar_job_indices],
        'Similarity_Score': [resume_similarity_scores[index] for index in most_similar_job_indices]
    })

    return result_data1
