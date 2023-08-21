# import internal .py modules
import file_path_management as fpath
import public_library as plib
import extract_info_from_webpage as extra_info
import parameters as params

# import packages
import os
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_info_from_webpage(url, websites):
    if url != url:
        raise Exception("The given url is np.nan")
    print(url)
    source = url.split("://")[1].split("/")[0]
    print(source)
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }
    
    for website in websites:
        func = None
        if website in source:
            # Get the function name by replacing "." with "_" and use globals() to call it
            func_name = "func_" + website.replace(".", "_")
            func = globals().get(func_name)
            break
    if func != None:
        info = func(url)
    else:
        print("The given url is not from a supported website: ", url)
        raise Exception("Function does not exist for website:", url)
    return info
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


# ncbi.nlm.nih.gov
def func_ncbi_nlm_nih_gov(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # load the webpage
    soup = plib.request_webpage(url)
    time.sleep(5)
    
    # extract information from loaded webpage
    # doi
    try:
        doi = soup.find_all("span", {"class": "doi"})[0].find_all("a")[0].get_text().strip()
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    # print(doi)

    # pmid
    try:
        pmid = soup.find_all("div", {"class": "fm-citation-pmid"})[0].find_all("a")[0].get_text().strip()
        pmid = pmid.strip()
    except:
        pmid = np.nan
    # print(pmid)
    if pmid == pmid:
        pmid = str(int(pmid)).strip()
    # pmcid
    try:
        pmcid = soup.find_all("div", {"class": "fm-citation-pmcid"})[0].find_all("span")[1].get_text().strip()
        pmcid = pmcid.strip()
    except:
        pmcid = np.nan
    # print(pmcid)

    # title
    try:
        title = soup.find_all("h1", {"class": "content-title"})[0].get_text().strip()
        title = title.strip()
    except:
        title = np.nan
    # print(title)

    # abstract
    try:
        abstract = ""
        elems = soup.find(lambda tag: tag.name=="h2" and ("Abstract" in tag.text or "ABSTRACT" in tag.text or "Summary" in tag.text or "SUMMARY" in tag.text)).find_next_sibling("div").find_all("p")
        for elem in elems:
            abstract = abstract + " " + elem.get_text().strip()
        abstract = abstract.strip()
    except:
        try:
            abstract = ""
            elems = soup.find(lambda tag: tag.name=="h2" and ("Abstract" in tag.text or "ABSTRACT" in tag.text or "Summary" in tag.text or "SUMMARY" in tag.text)).find_next_siblings("p")
            for elem in elems:
                abstract = abstract + " " + elem.get_text().strip()
            abstract = abstract.strip()
        except:
            abstract = np.nan
    # print(abstract) 

    # keywords
    try:
        elems = soup.find(lambda tag:tag.name=="strong" and "Keywords" in tag.text)
        keywords = elems.findNext('span').get_text().strip()
        keywords = keywords.strip()
    except:
        keywords = np.nan
    # print(keywords)

    # pdf_link
    try:
        pdf_link = soup.find_all("li", {"class": "pdf-link other_item"})[0].find_all("a")[0]["href"]
        pdf_link = "https://www.ncbi.nlm.nih.gov" + pdf_link
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # print(pdf_link)

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10133512/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2613515/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8328208/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8541979/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4855639/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3140205/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4362213/"
# url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC48909/"
# info = func_ncbi_nlm_nih_gov(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


def func_elsevier_com(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(10)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[@class='anchor doi anchor-default']/span").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').find_element(By.XPATH, "//span[@class='title-text']").text
        title = title.strip()
    except:
        title = np.nan

    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstract author']").find_elements(By.TAG_NAME, "p")
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elements = driver.find_element(By.XPATH, "//div[@class='keywords-section']").find_elements(By.XPATH, "//div[@class='keyword']")
        for element in elements:
            keywords = keywords + element.find_element(By.TAG_NAME, "span").text + ", "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//li[@class='ViewPDF']/a").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://linkinghub.elsevier.com/retrieve/pii/0006899395013385"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0891061898000222"
# # url = "https://www.sciencedirect.com/science/article/pii/S0006322310010036?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0165027017303631?via%3Dihub#abs0010"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0165027017303631"
# # url = "https://www.sciencedirect.com/science/article/pii/S0079612308626783?via%3Dihub"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/0006899376902067"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899378911034?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899377904747?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0165017379900080?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/000689937990132X?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S2211124723008550?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0960982215014190?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899375905296?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0166432805800166?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/000689938690925X?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/abs/pii/S1042368018302602?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899367900042?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0165017380900028?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/B9780124077942000092?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899368900450?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0006322310010036?via%3Dihub"
# url = "https://www.sciencedirect.com/science/article/pii/0006899377907806?via%3Dihub"
# info = func_elsevier_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# sciencedirect.com
def func_sciencedirect_com(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(10)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[@class='anchor doi anchor-default']/span").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').find_element(By.XPATH, "//span[@class='title-text']").text
        title = title.strip()
    except:
        title = np.nan

    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstract author']").find_elements(By.TAG_NAME, "p")
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elements = driver.find_element(By.XPATH, "//div[@class='keywords-section']").find_elements(By.XPATH, "//div[@class='keyword']")
        for element in elements:
            keywords = keywords + element.find_element(By.TAG_NAME, "span").text + ", "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//li[@class='ViewPDF']/a").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://linkinghub.elsevier.com/retrieve/pii/0006899395013385"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0891061898000222"
# # url = "https://www.sciencedirect.com/science/article/pii/S0006322310010036?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0165027017303631?via%3Dihub#abs0010"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0165027017303631"
# # url = "https://www.sciencedirect.com/science/article/pii/S0079612308626783?via%3Dihub"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/0006899376902067"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899378911034?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899377904747?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0165017379900080?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/000689937990132X?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S2211124723008550?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0960982215014190?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899375905296?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0166432805800166?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/000689938690925X?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/abs/pii/S1042368018302602?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899367900042?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0165017380900028?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/B9780124077942000092?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899368900450?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/S0006322310010036?via%3Dihub"
# url = "https://www.sciencedirect.com/science/article/pii/0006899377907806?via%3Dihub"
# info = func_sciencedirect_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# wiley.com
def func_wiley_com(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(10)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[@class='epub-doi']").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='citation__title']").text
        title = title.strip()
    except:
        try:
            title = driver.find_element(By.XPATH, "//h2[@class='citation__title']").text
            title = title.strip()
        except:
            title = np.nan
    
    # abstract
    try:
        abstract = ""
        try:
            elems = driver.find_element(By.XPATH, "//h3[text()='Abstract' or text()='ABSTRACT' or text()='Summary' or text()='SUMMARY']").find_element(By.XPATH, "following-sibling::div").find_elements(By.XPATH, 'p')
        except:
            elems = driver.find_element(By.XPATH, "//h2[text()='Abstract' or text()='ABSTRACT' or text()='Summary' or text()='SUMMARY']").find_element(By.XPATH, "following-sibling::div").find_elements(By.XPATH, 'p')                
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@title='ePDF']").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://onlinelibrary.wiley.com/doi/abs/10.1002/cne.901980111"
# # url = "https://onlinelibrary.wiley.com/doi/abs/10.1002/cne.902890211"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.21440"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.21155"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1096-9861(19981019)400:2%3C271::AID-CNE8%3E3.0.CO;2-6"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.902360304"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.902820107"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1096-9861(19990726)410:2%3C211::AID-CNE4%3E3.0.CO;2-X"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.902940314"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.901990104"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1096-9861(19981019)400:2%3C271::AID-CNE8%3E3.0.CO;2-6"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.902360304"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.24389"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1096-9861(19960805)371:4%3C513::AID-CNE2%3E3.0.CO;2-7"
# # url = "https://nyaspubs.onlinelibrary.wiley.com/doi/full/10.1196/annals.1300.030"
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.23436"
# url = "https://onlinelibrary.wiley.com/doi/10.1002/9780470513545.ch4"
# info = func_wiley_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# springer.com
def func_springer_com(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(10)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//abbr[text()='DOI']").find_element(By.XPATH, 'following-sibling::span').find_element(By.XPATH, 'following-sibling::span').text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        try:
            elems = driver.find_element(By.XPATH, "//div[@id='Abs1-content']").find_elements(By.TAG_NAME, 'p')
        except:
            elems = driver.find_element(By.XPATH, "//div[@id='Abs1_2-content']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//ul[@class='c-article-subject-list']").find_elements(By.TAG_NAME, 'li')
        for elem in elems:
            keywords = keywords + elem.find_element(By.TAG_NAME, 'span').text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[@class='c-pdf-container']/div[1]/a[1]").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://link.springer.com/article/10.1007/PL00005713"
# # url = "https://link.springer.com/article/10.1007/BF00231734"
# # url = "https://link.springer.com/article/10.1007/BF00231444"
# # url = "https://link.springer.com/article/10.1007/BF00237252"
# # url = "https://link.springer.com/article/10.1007/BF00237252"
# # url = "https://link.springer.com/chapter/10.1007/978-1-4419-0754-7_2"
# info = func_springer_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# physiology.org
def func_physiology_org(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(10)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'citation__title')]").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstractSection abstractInFull']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//ul[@id='download_Pop']/li[1]/a[1]").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://journals.physiology.org/doi/abs/10.1152/jn.1963.26.5.775"
# # url = "https://journals.physiology.org/doi/10.1152/jn.1994.72.3.1270"
# url = "https://journals.physiology.org/doi/10.1152/jn.1981.46.5.901"
# info = func_physiology_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# oup.com
def func_oup_com(url):
    # initialize
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

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi, pmid, pmcid
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'ww-citation-primary')]/a").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.TAG_NAME, "h1").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='kwd-group']").find_elements(By.TAG_NAME, 'a')
        for elem in elems:
            keywords = keywords + elem.text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@class='al-link pdf article-pdfLink']").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://academic.oup.com/biolreprod/article/24/1/44/2766870"
