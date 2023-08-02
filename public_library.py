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
    if response.status_code == 403:
        final_url = url
    if response.status_code == 404:
        final_url = np.nan
    while(response.status_code != 200 and response.status_code != 403 and response.status_code != 404):
        print(response.status_code)     
        # sleep for 5 minutes
        time.sleep(300)
        response = requests.get(url, headers = plib.headers)
    if response.status_code == 200:
        final_url = response.url
    # history = response.history
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
                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/form/button"))).click()
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
