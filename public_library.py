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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import re


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
            driver = webdriver.Chrome(options, service=Service(ChromeDriverManager().install()))
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
        pmid  = driver.find_element(By.XPATH, "//p[@class='output']").find_element(By.TAG_NAME, "a").text.strip()
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
websites = ["ncbi.nlm.nih.gov", "frontiersin.org", "sciencedirect.com", "wiley.com", 
            "springer.com", "europepmc.org", "www.biorxiv.org", "www.jneurosci.org", "orca.cardiff.ac.uk", "www.science.org", 
            "thejns.org", "www.cambridge.org", "www.ahajournals.org", "www.mdpi.com", "www.pnas.org", "www.nature.com", 
            "www.cell.com", "www.eneuro.org", "physiology.org", "ieee.org", "plos.org", "jstage.jst.go.jp", "biomedcentral.com", 
            "jamanetwork.com", "psycnet.apa.org", "bmj.com", "degruyter.com", "karger.com", "lifesciences.org", 
            "neurology_org", "asahq.org", "sagepub.com", "ekja.org", "liebertpub.com", "lww.com", "tandfonline.com", 
            "aspetjournals.org", "oup.com", "royalsocietypublishing.org", "psychiatryonline.org", "jpn.ca", "bu.edu",
            "agro.icm.edu.pl", "lib.wfu.edu", "mirasmart.com", "jstor.org", "mpg.de"]


def extract_info_from_webpage(url):
    if url != url:
        raise Exception("The given url is np.nan")
    
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "introduction": np.nan,
        "pdf_link": np.nan
    }

    url = plib.get_final_redirected_url(url)
    source = url.split("://")[1].split("/")[0]
    
    for website in plib.websites:
        if website in source:
            # Get the function name by replacing "." with "_" and use globals() to call it
            func_name = website.replace(".", "_")
            func = globals().get(func_name)
            info = func(url)
            break
        else:
            continue
    return info
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

    if info["doi"] == info["doi"]:
        return info["doi"]
    elif info["pmid"] == info["pmid"]:
        return pmid2doi(info["pmid"])
    else:
        return np.nan
# --------------------start of test code--------------------
# url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10133512/"
# doi = url2doi(url)
# print(doi)
# ---------------------end of test code---------------------


# jstor.org
def jstor_org(url):
    doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.jstor.org/stable/82698"
# info = jstor_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# mirasmart.com
def mirasmart_com(url):
    doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://submissions.mirasmart.com/ISMRM2022/Itinerary/Files/PDFFiles/2200.html"
# info = mirasmart_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# lib.wfu.edu
def lib_wfu_edu(url):
    doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://wakespace.lib.wfu.edu/handle/10339/37434"
# info = lib_wfu_edu(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# agro.icm.edu.pl
def agro_icm_edu_pl(url):
    doi = "10.1002/cne.902820107"
    pmid = "2468699"
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://agro.icm.edu.pl/agro/element/bwmeta1.element.agro-3eefdf76-4976-454b-b43f-a2312ad21b00"
# info = agro_icm_edu_pl(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jpn.ca
def jpn_ca(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    doi = np.nan
    pmid = "18982171" 
    pmcid = "PMC2575763"
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.jpn.ca/content/33/6/489/tab-article-info"
# info = jpn_ca(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# bu.edu
def bu_edu(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://open.bu.edu/handle/2144/12127"
# info = bu_edu(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# psychiatryonline.org
def psychiatryonline_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://ajp.psychiatryonline.org/doi/full/10.1176/appi.ajp.161.5.896"
# info = psychiatryonline_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# royalsocietypublishing.org
def royalsocietypublishing_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        # doi = np.nan
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
        # for elem in elems:
        #     if "doi.org/" in elem.text:
        #         doi = elem.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://royalsocietypublishing.org/doi/abs/10.1098/rstb.2002.1171"
# info = royalsocietypublishing_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# oup.com
def oup_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'ww-citation-primary')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://academic.oup.com/brain/article/141/7/2142/5033684"
# info = oup_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# tandfonline.com
def tandfonline_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        # doi = np.nan
        doi = driver.find_element(By.XPATH, "//li[contains(@class, 'dx-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
        # for elem in elems:
        #     if "doi.org/" in elem.text:
        #         doi = elem.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.tandfonline.com/doi/abs/10.1080/01616412.1985.11739692"
# info = tandfonline_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# aspetjournals.org
def aspetjournals_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class, 'highwire-cite-metadata-doi highwire-cite-metadata')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://jpet.aspetjournals.org/content/321/1/116.short"
# info = aspetjournals_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# lww.com
def lww_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        # doi = np.nan
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'ej-journal-info')]").text.split("DOI: ")[1]
        # for elem in elems:
        #     if "doi.org/" in elem.text:
        #         doi = elem.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://journals.lww.com/pain/Citation/1981/08001/Potentials_evoked_in_thalamic_nuclei_by_dental.298.aspx"
