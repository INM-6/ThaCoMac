# import internal .py modules
import file_path_management as fpath
import public_library as plib
import parameters as params

# import packages
import os
import time
import numpy as np
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException


def extract_info_from_webpage(url, websites):
    if url != url:
        raise Exception("The given url is np.nan")
    # print(url)

    source = url.split("://")[1].split("/")[0]
    # print(source)

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
            func_name = website.replace(".", "_").replace("-", "_")
            # print(func_name)
            func = globals().get(func_name)
            # print(func)
            break
    # print(func)

    if func != None:
        # print(func)
        info = func(url)
    else:
        print("The given url is not from a supported website: ", url)
        raise Exception("Function does not exist for website:", url)
    
    if info["doi"] == info["doi"]:
        info["doi"] = info["doi"].lower()
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


# www.ncbi.nlm.nih.gov
def www_ncbi_nlm_nih_gov(url):
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
# url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2613515/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8328208/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8541979/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4855639/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3140205/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4362213/"
# # url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC48909/"
# info = www_ncbi_nlm_nih_gov(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# linkinghub.elsevier.com
def linkinghub_elsevier_com(url):
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
    driver = webdriver.Firefox(options=options)

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
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//li[@class='ViewPDF']/a").get_attribute('href')
    #     pdf_link = pdf_link.strip()
    # except:
    #     pdf_link = np.nan
    pdf_link = "://linkinghub.elsevier.com/"

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
# url = "https://linkinghub.elsevier.com/retrieve/pii/0006899395013385"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0891061898000222"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/S0165027017303631"
# # url = "https://linkinghub.elsevier.com/retrieve/pii/0006899376902067"
# info = linkinghub_elsevier_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# wiley.com
def wiley_com(url):
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
    driver = webdriver.Firefox(options=options)

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
# url = "https://onlinelibrary.wiley.com/doi/10.1002/cne.21155"
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
# # url = "https://onlinelibrary.wiley.com/doi/10.1002/9780470513545.ch4"
# info = wiley_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# link.springer.com
def link_springer_com(url):
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
    driver = webdriver.Firefox(options=options)

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
# info = link_springer_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# journals.physiology.org
def journals_physiology_org(url):
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
    driver = webdriver.Firefox(options=options)

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
# url = "https://journals.physiology.org/doi/10.1152/jn.1994.72.3.1270"
# # url = "https://journals.physiology.org/doi/10.1152/jn.1981.46.5.901"
# info = journals_physiology_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# # sciencedirect.com
# def sciencedirect_com(url):
#     # initialize
#     info = {
#         "doi": np.nan,
#         "pmid": np.nan,
#         "pmcid": np.nan,
#         "title": np.nan,
#         "abstract": np.nan,
#         "keywords": np.nan,
#         "pdf_link": np.nan
#     }

#     # set up the webdriver
#     os.environ['WDM_LOG'] = '0'
#     options = Options()
#     options.add_argument('--headless')
#     driver = webdriver.Firefox(options=options)

#     # load the webpage
#     error_label = 0
#     while(error_label == 0):
#         try:
#             driver.get(url)
#             time.sleep(10)
#             error_label = 1
#         except:
#             print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
#             time.sleep(5*60)
#             error_label = 0
    
#     # doi
#     try:
#         doi = driver.find_element(By.XPATH, "//a[@class='anchor doi anchor-default']/span").text.split("doi.org/")[1]
#         doi = doi.strip()
#     except:
#         doi = np.nan
#     if doi == doi:
#         doi = doi.lower()

#     # pmid, pmcid
#     pmid = np.nan
#     pmcid = np.nan

#     # title
#     try:
#         title = driver.find_element(By.TAG_NAME, 'h1').find_element(By.XPATH, "//span[@class='title-text']").text
#         title = title.strip()
#     except:
#         title = np.nan

#     # abstract
#     try:
#         abstract = ""
#         elems = driver.find_element(By.XPATH, "//div[@class='abstract author']").find_elements(By.TAG_NAME, "p")
#         for elem in elems:
#             abstract = abstract + elem.text + " "
#         abstract = abstract.strip()
#     except:
#         abstract = np.nan
    
#     # keywords
#     try:
#         keywords = ""
#         elements = driver.find_element(By.XPATH, "//div[@class='keywords-section']").find_elements(By.XPATH, "//div[@class='keyword']")
#         for element in elements:
#             keywords = keywords + element.find_element(By.TAG_NAME, "span").text + ", "
#         keywords = keywords.strip()
#     except:
#         keywords = np.nan

