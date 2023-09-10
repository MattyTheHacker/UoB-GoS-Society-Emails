import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
from file_utils import *

DOMAIN = "https://www.guildofstudents.com"
BASE_URL = "https://www.guildofstudents.com/studentgroups/searchgroups/"
VALID_URLS = ['/organisation/', '/studentgroups/societies/']

emails = []
society_urls = []

email_dict = {}

session = requests.Session()

retries = Retry(total=10, backoff_factor=30, status_forcelist=[500, 502, 503, 504])

session.mount('http://', HTTPAdapter(max_retries=retries))

def get_societies(site):
    try:
        r = session.get(site)
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('href') is not None:
                # check if the link is in the valid list
                if link.get('href').startswith(tuple(VALID_URLS)):
                    # check if the link is already in the list
                    society_link = DOMAIN + link.get('href')
                    if society_link not in society_urls:
                        society_urls.append(society_link)
                        print(link.get('href'))
                    else: 
                        print("[INFO] %s already in list" % link.get('href'))
                else: 
                    print("[INFO] %s not in valid list" % link.get('href'))
            else:
                print("[INFO] No href found for %s" % link)
    except Exception as e:
        print(e)
                

def get_emails():
    # for each society url, get the email
    for url in society_urls:
        try:
            r = session.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            email_url = soup.find('a', {'class': 'msl_email'}).get('href')
            email = email_url.split(':')[1]
            # get first h1 as soc name
            soc_name = soup.find('h1').text
            if email not in emails:
                emails.append(email)

            # add to dict
            if soc_name not in email_dict:
                email_dict[soc_name] = email
        except Exception as e:
            print("[ERROR] %s" % url)
            print(e)


def sort_lists():
    global society_urls
    global emails

    # convert all to lower-case
    society_urls = [x.lower() for x in society_urls]
    emails = [x.lower() for x in emails]

    society_urls.sort()
    emails.sort()

if __name__ == "__main__":
    get_societies(BASE_URL)
    get_emails()
    sort_lists()
    save_emails_to_file(emails)
    save_societies_to_file(society_urls)
    save_dict_to_json(email_dict)
    print("Done!")