# info = lww_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# liebertpub.com
def liebertpub_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        # doi = np.nan
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
        # for elem in elems:
        #     if "doi.org/" in elem.text:
        #         doi = elem.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.liebertpub.com/doi/abs/10.1089/brain.2013.0143"
# info = liebertpub_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ekja.org
def ekja_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        # doi = np.nan
        doi = driver.find_element(By.XPATH, "//div[contains(@id, 'include_journal')]").find_element(By.XPATH, "//table[contains(@class, 'front')]").find_element(By.XPATH, "//td[contains(@class, 'front')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
        # for elem in elems:
        #     if "doi.org/" in elem.text:
        #         doi = elem.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://ekja.org/journal/view.php?number=4940"
# info = ekja_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# sagepub.com
def sagepub_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://journals.sagepub.com/doi/full/10.1177/2398212819871205"
# info = sagepub_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# asahq.org
def asahq_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'citation-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://pubs.asahq.org/anesthesiology/article/116/2/372/13001/Ketamine-induced-Neuroapoptosis-in-the-Fetal-and"
# info = asahq_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# neurology.org
def neurology_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class, 'highwire-cite-metadata-doi highwire-cite-metadata')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://n.neurology.org/content/64/6/1014.short"
# info = neurology_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# elifesciences.org
def elifesciences_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'doi__link')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://elifesciences.org/articles/37325"
# info = elifesciences_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# mpg.de
def mpg_de(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://pure.mpg.de/pubman/faces/ViewItemOverviewPage.jsp?itemId=item_1790170"
# info = mpg_de(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# karger.com
def karger_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'citation-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://karger.com/sfn/article/54-55/1-8/114/303620/Structural-and-Connectional-Diversity-of-the"
# info = karger_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# degruyter.com
def degruyter_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.degruyter.com/document/doi/10.1515/REVNEURO.2007.18.6.417/html"
# info = degruyter_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# bmj.com
def bmj_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "/html/body/div[3]/section[2]/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div[7]/div/div/div[2]/div/div/div/div[7]/div/p/a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://jnnp.bmj.com/content/37/7/765.short"
# info = bmj_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# psycnet.apa.org
def psycnet_apa_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = np.nan
        elems = driver.find_element(By.XPATH, "//div[contains(@class, 'citation-text')]").find_elements(By.TAG_NAME, "a")
        for elem in elems:
            if "doi.org/" in elem.text:
                doi = elem.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://psycnet.apa.org/record/1972-06153-001"
# info = psycnet_apa_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jamanetwork.com
def jamanetwork_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = np.nan
        elems = driver.find_element(By.XPATH, "//div[contains(@class, 'meta-citation-wrap')]").find_elements(By.TAG_NAME, "span")
        for elem in elems:
            if "doi:" in elem.text:
                doi = elem.text.split("doi:")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://jamanetwork.com/journals/archneurpsyc/article-abstract/648966"
# info = jamanetwork_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# biomedcentral.com
def biomedcentral_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        eles = driver.find_element(By.XPATH, "//abbr[contains(@title, 'Digital Object Identifier')]").find_elements(By.XPATH, "following-sibling::span")
        doi = np.nan
        for ele in eles:
            if "doi.org/" in ele.text:
                doi = ele.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://bmcneurosci.biomedcentral.com/articles/10.1186/1471-2202-6-67#article-info"
# info = biomedcentral_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jstage.jst.go.jp
def jstage_jst_go_jp(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class, 'doi-icn')]").find_element(By.XPATH, "following-sibling::a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.jstage.jst.go.jp/article/pjab1945/43/8/43_8_822/_article/-char/ja/"
# info = jstage_jst_go_jp(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# plos.org
def plos_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//li[contains(@id, 'artDoi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0000848"
# info = plos_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ieee.org
def ieee_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'u-pb-1 stats-document-abstract-doi')]").find_element(By.TAG_NAME, "a").text
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://ieeexplore.ieee.org/abstract/document/5333751"
# info = ieee_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# physiology.org
def physiology_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Chrome(options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://journals.physiology.org/doi/abs/10.1152/jn.1963.26.5.775"
# info = physiology_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.eneuro.org
def www_eneuro_org(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class, 'highwire-cite-metadata-doi highwire-cite-metadata')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.eneuro.org/content/5/3/ENEURO.0060-18.2018.abstract"
# info = www_eneuro_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.cell.com
def www_cell_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'article-header__doi__value')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(18)30205-5"
# info = www_cell_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.nature.com
def www_nature_com(url):
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
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        elements = driver.find_element(By.XPATH, "//abbr[contains(@title, 'Digital Object Identifier')]").find_elements(By.XPATH, 'following-sibling::span')
        for element in elements:
            if "doi.org/" in element.text:
                doi = element.text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.nature.com/articles/387281a0"
