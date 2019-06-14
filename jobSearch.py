import os
import requests
from bs4 import BeautifulSoup
from JobFormat import JobFormat


def get_site_content(website):
    response = requests.get(website, timeout=5)
    return BeautifulSoup(response.text, "html.parser")


def get_readable_version(content):
    return content.prettify()


def get_all_jobs_in_seed(seed, maxPage):
    contentTitle = input("what folder to save to?")
    jobList = []

    for pageNum in range(0, maxPage):

        current = seed + "&start=" + str(pageNum)
        try:
            content = get_site_content(current)
        except:
            break

        jobList = (get_jobs(content))+ jobList

    return jobList


def get_jobs(contents):
    jobs = []
    for result in contents.find_all(class_='result'):
        link = result.find(class_="turnstileLink")
        jobTitle = link.get('title')
        jobSummary = result.find(class_='summary').get_text()
        companyName = result.find(class_='company').get_text().strip()
        jobPage = JobFormat(jobTitle, jobSummary, companyName, link)
        jobs.append(jobPage)
    return jobs


def get_job_summary(jobList):
    for job in jobList:
        job.find(class_='summary')


# used to write the content of the html pages to files on local machine
def write_to_html(content, pageNum, contentTitle):
    full_path = os.path.abspath(os.path.join('.', contentTitle))
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        # print('creating new directory at {}'.format(full_path))
        os.mkdir(full_path)

    fileName = os.path.join(full_path, "pagenumber" + str(pageNum) + ".html")

    f = open(fileName, 'w', newline='')
    f.write(content.prettify())
    f.close()


def filter_jobs(jobList, title_filters):
    newList = []
    for position in jobList:
        # print(position)
        if position.qualifies(title_filters):
            newList.append(position)
    return newList


def main():
    # indeed search querie=
    # https://www.indeed.com/jobs?q="job+title+attribute"&l="location+seting"+CA(&entry_level)+&start="(pgno)"
    # url_base+"&start="+str(pgno))
    # website="https://kcnguyen.com/"

    website = input("what is the base site to start the search")
    maxPages = input("how many pages would you like to search")

    jobList = get_all_jobs_in_seed(website, int(maxPages))
    print("filter jobs now")

    filterList = filter_jobs(jobList, ["senior", "intern", "contract", "staff"])
    print("filtered")

    print(filterList)

    print("length of unfiltered list= {}".format(jobList))
    print("length of filtered list= {}".format(filterList))

if __name__ == '__main__':
    main()
