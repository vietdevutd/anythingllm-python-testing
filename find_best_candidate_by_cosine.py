import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load data from a file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to extract intersecting skills between job and applicant, converting to lowercase
def get_intersecting_skills(job_skills, resume_skills):
    job_skills_lower = set(skill.lower() for skill in job_skills)
    resume_skills_lower = set(skill.lower() for skill in resume_skills)
    return list(job_skills_lower & resume_skills_lower)

# Function to prepare the skills corpus for comparison, converting skills to lowercase
def prepare_skills_corpus(job_skills, resumes):
    skills_corpus = []
    for resume in resumes:
        intersecting_skills = get_intersecting_skills(job_skills, resume['skills'])
        if intersecting_skills:
            skills_corpus.append(" ".join(intersecting_skills))
    return skills_corpus

# Function to calculate cosine similarity using TF-IDF
def calculate_cosine_similarity(skills_corpus, job_skills_str):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(skills_corpus + [job_skills_str])
    return cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])

# Function to classify similarity score
def classify_similarity(score):
    if score >= 0.75:
        return "strong match"
    elif 0.5 <= score < 0.75:
        return "moderate match"
    else:
        return "weak match"

# Function to process job matching for multiple applicants
def match_job_with_applicants(job, applicants):
    job_skills_str = " ".join(skill.lower() for skill in job['skills'])
    skills_corpus = prepare_skills_corpus(job['skills'], applicants)
    
    if not skills_corpus:
        print("No matching skills found for any applicants.")
        return

    # Calculate cosine similarities
    cosine_similarities = calculate_cosine_similarity(skills_corpus, job_skills_str)

    # Display the results with match classification
    for i, score in enumerate(cosine_similarities[0]):
        match_strength = classify_similarity(score)
        print(f"Applicant: {applicants[i]['name']} - Similarity Score: {score:.4f} - {match_strength}")

    # Identify the best match
    best_match_index = cosine_similarities[0].argmax()
    best_match = applicants[best_match_index]
    best_match_strength = classify_similarity(cosine_similarities[0][best_match_index])

    print(f"\nBest match for the job at {job['company_name']} is: {best_match['name']} with a similarity score of {cosine_similarities[0][best_match_index]:.4f} ({best_match_strength})")

# Main function to orchestrate the job-applicant matching
def main(file_path):
    data = load_data(file_path)
    job = data['job_details']  # Single job details
    applicants = data['applicants']  # List of applicants

    match_job_with_applicants(job, applicants)

# Example usage
if __name__ == "__main__":
    file_path = './applications.txt'  # Ensure this points to your modified file
    main(file_path)
