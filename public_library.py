# self-written public library

# import internal .py modules
from bs4 import BeautifulSoup
import numpy as np
import file_path_management as fpath
import public_library as plib

# import packages
import csv
import pandas as pd
import PyPDF2
import requests
import time
import os
import random
from requests.auth import HTTPProxyAuth
from metapub import FindIt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import os


# setting headers and proxies
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
def get_proxies():
    with open(fpath.proxy_list) as f:
        proxy_list = f.readlines()
        # print(proxy_list)
        i = random.randint(0, len(proxy_list)-1)
    proxies = { 
        "http": "http://" + proxy_list[i].strip(),
    }
    return proxies
# --------------------start of test code--------------------
# page_url = "https://scholar.google.com/scholar?start=0&q=(macaque+OR+macaca+OR+%22rhesus+monkey%22)+(thalamus+OR+thalamic+OR+thalamocortical+OR+%22thalamo-cortical%22)&hl=en&as_sdt=0,5"
# proxies = get_proxies()
# page = 2
# if(page%10 == 0):
#     time.sleep(5*60)
#     proxies = get_proxies()
# print(proxies)
# response = requests.get(page_url, headers = plib.headers, proxies = proxies)
# page = 5
# if(page%5 == 0):
#     time.sleep(5)
#     proxies = get_proxies()
# print(proxies)
# response = requests.get(page_url, headers = plib.headers, proxies = proxies)
# ---------------------end of test code---------------------


# request a webpage
def request_webpage(url):
    response = requests.get(url, headers=plib.headers)
    while(response.status_code != 200):
        print("Error", response.status_code, "when searching page:", url)
        time.sleep(random.randint(5)*60)
        response = requests.get(url, headers = plib.headers)
    soup = BeautifulSoup(response.content, "lxml")
    return soup
# --------------------start of test code--------------------
# url = "https://pubmed.ncbi.nlm.nih.gov/35851953/"
# proxies = get_proxies()
# soup = request_webpage(url, proxies)
# print(soup)
# ---------------------end of test code---------------------


# clear a file given file path
def clear_file(file_path):
    with open(file_path, 'w') as f:
        f.truncate()
        f.close()
# --------------------start of test code--------------------
# file_path = ''
# clear_file(file_path)
# ---------------------end of test code---------------------


# ask ChatGPT
def ask_ChatGPT(context, queries):
    answers =  []
    # code
    return answers 
# --------------------start of test code--------------------
# context = ['', '']
# queries = ['', '']
# answers = ask_ChatGPT(context, queries)
# for answer in answers:
#     print(answers, '\n')
# ---------------------end of test code---------------------


# add a new row to a given .csv file
def add_row_to_csv(csv_path, new_row, columns):
    try:
        df_new_row = pd.DataFrame(data = new_row, columns = columns)
        df_new_row.to_csv(csv_path, mode = 'a', index = False, header = False, encoding='utf-8')
        return True
    except:
        return False
# --------------------start of test code--------------------
# add_rows_to_csv(path_potential, info_json, columns)
# ---------------------end of test code---------------------


# extract text from given .pdf file
def pdf2text(pdf_path):
    # creating a pdf reader object
    reader = PyPDF2.PdfReader(pdf_path)
    
    # printing number of pages in pdf file
    print(len(reader.pages))
    
    # getting a specific page from the pdf file
    page = reader.pages[0]
    
    # extracting text from page
    text = "".join(page.extract_text().splitlines())
    return text
# --------------------start of test code--------------------
# pdf_path = ''
# text = pdf2text(pdf_path)
# print(text)
# ---------------------end of test code---------------------

  
# get the final url when the given url is redirected once or even multiple times
def get_final_redirected_url(url):
    response = requests.get(url, headers = plib.headers)
    
    while(response.status_code != 200):
        if response.status_code == 403: # forbidden
            final_url = url
            break
        elif response.status_code == 404: # not found
            final_url = np.nan
            break
        else:
            print(response.status_code)     
            # sleep for 5 minutes
            time.sleep(300)
            response = requests.get(url, headers = plib.headers)
    if response.status_code == 200:
        final_url = response.url
        
    return final_url
# --------------------start of test code--------------------
# url = "https://doi.org/10.1016/j.neuron.2020.01.005"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0896627320300052"
# final_url, histo = get_final_redirected_url(url)
# print(histo)
# print(final_url)
# ---------------------end of test code---------------------


# download pdf to specified folder given pdf_url and file name
def download_pdf(pdf_url: str, pdf_folder_path: str, file_name: str) -> bool:    
    response = requests.get(pdf_url, stream=True, headers = plib.headers)
    
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
# --------------------start of test code--------------------
# pdf_url = 'https://www.sciencedirect.com/science/article/pii/S0896627320300052/pdfft?md5=3f0648c6385e6fae3a5a73b053903014&pid=1-s2.0-S0896627320300052-main.pdf'
# file_name = 'test_pdf'
# download_pdf(pdf_url, file_name)
# ---------------------end of test code---------------------


