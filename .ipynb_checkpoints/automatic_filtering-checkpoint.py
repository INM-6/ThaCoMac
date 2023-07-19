# count the number of times that certain on-topic keyword appear in a given text
def count_keyword(text: str, keyword: str) -> int:
    # print(text)
    # remove spaces before and after the text and split the string by word
    text = text.strip().split(" ")
    word_count = 0
    for word in text:
        # print(word)
        if word == keyword:
            word_count += 1
    return word_count

'''
# test code: count_keyword(text: str, keyword: str) -> int
text = 'This apple 6i7s very tasty？、  2but th&e banana is not delicious at all.6'
keyword = 'is'
count = count_keyword(text, keyword)
print(count)
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

'''
# test code: add_rows_to_csv(path_potential, info_json, columns)

add_rows_to_csv(path_potential, info_json, columns)
'''

# count the number of times all on-topic keywords appear in the text (title, abstract, keywords and so on)
# extracted from the given url
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
# test code: 
url = 'https://pubmed.ncbi.nlm.nih.gov/32053769/'
pdf_folder_path = '/Users/didihou/myProjects/liter_pdfs'
info_json_ele = count_freq_from_liter(url, on_topic_kws)
file_name = 'test.pdf'
download_pdf_file(info_json_ele['pdf_link'], pdf_folder_path, file_name)
print(info_json_ele)
'''

# download pdf to specified folder given pdf_url and file name
def download_pdf(pdf_url: str, pdf_folder_path: str, file_name: str) -> bool:    
    response = requests.get(pdf_url, stream=True, headers = headers)
    
    # download the .pdf file to the pdf_file_path folder
    # write content in pdf file
    pdf_path = os.path.join(pdf_folder_path, file_name + '.pdf')
    if response.status_code == 200:
        with open(pdf_path, 'wb') as pdf_object:
            pdf_object.write(response.content)
            # print(f'{file_name} was successfully saved!')
            return True
    else:
        print(f'Failed downloading PDF:' + 'pdf_url')
        print(f'HTTP response status code: {response.status_code}')
        return False

'''
# test code: download_pdf(pdf_url: str, pdf_folder_path: str, file_name: str) -> bool
pdf_url = 'https://www.sciencedirect.com/science/article/pii/S0896627320300052/pdfft?md5=3f0648c6385e6fae3a5a73b053903014&pid=1-s2.0-S0896627320300052-main.pdf'
file_name = 'test_pdf'
download_pdf(pdf_url, pdf_folder_path, file_name)
'''

# scan each url in list_of_literature_urls.txt and record information and download pdf
def scan_record_download(path_urls, on_topic_kws, pdf_folder_path):
    columns = ['DOI', 'url', 'title'] + on_topic_kws
    file_index = 0
    with open(path_urls, 'r') as url_file:
        for url in url_file:
            # print(url)
            info_json = {}
            info_json = count_freq_from_liter(url.strip(), on_topic_kws)
            add_rows_to_csv(path_potential, info_json, columns)
            # download_pdf_file(info_json['pdf_link'], pdf_folder_path, str(file_index))
            file_index += 1

'''
# test code: scan_record_download(path_urls, on_topic_kws, pdf_folder_path)
scan_record_download(path_urls, on_topic_kws, pdf_folder_path)
'''
