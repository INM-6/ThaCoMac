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

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

# method 1: searching academic databases using searching keyword lexicon
def search_acad_db(keywords, acad_db):
    return liter_list_1

# method 2: spanning citations of seed papers
def expand_citation(seed_papers):
    return liter_list_2

# method 3: querying the existing connectome database 
def search_conne_db(connec_db, connec_db_quries):
    return liter_list_3


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
        
'''
# code for testing function: record_liter(doi_or_url, path)
doi_or_url = 'http://cocomac.g-node.org/main/index.php'
for i in range(10):
    record_liter(doi_or_url)
'''
    
# test code
acad_db_name = 'Google Scholar'
search_acad_dbs(acad_db_name, path_urls)


# count the number of times that certain on-topic keyword appear in a given text
def count_keyword(text: str, keyword: str) -> int:
    # print(text)
    word_count = 0
    for word in text.strip().split(" "):
        # print(word)
        if word == keyword:
            word_count += 1
    # print(f"I found {word_count} words")
    return word_count

'''
# test code
text = 'This apple 6i7s very tasty？、  2but th&e banana is not delicious at all.6'
keyword = 'is'
count = count_keyword(text, keyword)
print(count)
'''

# download pdf given pdf_url
def download_pdf_file(pdf_url: str, pdf_folder_path: str, file_name: str) -> bool:
    # param url: The url of the PDF file to be downloaded
    # return: True if PDF file was successfully downloaded, otherwise False.
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'} 
    response = requests.get(pdf_url, stream=True, headers = headers)
    
    # download the .pdf file to the pdf_file_path folder
    # write content in pdf file
    pdf_path = os.path.join(pdf_folder_path, file_name)
    if response.status_code == 200:
        # save in current working directory
        with open(pdf_path, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False
    
# read line by line the urls of related literature in the tex file and access the content
# seach for on-topic keywords and record the number of times they appear and record to a .csv file
def ChatPDF_relatedness(path_urls, ChatPDF_related_queries):
    with open(path_urls, 'r') as url_file:
        for line in url_file:
            a = 1
            # code
            
'''
# code for testing function: ChatPDF_relatedness(path_urls, ChatPDF_related_queries)

'''

# extract text of title, abstract, keywords, introduction from given url and download PDF of the paper
# return a json object consisting: DOI, url, keyword:frequency pair, relatedness of answers from ChatGPT

def count_freq_from_liter(url, on_topic_kws):
    print(url)
    # access the url by web scraping
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'} 
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content,'lxml')
    print(len(soup))
    
    # extract DOI
    # print(soup.find_all("a", {'class': 'id-link'}, href = True)[1]['href'])
    doi = soup.find_all("a", {'class': 'id-link'}, href = True)[1]['href']
    
    # extract title
    title = soup.select('h1')[0].get_text().strip()
    title = re.sub(' +', ' ', title).capitalize()
    
    '''
    # extract PDF link if exists
    print(doi)
    response_pdf = requests.get(doi, headers = headers)
    print(response_pdf.url)
    pdf_page_link = response_pdf.url
        
    # pdf_page = soup.find_all("a", {'class':'link-item dialog-focus'}, href = True)[0]['href']
    
    # print(pdf_page_link)
    pdf_page = requests.get(pdf_page_link, headers = headers)
    soup_pdf = BeautifulSoup(pdf_page.content,'lxml')
    print(len(soup_pdf.find_all("a", href = True)))
    pdf_link = soup_pdf.find_all("a", href = True)[0]['href']
    
    
    # print(pdf_link)
    pdf_link = 'https://www.ncbi.nlm.nih.gov' + pdf_link
    '''
    # extract title, abstract, keywords, introduction from the returned html file
    # count keywords from abstract + keywords
    abs_kws = soup.find_all("div", {'class': 'abstract'})[0].get_text()
    abs_kws = abs_kws.strip()
    abs_kws = re.sub(' +', ' ', abs_kws)
    text = title + ' ' + abs_kws
    text = re.sub(r"[^a-zA-Z' ']","",text).lower()
    
    # record the information into json
    info_json = {}
    info_json['DOI'] = doi,
    info_json['url'] = url,
    info_json['title'] = title
    # info_json['pdf_link'] = pdf_link
    # count the on-topic keywords or calculate the frequency
    for i in range(len(on_topic_kws)):
        word_count = count_keyword(text, on_topic_kws[i])
        info_json[on_topic_kws[i]] = word_count
    
    return info_json
  
'''
# test
url = 'https://pubmed.ncbi.nlm.nih.gov/32053769/'
pdf_folder_path = '/Users/didihou/myProjects/liter_pdfs'
info_json_ele = count_freq_from_liter(url, on_topic_kws)
file_name = 'test.pdf'
download_pdf_file(info_json_ele['pdf_link'], pdf_folder_path, file_name)
print(info_json_ele)
'''

# add the information to list_of_potential_related_literature.csv
def add_rows_to_csv(path_potential, info_json, columns):
    new_row = info_json
    df_new_row = pd.DataFrame(new_row, columns = columns)
    
    with open(path_potential, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            df_new_row.to_csv(path_potential, index = False, header = True)
        else:
            df_new_row.to_csv(path_potential, mode = 'a', index = False, header = False)
    # df_new_row.to_csv(path_potential, index = False)
    # df_liter = df_liter.append(new_row, ignore_index=False)
    # print(df_liter)
    
# scan url in list_of_literature_urls.txt and record information and download pdf
def scan_record_download(path_urls, on_topic_kws, pdf_folder_path, columns):
    file_index = 0
    with open(path_urls, 'r') as url_file:
        for url in url_file:
            # print(url)
            info_json = {}
            info_json = count_freq_from_liter(url.strip(), on_topic_kws)
            add_rows_to_csv(path_potential, info_json, columns)
            # download_pdf_file(info_json['pdf_link'], pdf_folder_path, str(file_index))
            file_index += 1
            
columns = ['DOI', 'url', 'title'] + on_topic_kws


scan_record_download(path_urls, on_topic_kws, pdf_folder_path, columns)

search_acad_db(acad_dbs, on_topic_kws, path_poten_urls, pdf_folder_path, columns)

def search_acad_db(acad_dbs, on_topic_kws, path_poten_urls, pdf_folder_path, columns):
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