# get pmid from doi
def doi2pmid(doi):
    doi = str(doi).strip()

    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options, service=Service(GeckoDriverManager().install()))
            driver.get("https://www.pmid2cite.com/doi-to-pmid-converter")

            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Consent']"))).click()

            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#formInput"))).send_keys(str(doi).strip())
            except TimeoutException:
                print("Waiting for clicking consent timeout")
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Get PMID"]'))).click()
            except TimeoutException:
                print("Waiting for clicking button timeout")
            error_label = 1
        except:
            print("DOI to PMID transformation failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0

    try:
        my_elem = driver.find_element(By.CLASS_NAME, 'output').find_element(By.TAG_NAME, "a")
        pmid = str(my_elem.get_attribute("innerHTML")).strip()
    except:
        pmid = np.nan
    driver.quit()
    return pmid
# --------------------start of test code--------------------
# pmid = "35851953"
# doi = "10.1093/cercor/bhn229"
# pmid = doi2pmid(doi)
# print(pmid)
# ---------------------end of test code---------------------


# get doi from pmid
def pmid2doi(pmid):
    # request the webpage
    url = "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/"
    # proxies = plib.get_proxies()
    soup = plib.request_webpage(url)
    # print(soup)
    try:
        doi = soup.find_all("span", {"class": "identifier doi"})[0].find_all("a", {"class": "id-link"})[0].get_text().strip()
    except:
        doi = np.nan
    return doi
# --------------------start of test code--------------------
# pmid = "7424595"
# # doi = "10.1113/JP282626"
# doi = plib.pmid2doi(pmid)
# print(doi)
# ---------------------end of test code---------------------


# extract information from websites
websites = ["www.ncbi.nlm.nih.gov", "www.frontiersin.org", "www.sciencedirect.com", "onlinelibrary.wiley.com", 
            "springer.com", "europepmc.org", "biorxiv", "jneurosci", "orca.cardiff", "science", "thejns", "cambridge",
            "ahajournals", "mdpi", "pnas", "nature", "cell", "eneuro", "physiology",
            "ieee", "plos", "jstage.jst", "biomedcentral", "jamanetwork", "psycnet.apa", "jnnp.bmj", "degruyter",
            "karger", "pure.mpg", "elifesciences", "neurology", "pubs.asahq", "sagepub", "ekja", "liebertpub", "lww",
            "tandfonline", "aspetjournals", "oup", "royalsocietypublishing", "psychiatryonline", "jpn", "open.bu.edu",
            "agro.icm", "lib.wfu", "mirasmart", "jstor"]

# www.ncbi.nlm.nih.gov/pmc/
def www_ncbi_nlm_nih_gov(url):
    soup = plib.request_webpage(url)
    
    # extract information from loaded webpage
    try:
        doi = soup.find_all("span", {"class": "doi"})[0].find_all("a")[0].get_text().strip()
    except:
        doi = np.nan
    try:
        pmid = soup.find_all("div", {"class": "fm-citation-pmid"})[0].find_all("a")[0].get_text().strip()
    except:
        pmid = np.nan
    try:
        pmcid = soup.find_all("div", {"class": "fm-citation-pmcid"})[0].find_all("span")[1].get_text().strip()
    except:
        pmcid = np.nan
    try:
        title = soup.find_all("h1", {"class": "content-title"})[0].get_text().strip()
    except:
        title = np.nan
    try:
        abstract = soup.find_all("div", {"id": "abstract-1"})[0].find_all("p", {"class": "p p-first-last"})[0].get_text().strip()
    except:
        abstract = np.nan
    try:
        keywords = soup.find_all("div", {"id": "abstract-1"})[0].find_all("span", {"class": "kwd-text"})[0].get_text().strip()
    except:
        keywords = np.nan
    try:
        intro = ""
        elements = soup.find_all("div", {"id": "S1"})[0].find_all("p")
        for element in elements:
            intro = intro + element.get_text().strip()
    except:
        intro = np.nan
    try:
        pdf_link = soup.find_all("li", {"class": "pdf-link other_item"})[0].find_all("a")[0]["href"]
        pdf_link = "https://www.ncbi.nlm.nih.gov" + pdf_link
    except:
        pdf_link = np.nan

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "introduction": intro,
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10133512/"
# info = www_ncbi_nlm_nih_gov(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.frontiersin.org
def www_frontiersin_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(3)
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(By.XPATH, "//button[text()='Accept Cookies']")).click()
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # extract information from loaded webpage
    try:
        doi = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/div[1]/main/div/div/div/div[1]/div[2]/div[1]/a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[1]/main/div/div/div/div[2]/h1').text
    except:
        title = np.nan
    try:
        abstract = driver.find_element(By.CLASS_NAME, "JournalAbstract").find_element(By.TAG_NAME, "p").text
    except:
        abstract = np.nan
    keywords = np.nan
    try:
        intro = ""
        # Get the starting element
        after = driver.find_elements(By.TAG_NAME, 'h2')[1].find_elements(By.XPATH, './/following-sibling::p')
        # Get the ending element
        before = driver.find_elements(By.TAG_NAME, 'h2')[2].find_elements(By.XPATH, './/preceding-sibling::p')
        # Get the middle (= the intercept)
        middle = [elem for elem in after if elem in before]
        for element in middle:
            intro = intro + element.text
    except:
        intro = np.nan
    try:
        pdf_link = driver.find_element(By.XPATH, "//*[@id='download_article​']").get_attribute('href')
    except:
        pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "introduction": intro,
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://www.frontiersin.org/articles/10.3389/fncir.2015.00079/full"
# info = www_frontiersin_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.sciencedirect.com
def www_sciencedirect_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(5)
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(By.XPATH, "//button[text()='Accept Cookies']")).click()
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/article/div[3]/a[1]/span").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
    except:
        title = np.nan
    try:
        abstract = driver.find_element(By.ID, "abstracts").find_element(By.TAG_NAME, "p").text
    except:
        abstract = np.nan
    keywords = np.nan
    try:
        intro = ""
        # Get the starting element
        elements = driver.find_element(By.LINK_TEXT, 'Introduction').find_element(By.TAG_NAME, 'section').find_elements(By.XPATH, 'p')
        for element in elements:
            intro = intro + element.text
    except:
        intro = np.nan
    try:
        pdf_link = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/ul/li[1]/a").get_attribute('href')
    except:
        pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "introduction": intro,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.sciencedirect.com/science/article/pii/030439409512056A"
