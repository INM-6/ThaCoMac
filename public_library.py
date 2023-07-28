# self-written public library

# import internal .py modules
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


# setting headers and proxies
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
def get_proxies():
    with open(fpath.proxy_list) as f:
        proxy_list = f.readlines()
        # print(proxy_list)
        i = random.randint(0, len(proxy_list)-1)
    proxies = { 
        "http": "http://" + proxy_list[i].strip()
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
                # sleep for 5 minutes
                time.sleep(300)
                response = requests.get(url, headers = plib.headers)
    final_url = response.url
    history = response.history
    return final_url, history
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