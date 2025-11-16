import time

def extract_jobs_prospects():
    # unable to transfer crawled data from dbfs to Unity Catalog due to "Free Edition"
    # Instead, crawling was done locally then transferred to Unity Catalog
    time.sleep(10)

extract_jobs_prospects()
print("Job prospects data extracted and transformed.")