#     # pdf_link
#     try:
#         pdf_link = driver.find_element(By.XPATH, "//li[@class='ViewPDF']/a").get_attribute('href')
#         pdf_link = pdf_link.strip()
#     except:
#         pdf_link = np.nan

#     driver.quit()

#     info = {
#         "doi": doi,
#         "pmid": pmid,
#         "pmcid": pmcid,
#         "title": title,
#         "abstract": abstract,
#         "keywords": keywords,
#         "pdf_link": pdf_link
#     }

#     return info
# # --------------------start of test code--------------------
# # # url = "https://www.sciencedirect.com/science/article/pii/0006899378911034?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/0006899377904747?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/0165017379900080?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/000689937990132X?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/S2211124723008550?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/S0960982215014190?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/0006899375905296?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/S0166432805800166?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/000689938690925X?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/abs/pii/S1042368018302602?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/0006899367900042?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/0165017380900028?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/B9780124077942000092?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/0006899368900450?via%3Dihub"
# # # url = "https://www.sciencedirect.com/science/article/pii/S0006322310010036?via%3Dihub"
# # url = "https://www.sciencedirect.com/science/article/pii/0006899377907806?via%3Dihub"
# # info = sciencedirect_com(url)
# # print(info["doi"])
# # print(info["pmid"])
# # print(info["pmcid"])
# # print(info["title"])
# # print(info["abstract"])
# # print(info["keywords"])
# # print(info["pdf_link"])
# # ---------------------end of test code---------------------


