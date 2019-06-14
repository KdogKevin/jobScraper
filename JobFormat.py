import requests
import re


class JobFormat:
    def __init__(self,title, summary, company, link,):

        self.summary = summary
        self.company = company
        self.link = link
        self.title= title


    def __repr__(self):
        str=""
        try:
            str=("{}/\n{}\n{}\n{}").format(self.title, self.company, self.link, self.description)
        except:
            str= ("{}/\n{}\n{}\n{}").format(self.title, self.company, self.link, self.summary)
        return str

    def qualifies(self, title_filters):
        print("check to see if description is matched")
        for filter in title_filters:
            #filter caught a word in title we dont want
            try:
                if filter in self.title:
                    return False
            except:
                self.title="no found title"
                break

        #defining the Regex

        unwanted1=re.compile('[2-9]\s*\+?-?\s*[1-9]?\s*[yY]e?a?[rR][Ss]?')

        badmatch=self.description.text().search(unwanted1)