# info = www_sciencedirect_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# onlinelibrary.wiley.com
def onlinelibrary_wiley_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(3)
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(By.XPATH, "//button[text()='Accept Cookies']")).click()
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/main/div[1]/div/section/div/div/div/div[1]/article/div/div[1]/div[2]/div/div[6]/div[2]/a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
    except:
        title = np.nan
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//h3[text()='Abstract']").find_element(By.XPATH, 'following-sibling::div').find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text
    except:
        abstract = np.nan
    keywords = np.nan
    intro = np.nan
    try:
        pdf_link = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/main/div[1]/div/section/div/div/div/div[1]/article/div/div[1]/div[3]/nav/div/div[2]/div[1]/a").get_attribute('href')
    except:
        pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "introduction": intro,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://onlinelibrary.wiley.com/doi/abs/10.1002/cne.901980111"
# info = onlinelibrary_wiley_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# springer.com
def springer_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(3)
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(By.XPATH, "//button[text()='Accept Cookies']")).click()
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//abbr[text()='DOI']").find_element(By.XPATH, 'following-sibling::span').find_element(By.XPATH, 'following-sibling::span').text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
    except:
        title = np.nan
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//h2[text()='Abstract']").find_element(By.XPATH, 'following-sibling::div').find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text
    except:
        abstract = np.nan
    keywords = np.nan
    intro = np.nan
    try:
        pdf_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/aside/div[1]/div/div/a").get_attribute('href')
    except:
        pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "introduction": intro,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://link.springer.com/article/10.1007/PL00005713"
# info = springer_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


def extract_info_from_webpage(url):
    if url != url:
        raise Exception("The given url is np.nan")
    
    url = plib.get_final_redirected_url(url)
    source = url.split("://")[1].split("/")[0]
    
    for website in plib.websites:
        if website in source:
            # Get the function name by replacing "." with "_" and use globals() to call it
            func_name = website.replace(".", "_")
            func = globals().get(func_name)
            return func(url)
        else:
            print("The url:" + url + " is not included in our websites database yet!")
            return None
# --------------------start of test code--------------------
# websites = ["PMC", "frontiersin", "europepmc", "biorxiv", "jneurosci", "orca.cardiff", "science", "thejns", "cambridge",
#                 "wiley", "ahajournals", "mdpi", "sciencedirect", "pnas", "nature", "cell", "eneuro", "physiology", "springer",
#                 "ieee", "plos", "jstage.jst", "biomedcentral", "jamanetwork", "psycnet.apa", "jnnp.bmj", "degruyter",
#                 "karger", "pure.mpg", "elifesciences", "neurology", "pubs.asahq", "sagepub", "ekja", "liebertpub", "lww",
#                 "tandfonline", "aspetjournals", "oup", "royalsocietypublishing", "psychiatryonline", "jpn", "open.bu.edu",
#                 "agro.icm", "lib.wfu", "mirasmart", "jstor"]
# if len(websites) == len(set(websites)):
#     print("There are no duplicates in the list.")
# else:
#     print("There are duplicates in the list.")
# ---------------------end of test code---------------------

# --------------------start of test code--------------------
# url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10133512/"
# info = extract_info_from_webpage(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# get doi from url
def url2doi(url):
    if url != url:
        raise Exception("The url given is np.nan")
    
    url = str(url).strip()
    info = plib.extract_info_from_webpage(url) # dictionary
    if info == None:
        return np.nan
    else:
        return info["doi"]
# --------------------start of test code--------------------
# url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10133512/"
# doi = url2doi(url)
# print(doi)
# ---------------------end of test code---------------------