# academic.oup.com
def academic_oup_com(url):
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
    driver = webdriver.Firefox(options=options)

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
# # url = "https://academic.oup.com/biolreprod/article/24/1/44/2766870"
# url = "https://academic.oup.com/cercor/article/22/6/1294/305674"
# # url = "https://academic.oup.com/brain/article/141/7/2142/5033684"
# info = academic_oup_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.cambridge.org
def www_cambridge_org(url):
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
    driver = webdriver.Firefox(options=options)

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
# # url = "https://www.cambridge.org/core/journals/thalamus-and-related-systems/article/abs/pathways-for-emotions-and-memory-i-input-and-output-zones-linking-the-anterior-thalamic-nuclei-with-prefrontal-cortices-in-the-rhesus-monkey/82C8F1BECABA367B0FBCD7E3EAACAAB3"
# # url = "https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/neuronal-organization-and-plasticity-in-adult-monkey-visual-cortex-immunoreactivity-for-microtubuleassociated-protein-2/B0317C6BF7C278292397F80735F19E54"
# # url = "https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/neuropeptide-ycontaining-neurons-are-situated-predominantly-outside-cytochrome-oxidase-puffs-in-macaque-visual-cortex/B66BA877CC63A9CA1AE958AC6433FC49"
# url = "https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/subcortical-connections-of-visual-areas-mst-and-fst-in-macaques/2E765908869A8B03AD1D566D488A6D19"
# info = www_cambridge_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# karger.com
def karger_com(url):
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
    driver = webdriver.Firefox(options=options)

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
        pdf_link = driver.find_element(By.XPATH, "//li[@class='toolbar-item item-with-dropdown item-pdf']/a").get_attribute('href')
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
# # url = "https://karger.com/sfn/article/60/1-3/104/291839/Action-of-the-Cerebello-Thalamo-Cortical"
# url = "https://karger.com/bbe/article/31/4/198/45901/Is-Binocular-Competition-Essential-for-Layer"
# info = karger_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# journals.lww.com
def journals_lww_com(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    keywords = np.nan
    pdf_link = "://journals.lww.com/"

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
# url = "https://journals.lww.com/pain/Abstract/1989/06000/A_dorsolateral_spinothalamic_tract_in_macaque.10.aspx"
# # url = "https://journals.lww.com/pain/Abstract/1994/03000/The_effect_oftrans_ACPD,_a_metabotropic_excitatory.2.aspx"
# # url = "https://journals.lww.com/pain/Abstract/2001/05000/Projections_from_the_marginal_zone_and_deep_dorsal.29.aspx"
# info = journals_lww_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.nature.com
def www_nature_com(url):
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
    driver = webdriver.Firefox(options=options)

    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        elems = driver.find_element(By.XPATH, "//abbr[@title='Digital Object Identifier']").find_elements(By.XPATH, "following-sibling::span")
        for elem in elems:
            text = elem.text
            if "doi.org" in text:
                break
        doi = text.split("doi.org/")[1]
    except:
        doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'c-article-title')]").text
    except:
        title = np.nan
    # title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='c-article-section__content']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    # abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[@class='c-pdf-download u-clear-both js-pdf-download']").find_element(By.TAG_NAME, 'a').get_attribute("href")
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
# # url = "https://www.nature.com/articles/387281a0"
# # url = "https://www.nature.com/articles/s41583-019-0212-7"
# url = "https://www.nature.com/articles/nn1318"
# # url = "https://www.nature.com/articles/nn1544"
# # url = "https://www.nature.com/articles/nrn3915"
# info = www_nature_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.XPATH, "a").text.split("DOI: ")[1]
    except:
        doi = np.nan

    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@property='name']").text
        title = title.strip()
    except:        
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//h2[text()='Abstract']").find_element(By.XPATH, "following-sibling::div").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[@class='info-panel__formats info-panel__item']").find_element(By.XPATH, "//a[@class='btn btn--slim btn-secondary']").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # pdf_link = np.nan

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
# # url = "https://www.science.org/doi/full/10.1126/science.282.5391.1117"
# # url = "https://www.science.org/doi/10.1126/science.7939688"
# url = "https://www.science.org/doi/10.1126/science.1109154"
# info = www_science_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.tandfonline.com
def www_tandfonline_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    try:
        doi = driver.find_element(By.XPATH, "//li[contains(@class, 'dx-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    pmid = np.nan
    pmcid = np.nan
    
    # title
    try:
        title = driver.find_element(By.TAG_NAME, "h1").find_element(By.XPATH, "//span[@class='NLM_article-title hlFld-title']").text
        title = title.strip()
    except:        
        title = np.nan
    
    # abstract
    try:
        elems = driver.find_elements(By.XPATH, "//div[@class='abstractSection abstractInFull']/p")
        for elem in elems:
            if len(elem.text) > 50:
                abstract = elem.text
                break
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstractKeywords']/div/div/ul").find_elements(By.TAG_NAME, "li")
        for elem in elems:
            keywords = keywords + elem.find_element(By.TAG_NAME, "a").text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@class='show-pdf']").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # pdf_link = np.nan

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
# # url = "https://www.tandfonline.com/doi/abs/10.1080/01616412.1985.11739692"
# # url = "https://www.tandfonline.com/doi/full/10.3109/00207458309148649"
# # url = "https://www.tandfonline.com/doi/full/10.3109/00207458408990681"
# url = "https://www.tandfonline.com/doi/full/10.3109/00207458009147579"
# info = www_tandfonline_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# journals.sagepub.com
def journals_sagepub_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@property='name']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//h2[text()='Abstract']").find_element(By.XPATH, "following-sibling::div").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//li[@class='collateral-middle']").find_element(By.XPATH, "//a[@title='PDF / ePub']").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://journals.sagepub.com/doi/full/10.1177/2398212819871205"
# # url = "https://journals.sagepub.com/doi/10.1177/0192623311436180"
# # url = "https://journals.sagepub.com/doi/10.1038/jcbfm.1983.2"
# url = "https://journals.sagepub.com/doi/10.1097/00004647-199810000-00010"
# # url = "https://journals.sagepub.com/doi/10.1177/107385840100700408"
# # url = "https://journals.sagepub.com/doi/10.1038/jcbfm.1992.141"
# info = journals_sagepub_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
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

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'meta-article-title')]").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        children = driver.find_element(By.XPATH, "//div[@class='article-full-text']").find_elements(By.XPATH, "*")
        # print(children[0].tag_name)
        # print(children[0].text)
        # print(children[1].tag_name)
        # print(children[1].text)
        # print(children[2].tag_name)
        # print(children[2].text)
        # print(children[3].tag_name)
        # print(children[3].text)
        div = []
        for child in children:
            # print(child.tag_name)
            if child.tag_name == 'div':
                div.append(children.index(child))
        # print(div)
        start = div[0] + 1
        end = div[1]

        for i in range(start, end):
            # print(children[i].text)
            abstract = abstract + children[i].text + " "
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    pdf_link = "://jamanetwork.com/"

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
# # url = "https://jamanetwork.com/journals/archneurpsyc/article-abstract/648966"
# # url = "https://jamanetwork.com/journals/jamapsychiatry/fullarticle/482591"
# # url = "https://jamanetwork.com/journals/jamaneurology/article-abstract/577288"
# url = "https://jamanetwork.com/journals/jamaneurology/article-abstract/567406"
# # url = "https://jamanetwork.com/journals/jamaophthalmology/fullarticle/412961"
# # url = "https://jamanetwork.com/journals/jamaneurology/article-abstract/574320"
# # url = "https://jamanetwork.com/journals/jamaophthalmology/article-abstract/632332"
# info = jamanetwork_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class, 'metadata-doi')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='page-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='section abstract']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        elem = driver.find_element(By.XPATH, "//ul[@class='tabs inline panels-ajax-tab']").find_element(By.XPATH, "//li[@class='last']/a")
        pdf_link = elem.get_attribute("href").strip()
    except:
        pdf_link = "np.nan"

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
# url = "https://www.jneurosci.org/content/11/8/2383"
# info = www_jneurosci_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
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
    
    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='page-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='section abstract']").find_elements(By.TAG_NAME, "p")
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@class='link-icon']").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://n.neurology.org/content/64/6/1014.short"
# # url = "https://n.neurology.org/content/64/6/1014"
# # url = "https://n.neurology.org/content/64/6/1014"
# url = "https://n.neurology.org/content/32/10/1198"
# # url = "https://n.neurology.org/content/22/9/998"
# info = neurology_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class,'cite-metadata-doi')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='page-title']").text
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='section abstract']").find_elements(By.TAG_NAME, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan
    
    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@class,'pdf-link link-icon')]").get_attribute("href")
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
# # url = "https://www.biorxiv.org/content/10.1101/398917v1.abstract"
# # url = "https://www.biorxiv.org/content/10.1101/2022.05.18.492367v2"
# # url = "https://www.biorxiv.org/content/10.1101/398917v1"
# url = "https://www.biorxiv.org/content/10.1101/2021.02.01.429141v2"
# info = www_biorxiv_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//span[@class='metadata--doi']").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()
    
    # pmid, pmcid
    try:
        pmid = driver.find_element(By.XPATH, "//span[contains(@class, 'metadata--pmid')]").text.split("PMID: ")[1]
    except:
        pmid = np.nan
    try:
        pmcid = driver.find_element(By.XPATH, "//span[contains(@class, 'metadata--pmcid')]").text.split("PMCID: ")[1]
    except:
        pmcid = np.nan
    
    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='article-metadata-title']").text
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//div[contains(@class, 'abstract')]").text
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan
    
    # pdf_link
    pdf_link = "://europepmc.org/"

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
# # url = "https://europepmc.org/article/MED/37298594"
# # url = "https://europepmc.org/article/med/8784824"
# url = "https://europepmc.org/article/med/823649"
# # url = "https://europepmc.org/article/med/4220147"
# info = europepmc_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# iovs.arvojournals.org
def iovs_arvojournals_org(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        elems = driver.find_element(By.XPATH, "//div[@class='ww-citation large-view-only']").find_elements(By.TAG_NAME, "span")
        for elem in elems:
            if "doi.org" in elem.text:
                doi = elem.text.split("doi.org/")[1]
                break
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
        title = driver.find_element(By.XPATH, "//div[@class='wi-article-title article-title-main']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.TAG_NAME, "p")
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@id='pdfLink']").get_attribute('data-article-url')
        pdf_link = "https://iovs.arvojournals.org/" + pdf_link
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
# # url = "https://iovs.arvojournals.org/article.aspx?articleid=2124655"
# url = "https://iovs.arvojournals.org/article.aspx?articleid=2659608"
# info = iovs_arvojournals_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='citation__title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstractSection abstractInFull']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    pdf_link = "://royalsocietypublishing.org/"

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
# # url = "https://royalsocietypublishing.org/doi/abs/10.1098/rstb.2002.1171"
# # url = "https://royalsocietypublishing.org/doi/10.1098/rspb.1972.0087"
# url = "https://royalsocietypublishing.org/doi/10.1098/rstb.1984.0021"
# info = royalsocietypublishing_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan
    
    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='citation__title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstractSection abstractInFull']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//span[contains(text(),'PDF')]").find_element(By.XPATH, "..").get_attribute("href")
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://ajp.psychiatryonline.org/doi/full/10.1176/appi.ajp.161.5.896"
# # url = "https://ajp.psychiatryonline.org/doi/10.1176/ajp.156.11.1709"
# url = "https://ajp.psychiatryonline.org/doi/full/10.1176/appi.ajp.158.9.1411"
# info = psychiatryonline_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# direct.mit.edu
def direct_mit_edu(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[@class='citation-doi']").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan
    
    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='wi-article-title article-title-main']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@class,'article-pdfLink')]").get_attribute("href")
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://direct.mit.edu/jocn/article/10/6/691/3328/The-von-Restorff-Effect-in-Visual-Object"
# # url = "https://direct.mit.edu/neco/article-abstract/15/4/735/6721/Modeling-Reverse-Phi-Motion-Selective-Neurons-in?redirectedFrom=fulltext"
# url = "https://direct.mit.edu/neco/article-abstract/24/7/1695/7782/Neural-Information-Processing-with-Feedback?redirectedFrom=fulltext"
# info = direct_mit_edu(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//dl[@class='doi c-List__items']/dd/span/a").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
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
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//span[contains(@class,'typography-body')]").find_element(By.XPATH, "//a[@title='Download PDF']").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://thejns.org/view/journals/j-neurosurg/86/1/article-p77.xml"
# url = "https://thejns.org/view/journals/j-neurosurg/41/2/article-p217.xml"
# info = thejns_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.annualreviews.org
def www_annualreviews_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[@class='article-details']/p[1]/a[1]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='article-header']").find_element(By.TAG_NAME, "h1").text
        title = title.strip()
    except:    
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstractSection abstractInFull']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='hlFld-KeywordText']/p[1]/kwd-group[1]").find_elements(By.XPATH, 'a')
        for elem in elems:
            keywords = keywords + elem.text + "; "
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@class='btn icon-pdf']").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://www.annualreviews.org/doi/10.1146/annurev.ne.02.030179.001303"
# # url = "https://www.annualreviews.org/doi/10.1146/annurev.ps.23.020172.002023"
# url = "https://www.annualreviews.org/doi/10.1146/annurev.neuro.23.1.127"
# info = www_annualreviews_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//span[contains(@class, 'cite-metadata-doi')]").text.split("doi.org/")[1]
    except:
        doi = np.nan
    if doi == doi:
        doi = doi.lower()

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='page-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='section abstract']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//ul[@class='tabs inline panels-ajax-tab']").find_element(By.XPATH, "//li[@class='last']").find_element(By.TAG_NAME, "a").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # pdf_link = np.nan

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
# # url = "https://jpet.aspetjournals.org/content/321/1/116.short"
# url = "https://jpet.aspetjournals.org/content/316/2/772"
# # url = "https://jpet.aspetjournals.org/content/319/2/561"
# # url = "https://jpet.aspetjournals.org/content/325/2/629"
# info = aspetjournals_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# jnm.snmjournals.org
def jnm_snmjournals_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    # try:
    #     doi = driver.find_element(By.XPATH, "//span[contains(@class, 'cite-metadata-doi')]").text.split("doi.org/")[1]
    # except:
    #     doi = np.nan
    # if doi == doi:
    #     doi = doi.lower()
    doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@id='page-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='section abstract']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@data-panel-name='jnl_snm_tab_pdf']").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://jnm.snmjournals.org/content/39/2/281.long"
