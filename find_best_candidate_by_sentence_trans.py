import json
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # This is a lightweight pre-trained model

# Function to load data from a file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to encode skills into sentence embeddings using Sentence-BERT
def encode_skills(skills_list):
    return model.encode(" ".join(skills_list), convert_to_tensor=True)

# Function to calculate semantic similarity using Sentence-BERT embeddings
def calculate_semantic_similarity(job_skills_str, applicants):
    job_embedding = encode_skills(job_skills_str)  # Convert job skills to embedding
    similarities = []
    
    for applicant in applicants:
        applicant_embedding = encode_skills(applicant['skills'])  # Convert applicant's skills to embedding
        similarity = util.pytorch_cos_sim(job_embedding, applicant_embedding).item()  # Calculate cosine similarity
        similarities.append(similarity)
    
    return similarities

# Function to classify similarity score
def classify_similarity(score):
    if score >= 0.75:
        return "strong match"
    elif 0.5 <= score < 0.75:
        return "moderate match"
    else:
        return "weak match"

# Function to match a job with multiple applicants using semantic similarity
def match_job_with_applicants(job, applicants):
    job_skills_str = job['skills']  # Job skills in list format
    
    # Calculate semantic similarities
    similarities = calculate_semantic_similarity(job_skills_str, applicants)
    
    # Display the results with match classification
    for i, score in enumerate(similarities):
        match_strength = classify_similarity(score)
        print(f"Applicant: {applicants[i]['name']} - Similarity Score: {score:.4f} - {match_strength}")
    
    # Identify the best match
    best_match_index = similarities.index(max(similarities))
    best_match = applicants[best_match_index]
    best_match_strength = classify_similarity(similarities[best_match_index])

    print(f"\nBest match for the job at {job['company_name']} is: {best_match['name']} with a similarity score of {similarities[best_match_index]:.4f} ({best_match_strength})")

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