# # url = "https://academic.oup.com/cercor/article/22/6/1294/305674"
# # url = "https://academic.oup.com/brain/article/141/7/2142/5033684"
# info = func_oup_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# cambridge.org
def func_cambridge_org(url):
    # initialize
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

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi, pmid, pmcid
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(text(), 'DOI')]/a/span").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.TAG_NAME, "h1").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstract']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='keywords']").find_element(By.XPATH, "//div[@class='row keywords__pills']").find_elements(By.TAG_NAME, 'a')
        for elem in elems:
            keywords = keywords + elem.find_element(By.TAG_NAME, 'span').text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan
    
    # # introduction
    # try:
    #     intro = ""
    #     elements = driver.find_elements(By.TAG_NAME, "h2")
    #     for element in elements:
    #         if "Introduction" in element.text:
    #             ele_paren = element.find_element(By.XPATH, "..")
    #             intros = ele_paren.find_elements(By.TAG_NAME, "p")
    #             for intro_ele in intros:
    #                 intro = intro + intro_ele.text + " "
    #             break
    #     intro = intro.strip()
    # except:
    #     intro = np.nan
    # intro = np.nan

    # pdf_link
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//a[@class='al-link pdf article-pdfLink']").get_attribute('href')
    #     pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://www.cambridge.org/core/journals/thalamus-and-related-systems/article/abs/pathways-for-emotions-and-memory-i-input-and-output-zones-linking-the-anterior-thalamic-nuclei-with-prefrontal-cortices-in-the-rhesus-monkey/82C8F1BECABA367B0FBCD7E3EAACAAB3"
