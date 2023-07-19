import random
import re
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd

import file_path_management as FPM
import public_library as PL

def search_google_scholar(init_url, headers):
    # create a .txt file to record the urls of google scholar search results, clear the file if already exists
    f = open('google_scholar_poten_urls.txt', 'w')
    f.truncate()
    f.close()

    # request the first page and extract the number of pages of the search results
    first_page = init_url
    response = requests.get(first_page, headers = headers)
    soup = BeautifulSoup(response.content,'lxml')
    # print(soup)
    num_results_str = soup.find_all('div', {'class': 'gs_ab_mdw'})[1].get_text().split()[1]
    # print(num_results_str)
    # print(int(num_results_str))
    num_results = int(re.sub(r'[^\w\s]', '', num_results_str))
    pages = int(num_results/10)
    # print(pages)
    
    # iterate all pages and record the results
    pages = 5
    for page in range(pages):
        time.sleep(random.randint(1, 10))
        start = page * 10
        # google scholar
        page_url = init_url.split('?start=')[0] + '?start=' + str(start) + '&q=' + init_url.split('?start=')[1].split('&q=')[1]
        # search a page
        response = requests.get(page_url, headers = headers)
        # print(url)
        soup = BeautifulSoup(response.content,'lxml') 
        # print(soup.select('[data-lid]')) 
        for item in soup.select('[data-lid]'):
            add_url = item.select('h3')[0].find_all('a', href=True)[0]['href']
            try: 
                with open('google_scholar_poten_urls.txt', 'a') as url_file:
                    # append text at the end of file
                    url_file.write(f'{add_url}\n')
            except Exception as e: 
                print("Error when trying to write in google_scholar_poten_urls.txt")
                raise e
    print("Searching Google Scholar complated!")

def search_webofscience(init_url, headers):
    print("Searching Web of Science complated!")

def search_PubMed_Central_PMC(iinit_url, headers):
    print("Searching PubMedd Central PMC complated!")

def search_Europe_PMC(init_url, headers):
    print("Searching Europe PMC complated!")

# search academic databases, record the urls as a line in a .txt file from the webpages
def search_acad_dbs(acad_dbs, init_urls, headers, proxy):
    for acad_db in acad_dbs:
        if acad_db == 'Google Scholar':
            print("Searching Google Scholar...")
            search_google_scholar(init_urls['gs'], headers)
        elif acad_db == 'Web of Science':
            print("Searching Web of Science...")
            search_webofscience(init_urls['wos'], headers)
        elif acad_db == 'PubMed_Central_PMC':
            print("Searching PubMed Central PMC...")
            search_PubMed_Central_PMC(init_urls['pubmed'], headers)
        elif acad_db == 'Europe_PMC':
            print("Searching Europe PMC...")
            search_Europe_PMC(init_urls['pubmed'], headers)
        else:
            print("The specified academic database: " + acad_db + " is not supported by this function.")
            print("Plese choose one of the following databases:",)
            for db in ['Google Scholar', 'Web of Science', 'PubMed_Central_PMC', 'Europe_PMC']:
                print(db)
        
'''
        for page in range(pages):
            time.sleep(2)
            start = page * 10
            # google scholar
            url = 'https://scholar.google.com/scholar?start=' + str(start) + '&q=macaque+thalamus+OR+thalamocortical+OR+thalamo-cortical&hl=en&as_sdt=1,5'
            # pubmed
            url = 'https://pubmed.ncbi.nlm.nih.gov/?term=macaque%20AND%20(thalamus%20OR%20cortex%20OR%20thalamocortical%20OR%20thalamo-cortical%20or%20corticothalamic%20OR%20cortico-thalamic)&page=1
            response = requests.get(url,headers = headers)
            # print(url)
            soup = BeautifulSoup(response.content,'lxml') 
            #print(soup.select('[data-lid]')) 
            for item in soup.select('[data-lid]'): 
                try: 
                    # print('----------------------------------------') 
                    # print(item)  
                    # print(item.select('h3')[0])
                    with open(path_urls, 'a+') as url_file:
                        url_file.seek(0)
                        # If file is not empty then append '\n'
                        data = url_file.read(100)
                        if len(data) > 0 :
                            url_file.write('\n')
                            # Append text at the end of file
                        url_file.write('----------------------------------------\n')
                        url_file.write(item.select('h3')[0].get_text())
                        url_file.write('\n')
                        # print(item.select('h3')[0].get_text())
                        for a in item.select('h3')[0].find_all('a', href=True):
                            # print(a['href'])
                            url_file.write(a['href'])
                            url_file.write('\n')
                            # print(item.select('a'))
                            # print("PDF link:")
                        url_file.write(item.select('a')[0]['href'])
                        url_file.write('\n')
                        # print(item.select('a')[0]['href'])
                        # print(item.select('.gs_rs')[0].get_text()) 
                        # print('----------------------------------------') 
                except Exception as e: 
                    #raise e 
                    print('')
'''

def span_citations(seed_papers, num_span_time, headers, proxy):
    None
    
def search_conne_db(connec_db, connec_db_quries):
    None
    # end of search_conne_db
    
def merge_search_results():
    # process gs_poten_urls
    with open(FPM.gs_poten_urls, 'r') as file:
        lines = []
        for line in file:
            print(line)
            line = line.strip()
            lines.append(line)
    print(len(lines))
    doi_list = []
    for url in lines:
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content,'lxml')
        # print(soup)
        num_results_str = soup.find_all('a', href = True)
        for href in num_results_str:
            if '//doi.org/' in href:
                doi_list.append(href)
    doi_df = pd.DataFrame({'DOI': doi_list})
    PL.clear_file(FPM.path_poten_csv)
    doi_df.to_csv(FPM.path_poten_csv)
    
    # process wos_poten_urls
    doi_df = pd.read_excel(FPM.wos_poten_urls, engine = 'xlrd')
    doi_df = doi_df[['DOI']]
    doi_df.to_csv(FPM.path_poten_csv)
    
    # process pubmed_pmc_poten_urls
    doi_df = pd.read_csv(FPM.pubmed_pmc_poten_urls)
    doi_df = doi_df[['DOI']]
    doi_df.to_csv(FPM.path_poten_csv)
    
    # process eupmc_poten_urls
    doi_df = pd.read_csv(FPM.eupmc_poten_urls)
    doi_df = doi_df[['DOI']]
    doi_df.to_csv(FPM.path_poten_csv)
    
    # eliminate duplicates
    doi_df = pd.read_excel(FPM.path_poten_csv)
    print(doi_df.head())
    # end of merge_search_results


if __name__ == "__main__":
    # test code: search_acad_dbs(acad_dbs, init_urls, headers)
    acad_dbs = ['Semantic Scholar', 'Google Scholar', 'Web of Science', 'PubMed_Central_PMC', 'Europe_PMC']
    init_urls = {'gs': 'https://scholar.google.com/scholar?start=0&q=%22thalamus%22+OR+%22thalamocortical%22+OR+%22thalamo-cortical%22+%22macaque%22&hl=en&as_sdt=1,5',
                'wos': '',
                'pubmed': '',
                'eupmc': ''
                }
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    search_acad_dbs(acad_dbs, init_urls, headers)