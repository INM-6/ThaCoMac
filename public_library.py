# import packages
from bs4 import BeautifulSoup
import numpy as np
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
import string

# import internal modules
import file_path_management as fpath
import public_library as plib
import extract_info as extra_info
import parameters as params


# setting headers and proxies
# headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
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
    if response.status_code == 502:
        raise Exception("502 when requesting ", url)
    while(response.status_code != 200):
        print("Error", response.status_code, "when searching page:", url)
        time.sleep(5*60)
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
        df_new_row = pd.DataFrame(data=new_row, columns=columns)
        df_new_row.to_csv(csv_path, mode='a', index=False, header=False, escapechar='\\')
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
    try:
        response = requests.get(url, headers = plib.headers)
        while(True):
            if response.status_code == 404: # not found
                final_url = np.nan
                status_code = response.status_code
                print("Warning: 404 not found when getting final redirected url: from ", url)
                break
            elif response.status_code == 200 or 301 or 302 or 307 or 308:
                final_url = response.url
                status_code = response.status_code
                break
            elif response.status_code == 403:
                final_url = response.url
                status_code = response.status_code
                print("Warning: 403 forbidden when getting final redirected url: from ", url)
                break
            else:    
                print(response.status_code, "Retrying to get final redirected url...")
                # sleep for 5 minutes
                time.sleep(300)
                response = requests.get(url, headers = plib.headers)    
    except:
        final_url = np.nan
        status_code = np.nan
        print("Warning:", status_code, " when getting final redirected url: from ", url)
        # raise Exception("Error when getting final redirected url.")
    return final_url, status_code
# --------------------start of test code--------------------
# # url = "https://doi.org/10.1016/j.neuron.2020.01.005"
# url = "https://doi.org/10.1212/wnl.43.4.733"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0896627320300052"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9751134/"
# final_url, statua_code= get_final_redirected_url(url)
# # print(histo)
# print(final_url)
# print(statua_code)
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


# get pmid from title
def title2pmid(title):
    title = str(title).strip()
    words = title.split(" ")
    # print(words)
    term = ""
    for i in range(len(words)-1):
        term = term + words[i] + "+"
    term = term + words[-1]
    # print(term)
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + term
    # print(url)
    soup = plib.request_webpage(url)
    try:
        pmid = soup.find_all("section", {"class": "matching-citations search-results-list"})[0].find_all("span", {"class": "docsum-pmid"})[0].get_text()
    except:
        pmid = np.nan
    if pmid != pmid:
        try:
            pmid = soup.find_all("ul", {"id": "full-view-identifiers"})[0].find_all("span", {"class": "identifier pubmed"})[0].find_all("strong", {"class": "current-id"})[0].get_text()
        except:
            pmid = np.nan
    if pmid == pmid:
        pmid = str(pmid).strip()
    return pmid
# --------------------start of test code--------------------
# pmid = "21434138"
# title = "Thalamocortical connections of the parabelt auditory cortex in macaque monkeys"
# # https://pubmed.ncbi.nlm.nih.gov/?term=Thalamocortical+connections+of+the+parabelt+auditory+cortex+in+macaque+monkeys
# # title = "Independence and merger of thalamocortical channels within macaque monkey primary visual cortex: anatomy of interlaminar projections"
# # title = "… of GABAB antagonist [3H] CGP 62349 binding in the rhesus monkey thalamus and basal ganglia and the influence of lesions in the reticular thalamic nucleus"
# pmid = title2pmid(title)
# print(pmid)
# ---------------------end of test code---------------------


# get pmid from doi
def doi2pmid(doi):
    doi = str(doi).strip()
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + doi
    soup = plib.request_webpage(url)
    try:
        pmid_cadidate = soup.find_all("span", {"class": "identifier pubmed"})[0].find_all("strong", {"class": "current-id"})[0].get_text()
    except:
        pmid_cadidate = np.nan
    if pmid_cadidate == pmid_cadidate:
        pmid_cadidate = str(pmid_cadidate).strip()
        doi_validate, a = plib.pmid2doi_pmcid(pmid_cadidate)
        if doi_validate.strip().lower() == doi.strip().lower():
            pmid = str(pmid_cadidate).strip()
        else:
            print("doi and doi_cadidate are not consistent!")
            pmid = np.nan
    else:
        pmid = np.nan
    if pmid == pmid:
        pmid = str(pmid).strip()
    return pmid
