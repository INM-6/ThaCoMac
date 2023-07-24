# self-written public library

# import internal .py modules
import file_path_management as fpath
import public_library as plib

# import packages
import csv
import pandas as pd
from PyPDF2 import PdfReader
import requests
import time


# setting headers and proxies
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
http_proxy  = "http://103.148.39.50:83"
https_proxy = "https://47.254.158.115:20201"
proxy = {
    "http": http_proxy, 
    "https": https_proxy
}
# end of setting header and proxies


# clear a file given file path
def clear_file(file_path):
    with open(file_path, 'w') as f:
        f.truncate()
        f.close()
# --------------------start of test code--------------------
# file_path = ''
# clear_file(file_path)
# ---------------------end of test code---------------------
# end of clear_file


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
# end of ask_ChatGPT


# add a new row to a given .csv file
def add_row_to_csv(csv_path, new_row, columns):
    df_new_row = pd.DataFrame(data = new_row, columns = columns)
    with open(csv_path, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            df_new_row.to_csv(csv_path, index = False, header = True)
        else:
            df_new_row.to_csv(csv_path, mode = 'a', index = False, header = False, encoding='utf-8-sig', sep = ",")
# --------------------start of test code--------------------
# add_rows_to_csv(path_potential, info_json, columns)
# ---------------------end of test code---------------------
# end of add_row_to_csv


# extract text from given .pdf file
def pdf2text(pdf_path):
    # creating a pdf reader object
    reader = PdfReader(pdf_path)
    
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
# end of pdf2text

  
# get the final url when the given url is redirected once or even multiple times
def get_final_redirected_url(url):
    r = requests.get(url, headers = plib.headers) 
    while(response.status_code != 200):
                # sleep for 5 minutes
                time.sleep(300)
                response = requests.get(url, headers = plib.headers)
    final_url = r.url
    return final_url
# --------------------start of test code--------------------
url = ''
final_url = get_final_redirected_url(url)
print(final_url)
# ---------------------end of test code---------------------
# end of get_final_redirected_url