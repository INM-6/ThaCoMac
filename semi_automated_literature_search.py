'''
from serpapi import GoogleSearch
params = {
  "engine": "google_scholar",
  "q": "macaque thalamus OR thalamocortical OR thalamo-cortical",
  "api_key": "c397fc278e5a3483e64735af275a21bf6f78b17a8084ea7f507d933bb4d4b90a"
}

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]
'''

'''
# searching for related literature and write them into file 'list_of_potential_related_literature.txt'
def record_liter(doi_or_url, path):
    with open(path, 'a+') as url_file:
        url_file.seek(0)
        # If file is not empty then append '\n'
        data = url_file.read(100)
        if len(data) > 0 :
            url_file.write('\n')
        # Append text at the end of file
        url_file.write(doi_or_url)
    
# test code
acad_db_name = 'Google Scholar'
search_acad_dbs(acad_db_name, path_urls)
'''

# headers simulating a broswer so that the web scraping won't get blocked
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

# search academic databases, record the urls as a line in a .txt file from the webpages
def search_acad_dbs(acad_dbs, on_topic_kws, path_poten_urls, pdf_folder_path, columns):
    for acad_db in acad_dbs:
    if acad_db_name == 'Google Scholar':
        url = 'https://scholar.google.com/scholar?start=0&q=macaque+thalamus+OR+thalamocortical+OR+thalamo-cortical&hl=en&as_sdt=1,5'
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content,'lxml')
        num_results_str = soup.find_all('div', {'class': 'gs_ab_mdw'})[1].get_text().split()[1]
        # print(int(num_results_str))
        num_results = int(re.sub(r'[^\w\s]', '', num_results_str))
        pages = int(num_results/10)
        pages = 10
        # print(pages)
        # search all pages
        for page in range(pages):
            time.sleep(2)
            start = page * 10
            # google scholar
            page_url = 'https://scholar.google.com/scholar?start=' + str(start) + '&q=macaque+thalamus+OR+thalamocortical+OR+thalamo-cortical&hl=en&as_sdt=1,5'
            # search a page
            response = requests.get(page_url, headers = headers)
            # print(url)
            soup = BeautifulSoup(response.content,'lxml') 
            # print(soup.select('[data-lid]')) 
            for item in soup.select('[data-lid]'): 
                try: 
                    with open(path_urls, 'a+') as url_file:
                        # append text at the end of file
                        url_file.write(item.select('h3')[0].find_all('a', href=True)[0]['href'])
                        url_file.write('\n')
                except Exception as e: 
                    #raise e
                    print("error")
    elif acad_db_name == 'PubMed':
        url = 'https://pubmed.ncbi.nlm.nih.gov/?term=macaque%20AND%20(thalamus%20OR%20cortex%20OR%20thalamocortical%20OR%20thalamo-cortical%20or%20corticothalamic%20OR%20cortico-thalamic)&page=1'
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content,'lxml')
        # print(soup)
        num_results_str = soup.find_all('span', {'class': 'value'})[0].get_text()
        print(num_results_str)
        num_results = int(re.sub(r'[^\w\s]', '', num_results_str))
        pages = int(num_results/10)
        print(pages)
    else:
        None
    
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
'''
# test code: search_acad_dbs(acad_dbs, on_topic_kws, path_poten_urls, pdf_folder_path)

search_acad_dbs(acad_dbs, on_topic_kws, path_poten_urls, pdf_folder_path)
'''