# # url = "https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/neuronal-organization-and-plasticity-in-adult-monkey-visual-cortex-immunoreactivity-for-microtubuleassociated-protein-2/B0317C6BF7C278292397F80735F19E54"
# # url = "https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/neuropeptide-ycontaining-neurons-are-situated-predominantly-outside-cytochrome-oxidase-puffs-in-macaque-visual-cortex/B66BA877CC63A9CA1AE958AC6433FC49"
# # url = "https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/subcortical-connections-of-visual-areas-mst-and-fst-in-macaques/2E765908869A8B03AD1D566D488A6D19"
# info = func_cambridge_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# karger.com
def func_karger_com(url):
    # initialize
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

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi, pmid, pmcid
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'citation-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.TAG_NAME, "h1").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='content-metadata-keywords']").find_elements(By.TAG_NAME, 'a')
        for elem in elems:
            keywords = keywords + elem.text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[@class='pdf-notice']/div/a").get_attribute('href')
        pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://karger.com/sfn/article/54-55/1-8/114/303620/Structural-and-Connectional-Diversity-of-the"
# # url = "https://karger.com/sfn/article/60/1-3/70/291859/Cerebello-and-Pallido-Thalamic-Pathways-to-Areas-6"
# url = "https://karger.com/sfn/article/60/1-3/104/291839/Action-of-the-Cerebello-Thalamo-Cortical"
# # url = "https://karger.com/bbe/article/31/4/198/45901/Is-Binocular-Competition-Essential-for-Layer"
# info = func_karger_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# lww.com
def func_lww_com(url):
    # initialize
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

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(5)
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All Cookies')]"))).click()
            time.sleep(2)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi, pmid, pmcid
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'ej-journal-info')]").text.split("DOI: ")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='ejp-article-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='ejp-article-text-abstract']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    # try:
    #     keywords = ""
    #     elems = driver.find_element(By.XPATH, "//div[@class='ejp-article-text-abstract']").find_elements(By.TAG_NAME, 'a')
    #     for elem in elems:
    #         keywords = keywords + elem.text + "; "
    #     keywords = keywords.strip()
    # except:
    #     keywords = np.nan
    keywords = np.nan
    
    # # introduction
    # try:
    #     intro = ""
    #     elements = driver.find_elements(By.TAG_NAME, "h2")
    #     for element in elements:
    #         if "Introduction" in element.text:
    #             ele_paren = element.find_element(By.XPATH, "..")
    #             intros = ele_paren.find_elements(By.TAG_NAME, "p")
    #             for intro_ele in intros:
    #                 intro = intro + intro_ele.text + " "
    #             break
    #     intro = intro.strip()
    # except:
    #     intro = np.nan

    # pdf_link
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//button[contains(text(), 'PDF')]").click()
    #     driver.switch_to_window(driver.window_handles[-1])
    #     pdf_link = driver.current_url
    #     pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# # url = "https://journals.lww.com/neuroreport/Fulltext/2018/04010/Change_of_information_represented_by_thalamic.5.aspx"
