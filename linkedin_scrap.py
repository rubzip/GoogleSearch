from GoogleSearch import GoogleSearch
from time import time, sleep
from random import random
import pandas as pd

def get_linkedin_acc(results):
    for result in results:
        if "es.linkedin.com/company" in result:
            return result
    return "???"

def clean(line):
    return line[:-1] if line[-1]=='\n' else line

def get_all_link_accs(fname_in, fname_out, MAX_TIME=20*60, a=10, b=10):
    google = GoogleSearch()
    
    remaining = []
    with open(fname_in, encoding="utf8") as f:
        for line in f:
            remaining.append(clean(line))

    ini = time()
    data = []
    while ((time() - ini)<MAX_TIME) and (len(remaining)>0):
        companies = remaining 
        for company in companies:
            try:
                results = google.search(query=f"{company} linkedin", random_sleep=True)
                url = get_linkedin_acc(results)
                
                remaining.remove(company)
                data.append((company, url))
            except Exception as e:
                print(e)
                sleep(a + b*random())
    
    pd.DataFrame(data, columns=["Company", "Linkedin URL"]).sort_values(by="Company").to_csv("linkedin.csv")