# --------------------start of test code--------------------
# # pmid = "35851953"
# doi = "10.1016/j.neuroimage.2006.07.032"
# pmid = doi2pmid(doi)
# print(pmid)
# ---------------------end of test code---------------------


# get doi from pmid
def pmid2doi_pmcid(pmid):
    # request the webpage
    url = "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/"
    # proxies = plib.get_proxies()
    soup = plib.request_webpage(url)
    if soup == None:
        return np.nan, np.nan
    # print(soup)
    try:
        doi = soup.find_all("span", {"class": "identifier doi"})[0].find_all("a", {"class": "id-link"})[0].get_text().strip()
        # print(doi)
    except:
        doi = np.nan
    try:
        pmcid = soup.find_all("span", {"class": "identifier pmc"})[0].find_all("a", {"class": "id-link"})[0].get_text().strip()
    except:
        pmcid = np.nan
    if doi == doi:
        doi = str(doi).strip().lower()
    if pmcid == pmcid:
        pmcid = str(pmcid).strip()
    return doi, pmcid
# --------------------start of test code--------------------
# pmid = "7424595"
# # doi = "10.1113/JP282626"
# doi = plib.pmid2doi(pmid)
# print(doi)
# ---------------------end of test code---------------------

# get doi and pmid from pmcid
def pmcid2doi_pmid(pmcid):
    url = "https://www.ncbi.nlm.nih.gov/pmc/articles/" + pmcid + "/"
    soup = plib.request_webpage(url)
    try:
        doi = soup.find_all("span", {"class": "doi"})[0].find_all("a")[0].get_text().strip()
    except:
        doi = np.nan
    try:
        pmid = soup.find_all("div", {"class": "fm-citation-pmid"})[0].find_all("a")[0].get_text().strip()
    except:
        pmid = np.nan
    if doi == doi:
        doi = str(doi).strip()
    if pmid == pmid:
        pmid = str(pmid).strip()
    return doi, pmid
# --------------------start of test code--------------------
# pmcid = "PMC2753250"
# doi, pmid = pmcid2doi_pmid(pmcid)
# print(doi)
# print(pmid)
# ---------------------end of test code---------------------

# process text
def process_text(text, lower):
    # keep only printable ascii characters
    # text = ''.join(ch for ch in text if 0 <= ord(ch) <= 126)
    text = ''.join(ch for ch in text if ch in string.printable)
    # text = ''.join(ch for ch in text if ord(ch) <= 126)
    # text = text.encode('ascii', errors='ignore').decode('ascii') 
    # text.encode('ascii', errors='ignore')

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip() 

    # convert to lower case
    if lower == True:
        text = text.lower()
    elif lower == False:
        pass
    else:
        raise ValueError('lower must be assigned True or False.')

    return text