# # url = "https://journals.lww.com/pain/Abstract/1989/06000/A_dorsolateral_spinothalamic_tract_in_macaque.10.aspx"
# # url = "https://journals.lww.com/pain/Abstract/1994/03000/The_effect_oftrans_ACPD,_a_metabotropic_excitatory.2.aspx"
# url = "https://journals.lww.com/pain/Abstract/2001/05000/Projections_from_the_marginal_zone_and_deep_dorsal.29.aspx"
# info = func_lww_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# bmj.com
def func_bmj_com(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver.get(url)
            time.sleep(10)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[@class='panel-pane pane-custom pane-2']/div[1]/p[1]/a[1]").text.split("doi.org/")[1]
        doi = doi.strip()
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    # # pdf_link
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//li[@class='ViewPDF']/a").get_attribute('href')
    #     pdf_link = pdf_link.strip()
    # except:
    #     pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://jnnp.bmj.com/content/37/7/765.short"
# info = func_bmj_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# nature.com
def func_nature_com(url):
    # initialize
    info = {
        "doi": np.nan,
        "pmid": np.nan,
        "pmcid": np.nan,
        "title": np.nan,
        "abstract": np.nan,
        "keywords": np.nan,
        "pdf_link": np.nan
    }

    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()

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
    
    # doi
    try:
        spans = driver.find_element(By.XPATH, "//abbr[@title='Digital Object Identifier']").find_elements(By.XPATH,'following-sibling::span')
        for span in spans:
            if "doi.org" in span.text:
                doi = span.text.split("doi.org/")[1]
                break
    except:
        doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    # try:
    #     title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    # except:
    #     title = np.nan
    title = np.nan
    
    # abstract
    # try:
    #     abstract = ""
    #     elems = driver.find_element(By.XPATH, "//div[@class='ejp-article-text-abstract']").find_elements(By.TAG_NAME, 'p')
    #     for elem in elems:
    #         abstract = abstract + elem.text + " "
    #     abstract = abstract.strip()
    # except:
    #     abstract = np.nan
    abstract = np.nan
    
    # keywords
    # try:
    #     keywords = ""
    #     elems = driver.find_element(By.XPATH, "//div[@class='ejp-article-text-abstract']").find_elements(By.TAG_NAME, 'a')
    #     for elem in elems:
    #         keywords = keywords + elem.text + "; "
    #     keywords = keywords.strip()
    # except:
    #     keywords = np.nan
    keywords = np.nan

    # pdf_link
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//button[contains(text(), 'PDF')]").click()
    #     driver.switch_to_window(driver.window_handles[-1])
    #     pdf_link = driver.current_url
    #     pdf_link = pdf_link.strip()
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
        "pdf_link": pdf_link
    }

    return info
