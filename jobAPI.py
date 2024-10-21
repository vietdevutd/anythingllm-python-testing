import requests
from bs4 import BeautifulSoup

title = "Software Engineer"
location = "Dallas, TX"

#URL for job listing
list_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=Dallas%2C%2BTexas%2C%2BUnited%2BStates&start=25"
response = requests.get(list_url)
if response.status_code == 200:
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    jobs_page = list_soup.find_all("li") # Get the list of jobs
    job_id_list = []

    # Get job id
    for job in jobs_page:
        base_card_div = job.find("div", {"class": "base-card"})
        job_id = base_card_div.get("data-entity-urn").split(":")[3]
        job_id_list.append(job_id)
    job_list = []
    for job_id in job_id_list:
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        job_response = requests.get(job_url)
        if job_response.status_code == 200:
            job_soup = BeautifulSoup(job_response.text, "html.parser")
            job_post = {}
            #Extract job description
            job_description_div = job_soup.find("div", {"class": "show-more-less-html__markup"})
            if job_description_div:
                job_post["job_description"] = job_description_div.get_text(separator=" ").replace("\n", " ").strip()
            else:
                job_post["job_description"] = "No description available"
            job_list.append(job_post)
        else:
            print(f"Failed to retrieve job with id {job_id}, status code: {response.status_code}")
    print(job_list)
else:
    print(f"Failed to retrieve job list, status code: {response.status_code}")
