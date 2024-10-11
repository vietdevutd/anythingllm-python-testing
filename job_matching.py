import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Step 1: Specify the path to your modified text file
file_path = './job_desc.txt'  # Ensure this points to your modified file

# Step 2: Read the JSON data from the text file
with open(file_path, 'r') as file:
    data = json.load(file)  # Load the JSON data

# Step 3: Extract the job list and resume details
job_postings = data['job_list']  # List of job postings
resume_skills = data['resume_details']['skills']  # Resume skills

# Step 4: Compare only the intersecting skills between the resume and each job
def get_intersecting_skills(job_skills, resume_skills):
    return list(set(job_skills) & set(resume_skills))  # Get the common skills (intersection)

# Prepare skills corpus to compare only intersecting skills
skills_corpus = []

for job in job_postings:
    # Get intersecting skills between job and resume
    intersecting_skills = get_intersecting_skills(job['skills'], resume_skills)
    
    # Add only intersecting skills if they exist
    if intersecting_skills:
        skills_corpus.append(" ".join(intersecting_skills))  # Join intersecting skills into string

# Convert the resume's intersecting skills to a single string for each job
resume_intersecting_skills_str = " ".join(resume_skills)

# Step 5: Apply TF-IDF vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(skills_corpus + [resume_intersecting_skills_str])  # Combine job and resume corpus


# Step 6: Calculate cosine similarity between the resume skills and each job
cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])

# Function to convert cosine similarity to degree
def cosine_to_degree(cosine_value):
    # Ensure the cosine similarity is within [-1, 1] range to avoid numerical issues
    if cosine_value < -1:
        cosine_value = -1
    elif cosine_value > 1:
        cosine_value = 1
    return np.degrees(np.arccos(cosine_value))


# Step 7: Define thresholds for strong, moderate, and weak matches
def classify_similarity(score):
    if score >= 0.75:
        return "strong match"
    elif 0.5 <= score < 0.75:
        return "moderate match"
    else:
        return "weak match"

# Step 8: Display the results with match classification and cosine degree
for i, score in enumerate(cosine_similarities[0]):
    match_strength = classify_similarity(score)
    cosine_degree = cosine_to_degree(score)
    print(f"Job: {job_postings[i]['company_name']} - Similarity Score: {score:.4f} - {match_strength}")

# Step 9: Identify the best match
best_match_index = cosine_similarities[0].argmax()
best_match = job_postings[best_match_index]
best_match_strength = classify_similarity(cosine_similarities[0][best_match_index])
best_match_degree = cosine_to_degree(cosine_similarities[0][best_match_index])

print(f"\nBest job match for the resume is: {best_match['company_name']} with a similarity score of {cosine_similarities[0][best_match_index]:.4f} ({best_match_strength})")