# --------------------start of test code--------------------
# url = "https://www.nature.com/articles/387281a0"
# info = func_nature_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jstor.org
def func_jstor_org(url):
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
# info = func_jstor_org(url)
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


# wfu.edu
def func_wfu_edu(url):
    doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    return info
# --------------------start of test code--------------------
# url = "https://wakespace.lib.wfu.edu/handle/10339/37434"
# info = func_wfu_edu(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# agro.icm.edu.pl
def func_agro_icm_edu_pl(url):
    doi = "10.1002/cne.902820107"
    pmid = "2468699"
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    return info
# --------------------start of test code--------------------
# url = "https://agro.icm.edu.pl/agro/element/bwmeta1.element.agro-3eefdf76-4976-454b-b43f-a2312ad21b00"
# info = func_agro_icm_edu_pl(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
def func_bu_edu(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://open.bu.edu/handle/2144/12127"
# info = func_bu_edu(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# psych.ac.cn
def func_psych_ac_cn(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://journal.psych.ac.cn/adps/EN/abstract/abstract3663.shtml"
# info = func_psych_ac_cn(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# psychiatryonline.org
def func_psychiatryonline_org(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://ajp.psychiatryonline.org/doi/full/10.1176/appi.ajp.161.5.896"
# info = func_psychiatryonline_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# royalsocietypublishing.org
def func_royalsocietypublishing_org(url):
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
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
url = "https://royalsocietypublishing.org/doi/abs/10.1098/rstb.2002.1171"
info = func_royalsocietypublishing_org(url)
print(info["doi"])
print(info["pmid"])
print(info["pmcid"])
print(info["title"])
print(info["abstract"])
print(info["keywords"])
print(info["pdf_link"])
# ---------------------end of test code---------------------


# tandfonline.com
def func_tandfonline_com(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.tandfonline.com/doi/abs/10.1080/01616412.1985.11739692"
# info = func_tandfonline_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# aspetjournals.org
def func_aspetjournals_org(url):
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
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://jpet.aspetjournals.org/content/321/1/116.short"
# info = func_aspetjournals_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# liebertpub.com
def func_liebertpub_com(url):
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
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.liebertpub.com/doi/abs/10.1089/brain.2013.0143"
# info = func_liebertpub_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
def func_sagepub_com(url):
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
        doi = driver.find_element(By.XPATH, "//div[@class='doi']").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://journals.sagepub.com/doi/full/10.1177/2398212819871205"
# info = func_sagepub_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
def fun_neurology_org(url):
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
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://n.neurology.org/content/64/6/1014.short"
# # url = "https://n.neurology.org/content/64/6/1014"
# info = fun_neurology_org(url)
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
def func_elifesciences_org(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://elifesciences.org/articles/37325"
# info = func_elifesciences_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# frontiersin.org
def func_frontiersin_org(url):
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
        t = driver.find_element(By.XPATH, "//div[@class='header-bar-three']").find_element(By.TAG_NAME, "a").text
        if "doi.org/" in t:
            doi = t.split("doi.org/")[1]
        else:
            doi = np.nan
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.frontiersin.org/articles/10.3389/fnbeh.2014.00073/full"
# info = func_frontiersin_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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


# degruyter.com
def func_degruyter_com(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.degruyter.com/document/doi/10.1515/REVNEURO.2007.18.6.417/html"
# info = func_degruyter_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
        doi = driver.find_element(By.XPATH, "//div[@class='panel-pane pane-custom pane-2']/div[1]/p/a").text.split("doi.org/")[1]
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
def func_psycnet_apa_org(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://psycnet.apa.org/record/1972-06153-001"
# info = func_psycnet_apa_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jamanetwork.com
def func_jamanetwork_com(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://jamanetwork.com/journals/archneurpsyc/article-abstract/648966"
# info = func_jamanetwork_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# biomedcentral.com
def func_biomedcentral_com(url):
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
        eles = driver.find_element(By.XPATH, "//abbr[@title='Digital Object Identifier']").find_elements(By.XPATH, "following-sibling::span")
        doi = np.nan
        for ele in eles:
            if "doi.org/" in ele.text:
                doi = ele.text.split("doi.org/")[1]
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://bmcneurosci.biomedcentral.com/articles/10.1186/1471-2202-6-67#article-info"
# info = func_biomedcentral_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jstage.jst.go.jp
def func_jstage_jst_go_jp(url):
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
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.jstage.jst.go.jp/article/pjab1945/43/8/43_8_822/_article/-char/ja/"
# info = func_jstage_jst_go_jp(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# plos.org
def func_plos_org(url):
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
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0000848"
# info = func_plos_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ieee.org
def func_ieee_org(url):
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
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://ieeexplore.ieee.org/abstract/document/5333751"
# info = func_ieee_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# eneuro.org
def func_eneuro_org(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.eneuro.org/content/5/3/ENEURO.0060-18.2018.abstract"
# info = func_eneuro_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# cell.com
def func_cell_com(url):
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
    # try:
    #     title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    # except:
    #     title = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(18)30205-5"
# info = func_cell_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# func.pnas.org
def func_pnas_org(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.pnas.org/doi/abs/10.1073/pnas.1008054107"
# info = func_pnas_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# mdpi.com
def func_mdpi_com(url):
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
        doi = driver.find_element(By.XPATH, "//div[@class='bib-identity']/a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.mdpi.com/1422-0067/24/11/9643"
# info = func_mdpi_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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


# thejns.org
def func_thejns_org(url):
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
        doi = driver.find_element(By.XPATH, "//dl[@class='doi c-List__items']/dd/span/a").text.split("doi.org/")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://thejns.org/view/journals/j-neurosurg/86/1/article-p77.xml"
# info = func_thejns_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# science.org
def func_science_org(url):
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
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.XPATH, "a").text.split("DOI: ")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan
    title = np.nan
    abstract = np.nan
    keywords = np.nan
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.science.org/doi/full/10.1126/science.282.5391.1117"
# info = func_science_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
        doi = driver.find_element(By.XPATH, "//div[@class='ep_summary_content_main']/div[1]/a").text.split("doi.org/")[1]
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


# jneurosci.org
def func_jneurosci_org(url):
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
    pdf_link = np.nan

    driver.quit()

    info = {
        "doi": doi,
        "pmid": pmid,
        "pmcid": pmcid,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://www.jneurosci.org/content/30/25/8650.short"
# url = "https://www.jneurosci.org/content/20/10/3884.short"
# info = func_jneurosci_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# europepmc.org
def func_europepmc_org(url):
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
        doi = driver.find_element(By.XPATH, "//a[@id='article--doi--link-metadataSec']").text
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
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
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://europepmc.org/article/MED/37298594"
# info = func_europepmc_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# biorxiv.org
def func_biorxiv_org(url):
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
        "pdf_link": pdf_link
    }
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.biorxiv.org/content/10.1101/398917v1.abstract"
# info = func_biorxiv_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------