# # url = "https://jnm.snmjournals.org/content/45/5/878.long"
# url = "https://jnm.snmjournals.org/content/36/7/1275.long"
# info = jnm_snmjournals_org(url)
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
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class, 'epub-section__doi__text')]").text.split("doi.org/")[1]
    except:
        doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='citation__title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstractSection abstractInFull']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//span[contains(text(),'PDF')]").find_element(By.XPATH,"..").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# url = "https://www.ahajournals.org/doi/full/10.1161/01.STR.0000087786.38997.9E"
# # url = "https://www.ahajournals.org/doi/10.1161/01.STR.6.1.42"
# # url = "https://www.ahajournals.org/doi/10.1161/01.STR.32.1.107"
# # url = "https://www.ahajournals.org/doi/10.1161/01.STR.29.11.2377"
# info = www_ahajournals_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# pubs.acs.org
def pubs_acs_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'article_header-doiurl')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[@class='article_header-title']").find_element(By.TAG_NAME, "span").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//p[@class='articleBody_abstractText']").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@class='button_primary pdf-button']").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # pdf_link = np.nan

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
# # url = "https://pubs.acs.org/doi/10.1021/jm030384e"
# url = "https://pubs.acs.org/doi/10.1021/jm301597s"
# # url = "https://pubs.acs.org/doi/10.1021/acs.molpharmaceut.8b01209"
# info = pubs_acs_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.thieme-connect.de
def www_thieme_connect_de(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").text.split("DOI: ")[1]
    except:
        doi = np.nan

    # pmid, pmcid
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
        abstract = driver.find_element(By.XPATH, "//h3[contains(text(),'Abstract')]").find_element(By.XPATH, "following-sibling::p").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = driver.find_element(By.XPATH, "//div[@class='articleKeywords')]").find_element(By.TAG_NAME, "p").text
        keywords = keywords.strip()
    except:
        keywords = np.nan
    # keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[@class='divPdfIconInNewline']").find_element(By.TAG_NAME, "a").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # pdf_link = "://www.thieme-connect.de/"

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
# # url = "https://www.thieme-connect.de/products/ejournals/abstract/10.1055/s-2007-973495"
# url = "https://www.thieme-connect.de/products/ejournals/abstract/10.1055/s-0031-1299170"
# info = www_thieme_connect_de(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# pubs.asahq.org
def pubs_asahq_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'citation-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    except:
        doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class,'article-title')]").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.TAG_NAME,"p")
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='content-metadata-topics']").find_elements(By.TAG_NAME, "a")
        for elem in elems:
            keywords = keywords + elem.text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan
    # keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@class,'article-pdfLink')]").get_attribute('href')
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://pubs.asahq.org/anesthesiology/article/116/2/372/13001/Ketamine-induced-Neuroapoptosis-in-the-Fetal-and"
# url = "https://pubs.asahq.org/anesthesiology/article/66/1/39/29057/The-Effects-of-Dextrose-Infusion-and-Head-Position"
# # url = "https://pubs.asahq.org/anesthesiology/article/98/5/1101/40355/Neural-Mechanism-of-Propofol-Anesthesia-in-Severe"
# info = pubs_asahq_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.ingentaconnect.com
def www_ingentaconnect_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    # try:
    #     doi = driver.find_element(By.XPATH, "//div[contains(@class, 'citation-doi')]").find_element(By.TAG_NAME, "a").text.split("doi.org/")[1]
    # except:
    #     doi = np.nan
    doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class,'abstract-heading')]").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//div[@id='Abst']").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='content-metadata-topics')]").find_elements(By.TAG_NAME, "a")
        for elem in elems:
            keywords = keywords + elem.text + "; "
        keywords = keywords.strip()
    except:
        keywords = np.nan
    # keywords = np.nan

    # pdf_link
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//ul[contains(@class,'right-col-download contain']").get_attribute('href')
    #     pdf_link = pdf_link.strip()
    # except:
    #     pdf_link = np.nan
    pdf_link = "://www.ingentaconnect.com/"

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
# url = "https://www.ingentaconnect.com/content/aalas/cm/2000/00000050/00000002/art00006;jsessionid=9jxpglps7nq4.x-ic-live-03"
# info = www_ingentaconnect_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ujms.net
def ujms_net(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[@class='item doi']").find_element(By.XPATH, "//span[@class='value']/a").text.split("doi.org/")[1]
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
        title = driver.find_element(By.XPATH, "//h1[@class='page_title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='item abstract']").find_elements(By.TAG_NAME, "p")
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[@class='obj_galley_link pdf']").get_attribute('href')
        pdf_link = pdf_link.strip()
        pdf_link = pdf_link.replace("view", "download")
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
# url = "https://ujms.net/index.php/ujms/article/view/6812"
# info = ujms_net(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# journals.biologists.com
def journals_biologists_com(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[@class='citation-doi']/a").text.split("doi.org/")[1]
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
        title = driver.find_element(By.XPATH, "//h1[contains(@class,'article-title')]").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//section[@class='abstract']").find_elements(By.XPATH, 'p')               
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        keywords = ""
        elems = driver.find_element(By.XPATH, "//div[@class='content-metadata-keywords']").find_elements(By.XPATH, 'a')               
        for elem in elems:
            keywords = keywords + elem.text + ", "
        keywords = keywords.strip()
    except:
        keywords = np.nan
    # keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//li[contains(@class,'item-pdf')]/a").get_attribute('href')
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
# url = "https://journals.biologists.com/dmm/article/7/8/1013/197/Introduction-of-the-human-AVPR1A-gene"
# info = journals_biologists_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.microbiologyresearch.org
def www_microbiologyresearch_org(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//a[contains(@class,'item-meta-data__doi')]").text.split("doi.org/")[1]
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
        title = driver.find_element(By.XPATH, "//h1[@class='item-meta-data__item-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[contains(@class,'article-abstract')]").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[contains(@class,'download-content--pdf')]/form").get_attribute('target')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    pdf_link = "://www.microbiologyresearch.org/"

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
# url = "https://www.microbiologyresearch.org/content/journal/jgv/10.1099/vir.0.79883-0"
# # url = "https://www.microbiologyresearch.org/content/journal/jmm/10.1099/jmm.0.001413"
# info = www_microbiologyresearch_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.imrpress.com
def www_imrpress_com(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        elems = driver.find_elements(By.XPATH, "//a[@class='link-color']")
        for elem in elems:
            if "doi.org" in elem.text:
                doi = elem.text.split("doi.org/")[1]
                break
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
        title = driver.find_element(By.XPATH, "//div[contains(@class,'article-detail-title')]").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//div[contains(@class,'abstract')]/abstract/p[1]").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        elems = driver.find_elements(By.XPATH, "//span[contains(@class,'keywordItem')]")
        for elem in elems:
            keywords = keywords + elem.find_elements(By.TAG_NAME,'div').text + ", "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@download,'.pdf')]").get_attribute('href')
        # for elem in elems:
        #     if "pdf" in elem.get_attribute('href'):
        #         pdf_link = elem.get_attribute('href')
        #         break
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
# url = "https://www.imrpress.com/journal/JIN/20/1/10.31083/j.jin.2021.01.334" 
# info = www_imrpress_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# journals.aps.org
def journals_aps_org(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//span[@class='doi-field']").text.split("doi.org/")[1]
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
        title = driver.find_element(By.TAG_NAME, "h3").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//section[contains(@class,'abstract')]").find_element(By.XPATH, "//div[@class='content']/p[1]").text             
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//div[@class='article-nav-actions']").find_element(By.XPATH, "//a[@class='small button']").get_attribute('href')
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
# url = "https://journals.aps.org/pre/abstract/10.1103/PhysRevE.106.054304"
# info = journals_aps_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# www.researchsquare.com
def www_researchsquare_com(url):
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
    driver = webdriver.Firefox(options=options)

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
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[@class='tw-border-t-2 tw-border-gray-100 tw-py-2']/p[1]").text.split("doi.org/")[1]
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
        title = driver.find_element(By.TAG_NAME, "h1").find_element(By.TAG_NAME, "p").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//div[@class='tw-pb-1']/div/span/div/p").text
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//span[contains(text(),'PDF')]/..").get_attribute('href')
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
# url = "https://www.researchsquare.com/article/rs-2921649/v1"
# info = www_researchsquare_com(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


'www.jstage.jst.go.jp'
def www_jstage_jst_go_jp(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
    
    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//div[@class='global-article-title']").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    # try:
    #     abstract = ""
    #     elems = driver.find_element(By.XPATH, "//div[@class='abstract-text']").find_elements(By.XPATH, 'p')
    #     for elem in elems:
    #         abstract = abstract + elem.text + " "
    #     abstract = abstract.strip()
    # except:
    #     abstract = np.nan
    abstract = np.nan
    
    # keywords
    # try:
    #     # keywords = ""
    #     keywords = driver.find_element(By.XPATH, "//strong[contains(text(),'Keywords:')]/..").text
    #     # for elem in elems:
    #     #     keywords = keywords + elem.text + ", "
    #     keywords = keywords.strip()
    # except:
    #     keywords = np.nan
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//span[contains(@class,'download-file')]/..").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
        pdf_link = np.nan
    # pdf_link = "://papers.ssrn.com/"

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
# info = www_jstage_jst_go_jp(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# ieeexplore.ieee.org
def ieeexplore_ieee_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            error_label = 1
        except:
            print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
            time.sleep(5*60)
            error_label = 0
    
    # doi
    try:
        doi = driver.find_element(By.XPATH, "//div[contains(@class, 'doi')]").find_element(By.TAG_NAME, "a").text
        doi = doi.strip()
    except:
        doi = np.nan

    # pmid, pmcid
    pmid = np.nan
    pmcid = np.nan

    # title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class,'document-title')]/span").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = driver.find_element(By.XPATH, "//div[@class='u-mb-1']/div[1]").text
        abstract = abstract.strip()
    except:
        abstract = np.nan\
    
    # keywords
    keywords = np.nan

    # pdf_link
    try:
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@class,'pdf-btn-link')]").get_attribute('href')
        pdf_link = pdf_link.strip()
    except:
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
    driver.quit

    return info
# --------------------start of test code--------------------
# # url = "https://ieeexplore.ieee.org/abstract/document/5333751"
# url = "https://ieeexplore.ieee.org/document/8067466"
# info = ieeexplore_ieee_org(url)
# print(info["doi"])
# print(info["pmid"])
# print(info["pmcid"])
# print(info["title"])
# print(info["abstract"])
# print(info["keywords"])
# print(info["pdf_link"])
# ---------------------end of test code---------------------


# papers.ssrn.com
def papers_ssrn_com(url):
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
    driver = webdriver.Firefox(options=options)

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
        title = driver.find_element(By.TAG_NAME, "h1").text
        title = title.strip()
    except:
        title = np.nan
    
    # abstract
    try:
        abstract = ""
        elems = driver.find_element(By.XPATH, "//div[@class='abstract-text']").find_elements(By.XPATH, 'p')
        for elem in elems:
            abstract = abstract + elem.text + " "
        abstract = abstract.strip()
    except:
        abstract = np.nan
    
    # keywords
    try:
        # keywords = ""
        keywords = driver.find_element(By.XPATH, "//strong[contains(text(),'Keywords:')]/..").text
        # for elem in elems:
        #     keywords = keywords + elem.text + ", "
        keywords = keywords.strip()
    except:
        keywords = np.nan

    # pdf_link
    # try:
    #     pdf_link = driver.find_element(By.XPATH, "//a[contains(@class,'button-link primary')]").get_attribute('href')
    #     pdf_link = pdf_link.strip()
    # except:
    #     pdf_link = np.nan
    pdf_link = "://papers.ssrn.com/"

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
# url = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3689615"
# info = papers_ssrn_com(url)
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
    driver = webdriver.Firefox(options=options)

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
def func_mirasmart_com(url):
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
# info = func_mirasmart_com(url)
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
def func_jpn_ca(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
# info = func_jpn_ca(url)
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
            driver = webdriver.Firefox(options=options)
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
            driver = webdriver.Firefox(options=options)
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


# liebertpub.com
def func_liebertpub_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
def func_ekja_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
# info = func_ekja_org(url)
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
            driver = webdriver.Firefox(options=options)
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
            driver = webdriver.Firefox(options=options)
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
def func_mpg_de(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
# info = func_mpg_de(url)
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
            driver = webdriver.Firefox(options=options)
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
def func_bmj_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
# info = func_bmj_com(url)
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
            driver = webdriver.Firefox(options=options)
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


# biomedcentral.com
def func_biomedcentral_com(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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


# plos.org
def func_plos_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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


# # www.architalbiol.org
# def www_architalbiol_org(url):
#     # os.environ['WDM_LOG'] = '0'
#     # options = Options()
#     # options.add_argument('--headless')
    
#     # # load the webpage
#     # error_label = 0
#     # while(error_label == 0):
#     #     try:
#     #         driver = webdriver.Firefox(options=options)
#     #         driver.get(url)
#     #         time.sleep(5)
#     #         error_label = 1
#     #     except:
#     #         print("Extracting content from:" + url + " failed, retrying... This might take longer than 5 minutes...")
#     #         time.sleep(5*60)
#     #         error_label = 0
    
#     # doi
#     doi = np.nan

#     # pmid, pmcid
#     pmid = np.nan
#     pmcid = np.nan

#     # title
#     # try:
#     #     title = driver.find_element(By.XPATH, "//div[@id='articleTitle']").find_element(By.TAG_NAME, "h3").text
#     #     title = title.strip()
#     # except:
#     #     title = np.nan
#     title = np.nan

#     # abstract
#     abstract = np.nan
    
#     # keywords
#     keywords = np.nan

#     pdf_link = "://www.architalbiol.org/"

#     info = {
#         "doi": doi,
#         "pmid": pmid,
#         "pmcid": pmcid,
#         "title": title,
#         "abstract": abstract,
#         "keywords": keywords,
#         "pdf_link": pdf_link
#     }
#     # driver.quit

#     return info
# # --------------------start of test code--------------------
# # # url = "http://www.architalbiol.org/index.php/aib/article/view/11423/"
# # url = "http://www.architalbiol.org/index.php/aib/article/view/140315/"
# # # url = "http://www.architalbiol.org/index.php/aib/article/view/122301/"
# # info = www_architalbiol_org(url)
# # print(info["doi"])
# # print(info["pmid"])
# # print(info["pmcid"])
# # print(info["title"])
# # print(info["abstract"])
# # print(info["keywords"])
# # print(info["pdf_link"])
# # ---------------------end of test code---------------------


# eneuro.org
def func_eneuro_org(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
            driver = webdriver.Firefox(options=options)
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
            driver = webdriver.Firefox(options=options)
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
            driver = webdriver.Firefox(options=options)
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


# orca.cardiff.ac.uk
def func_orca_cardiff_ac_uk(url):
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    # load the webpage
    error_label = 0
    while(error_label == 0):
        try:
            driver = webdriver.Firefox(options=options)
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
# info = func_orca_cardiff_ac_uk(url)
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
            driver = webdriver.Firefox(options=options)
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