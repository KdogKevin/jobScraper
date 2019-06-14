import requests
from bs4 import BeautifulSoup
import urllib.request as ur
import re


def get_all_pages(website, max_pages):
    pages=[]
    for num in range(0,max_pages):
        web_url= website+"&start="+str(num)
        page= BeautifulSoup(requests.get(web_url, timeout=5).text,"html.parser")
        pages.append(page)
    return pages

def get_all_jobs(pages):
    jobs=[]
    for page in pages:
        print("in here")
        print(page)
        for job in page.find_all(class_='result'):
            jobs.append(job)
            print("now hjere")
    return jobs



def filter_title(job_title):
    red_flags=["senior", "intern", "contract", "staff"]
    # required = ["software"] #Can also check for required words

    for word in red_flags:
        if word in job_title: return False
    return True


def filter_jobs(jobs):
    filtered=[]
    for job in jobs:
        link = job.find(class_="turnstileLink")
        try:
            job_title = link.get('title')
        except:
            job_title = ""
        try:
            comp = job.find(class_='company').get_text().strip()
        except:
            comp = ""
        if filter_title(job_title.lower()):
            visit="http://www.indeed.com"+link.get('href')
            try:
                html_doc = ur.urlopen(visit).read().decode('utf-8')
            except:
                continue;
            unwanted1 = re.compile('[2-9]\s*\+?-?\s*[1-9]?\s*[yY]e?a?[rR][Ss]?')
            check= unwanted1.search(html_doc)
            if not check:
                print("{} : {} : link: {}".format(job_title, comp, visit))
                filtered.append([job_title,comp,visit])
    return filtered




def main():

    #get url
    # indeed search querie=
    # https://www.indeed.com/jobs?q="job+title+attribute"&l="location+seting"+CA(&entry_level)+&start="(pgno)"
    # url_base+"&start="+str(pgno))
    # website="https://kcnguyen.com/"

    website = input("what is the base site to start the search")
    max_pages = input("how many pages would you like to search")

    #get all pages

    pages= get_all_pages(website,int(max_pages))
    #print(pages)

    #get the jobs on those pages

    jobs= get_all_jobs(pages)

    print(jobs)
    filtered_list = filter_jobs(jobs)


    pass

if __name__ == '__main__':
    main()