# info = www_nature_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.pnas.org
def www_pnas_org(url):
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
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.pnas.org/doi/abs/10.1073/pnas.1008054107"
# info = www_pnas_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.mdpi.com
def www_mdpi_com(url):
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
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'bib-identity')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.mdpi.com/1422-0067/24/11/9643"
# info = www_mdpi_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.ahajournals.org
def www_ahajournals_org(url):
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
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.ahajournals.org/doi/full/10.1161/01.STR.0000087786.38997.9E"
# info = www_ahajournals_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.cambridge.org
def www_cambridge_org(url):
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
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi-data')]").find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'span').text.split("doi.org/")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.cambridge.org/core/journals/thalamus-and-related-systems/article/abs/ascending-inputs-to-the-presupplementary-motor-area-in-the-macaque-monkey-cerebello-and-pallidothalamocortical-projections/7385CA29F413D1E0EFD21261B0010306"
# info = www_cambridge_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# thejns.org
def thejns_org(url):
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
        doi = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div/div[3]/div/div/div/div/dl[3]/dd/span/a").text.split("doi.org/")[1]
        # doi = driver.find_element(By.CLASS_NAME, "//a[contains(@class, 'c-Button--link')]").find_element(By.XPATH, 'a').text
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://thejns.org/view/journals/j-neurosurg/86/1/article-p77.xml"
# info = thejns_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.science.org
def www_science_org(url):
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
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.XPATH, "a").text.split("DOI: ")[1]
        # doi = driver.find_element(By.CLASS_NAME, "//span[contains(@class, 'metadata--doi')]").find_element(By.XPATH, 'a').text
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.science.org/doi/full/10.1126/science.282.5391.1117"
# info = www_science_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# orca.cardiff.ac.uk
def orca_cardiff_ac_uk(url):
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
        doi = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[4]/div/div[4]/div/a").text.split("doi.org/")[1]
        # doi = driver.find_element(By.CLASS_NAME, "//span[contains(@class, 'metadata--doi')]").find_element(By.XPATH, 'a').text
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://orca.cardiff.ac.uk/id/eprint/11456/"
# info = orca_cardiff_ac_uk(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.jneurosci.org
def www_jneurosci_org(url):
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
        doi = driver.find_element(By.XPATH, "//span[@class='highwire-cite-metadata-doi highwire-cite-metadata']").text.split("doi.org/")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    intro = np.nan
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
# url = "https://www.jneurosci.org/content/30/25/8650.short"
# info = www_jneurosci_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ncbi.nlm.nih.gov
def ncbi_nlm_nih_gov(url):
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
# info = ncbi_nlm_nih_gov(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# frontiersin.org
def frontiersin_org(url):
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
# info = frontiersin_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ciencedirect.com
def sciencedirect_com(url):
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
# info = sciencedirect_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# wiley.com
def wiley_com(url):
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
# info = wiley_com(url)
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


# europepmc.org
def europepmc_org(url):
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
        doi = driver.find_element(By.XPATH, "//a[@id='article--doi--link-metadataSec']").text
        # doi = driver.find_element(By.CLASS_NAME, "//span[contains(@class, 'metadata--doi')]").find_element(By.XPATH, 'a').text
    except:
        doi = np.nan
    try:
        pmid = driver.find_element(By.XPATH, "//span[contains(@class, 'metadata--pmid')]").text.split("PMID: ")[1]
    except:
        pmid = np.nan
    try:
        pmcid = driver.find_element(By.XPATH, "//span[contains(@class, 'metadata--pmcid')]").text.split("PMCID: ")[1]
    except:
        pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='article--current--title']").text
    except:
        title = np.nan
    try:
        abstract = driver.find_element(By.XPATH, "//div[contains(@class, 'abstract')]").text
    except:
        abstract = np.nan
    keywords = np.nan
    intro = np.nan
    # try:
    #     element = driver.find_element(By.XPATH, "//span[contains(@id, 'open_pdf')]")
    #     element.click
    #     time.sleep(3)
    #     driver.switch_to.window(driver.window_handles[1])
    #     time.sleep(3)
    #     pdf_link = driver.current_url
    # except:
    #     pdf_link = np.nan
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
# url = "https://europepmc.org/article/MED/37298594"
# info = europepmc_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------

# www.biorxiv.org
def www_biorxiv_org(url):
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
        doi = driver.find_element(By.XPATH, "//span[@class='highwire-cite-metadata-doi highwire-cite-metadata']").text.split("doi.org/")[1]
        # doi = driver.find_element(By.CLASS_NAME, "//span[contains(@class, 'metadata--doi')]").find_element(By.XPATH, 'a').text
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='page-title']").text
    except:
        title = np.nan
    try:
        abstract = driver.find_element(By.XPATH, "//h2[contains(., 'ABSTRACT')]").find_element(By.XPATH, 'following-sibling::p').text
    except:
        abstract = np.nan
    keywords = np.nan
    intro = np.nan
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@class, 'article-dl-pdf-link link-icon')]").get_attribute("href")
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
# url = "https://www.biorxiv.org/content/10.1101/398917v1.abstract"
# info = www_biorxiv_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["introduction"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------