# --------------------start of test code--------------------
# text = "   Vision for-actio,,,,,n:   thalamic and cortical inputs,,$ in the macaque and human thalamus Miguel Ángel García-Cabezas,aBeatriz Rico,a,b Miguel Ángel Sánchez-González,aand Carmen Cavadaa,⁎ aDepartamento de Anatomía, Histología y Neurociencia, Facultad de Medicina, Universidad Autónoma de Madrid, C/Arzobispo Morcillo s/n, 28029 Madrid, Spain bInstituto de Neurociencias de Alicante, Universidad Miguel Hernández-CSIC, 03550 Sant Joan d ’Alacant, Spain Received 19 April 2006; revised 8 June 2006; accepted 11 July 2006 Available online 30 November 2006 We recently defined the thalamic dopaminergic system in primates; it arises from numerous dopaminergic cell groups and selectively targetsnumerous thalamic nuclei. Given the central position of the thalamus in subcortical and cortical interplay, and the functional relevance of dopamine neuromodulation in the brain, detailing dopamine dis-tribution in the thalamus should supply important information. Tothis end we performed immunohistochemistry for dopamine and the dopamine transporter in the thalamus of macaque monkeys and humans to generate maps, in the stereotaxic coronal plane, of thedistribution of dopaminergic axons. The dopamine innervation of the thalamus follows the same pattern in both species and is most dense in midline limbic nuclei, the mediodorsal and lateral posteriorassociation nuclei, and in the ventral lateral and ventral anteriormotor nuclei. This distribution suggests that thalamic dopamine has a prominent role in emotion, attention, cognition and complex somatosensory and visual processing, as well as in motor control.Most thalamic dopaminergic axons are thin and varicose and targetboth the neuropil and small blood vessels, suggesting that, besides neuronal modulation, thalamic dopamine may have a direct influence on microcirculation. The maps provided here should be a usefulreference in future experimental and neuroimaging studies aiming atclarifying the role of the thalamic dopaminergic system in health and in conditions involving brain dopamine, including Parkinson ’s disease, drug addiction and schizophrenia.© 2006 Elsevier Inc. All rights reserved. Keywords: Dopamine; Thalamus; Monkey; Human; Primate; Dopamine transporter; Parkinson; Schizophrenia; AddictionIntroduction The thalamus is made up of multiple nuclei relaying information from subcortical centers or from other cortices to the cerebral cortex (Sherman and Guillery, 2005 ), as well as the striatum, the nucleus accumbens and the amygdala ( Steriade et al., 1997 ). In addition to specific subcortical and cortical afferents, the primate thalamus receives axons containing the neuromodulators acetylcholine (Heckers et al., 1992 ), histamine ( Manning et al., 1996 ), serotonin (Morrison and Foote, 1986; Lavoie and Parent, 1991 ), and the catecholamines adrenaline ( Rico and Cavada, 1998a ), noradrenaline (Morrison and Foote, 1986; Ginsberg et al., 1993 ) and dopamine (Sánchez-González et al., 2005 ). Until recently, the existence of significant dopamine innervation in the primate thalamus has been largely ignored, probably becausedopamine innervation of the rodent thalamus is very scant(Groenewegen, 1988; Papadopoulos and Parnavelas, 1990 ). However, fragmentary data scattered through the literature endorse the presence of dopamine innervation in the primate thalamus.Postmortem biochemical studies showed the presence of dopamine in the thalamus of macaques ( Brown et al., 1979; Goldman-Rakic and Brown, 1981; Pifl et al., 1990, 1991 ) and human subjects ( Oke and Adams, 1987 ). Later, receptor binding and in situ hybridization analyses detected the presence of dopamine D2-like ( Joyce et al., 1991; Kessler et al., 1993; Hall et al., 1996; Langer et al., 1999;Rieck et al., 2004 ) and D3-like receptors ( Gurevich and Joyce, 1999 ) in several human thalamic nuclei. Positron emission tomography (PET) radioligand studies have also demonstratedthe presence of the dopamine transporter (DAT) ( Wang et al., 1995; Halldin et al., 1996; Helfenbein et al., 1999; Brownell et al., 2003 ) and of D2-like receptors ( Farde et al., 1997; Langer et al., 1999; Okubo et al., 1999; Brownell et al., 2003; Rieck et al., 2004 ) in the human and macaque thalamus. In the course of PET studies focusing on schizophrenia, D2- and D3-like radioligand binding was also found in the thalamus of control subjects ( Talvik et al., 2003; Yasuno et al., 2004 ). Finally, an immunohistochemical study using anti-DAT antibodies detected the presence of dopaminergic www.elsevier.com/locate/ynimg NeuroImage 34 (2007) 965 –984 ⁎Corresponding author. Fax: +34 91 497 53 15. E-mail address: carmen.cavada@uam.es (C. Cavada). Available online on ScienceDirect (www.sciencedirect.com). 1053-8119/$ - see front matter © 2006 Elsevier Inc. All rights reserved. doi:10.1016/j.neuroimage.2006.07.032"
# text = process_text(text, lower=True)
# print(text)
# ---------------------end of test code---------------------
