# import internal modules
import file_path_management as fpath
import public_library as plib
import extract_info
import parameters as params

# import external modules
import requests
import re
import os
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

# rename downloaded pdf
def rename_pdf(ind, pdf_folder, time_to_wait=60):
    newname = str(ind) + ".pdf"
    time_counter = 0
    filename = max([f for f in os.listdir(pdf_folder)], key=lambda xa: os.path.getctime(os.path.join(pdf_folder,xa)))
    while '.part' in filename:
        # print(filename)
        # print(time_counter)
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Waited too long for file to download')
        filename = max([f for f in os.listdir(pdf_folder)], key=lambda xa: os.path.getctime(os.path.join(pdf_folder,xa)))
    filename = max([f for f in os.listdir(pdf_folder)], key=lambda xa: os.path.getctime(os.path.join(pdf_folder,xa)))
    # filename is not a number
    if re.match(filename, "[0-9]+"):
        print('yes')
        raise Exception('File name is not a number')
    else:
        os.rename(os.path.join(pdf_folder, filename), os.path.join(pdf_folder, newname))


# download and rename pdf
def download_and_rename_pdf(pdf_url, doi, ind, pdf_folder):
    if pdf_url != pdf_url:
        print("pdf_url is nan")
        raise Exception("pdf_url is nan")
    
    pdf_source = pdf_url.split("://")[1].split("/")[0]
    func_name = None
    func = None

    # download_by_request
    if func == None:
        for website in params.download_by_request:
            if website in pdf_source:
                # Get the function name by replacing "." with "_" and use globals() to call it
                func_name = "download_by_request"
                # print(func_name)
                func = globals().get(func_name)
                # print(func)
                break

    # download_pdf_by_button
    if func == None:
        for website in params.download_pdf_by_button:
            if website in pdf_source:
                # Get the function name by replacing "." with "_" and use globals() to call it
                func_name = "download_pdf_by_button"
                # print(func_name)
                func = globals().get(func_name)
                # print(func)
                break
        
    # download_from
    if func == None:
        for website in params.download_from:
            if website in pdf_source:
                # Get the function name by replacing "." with "_" and use globals() to call it
                func_name = "download_from_" + website.replace(".", "_")
                # print(func_name)
                func = globals().get(func_name)
                # print(func)
                break
    
    # 'linkinghub.elsevier.com'
    if func == None and pdf_source == 'linkinghub.elsevier.com':
        # Get the function name by replacing "." with "_" and use globals() to call it
        func_name = "download_from_linkinghub_elsevier_com"
        # print(func_name)
        func = globals().get(func_name)
        # print(func)

    # 'journals.physiology.org'
    if func == None and pdf_source == 'journals.physiology.org':
        # Get the function name by replacing "." with "_" and use globals() to call it
        func_name = "download_from_journals_physiology_org"
        # print(func_name)
        func = globals().get(func_name)
        # print(func)
    
    # download_not_possible
    if func == None:
        for website in params.download_not_possible:
            if website in pdf_source:
                # Get the function name by replacing "." with "_" and use globals() to call it
                func_name = "download_not_possible"
                # print(func_name)
                func = globals().get(func_name)
                # print(func)
                break
    
    # download_pdf_by_a
    if func == None:
        for website in params.download_pdf_by_a:
            if website in pdf_source:
                # Get the function name by replacing "." with "_" and use globals() to call it
                func_name = "download_pdf_by_a"
                # print(func_name)
                func = globals().get(func_name)
                # print(func)
                break
    
    # download_pdf_by_driver
    if func == None:
        for website in params.download_pdf_by_driver:
            if website in pdf_source:
                # Get the function name by replacing "." with "_" and use globals() to call it
                func_name = "download_pdf_by_driver"
                # print(func_name)
                func = globals().get(func_name)
                # print(func)
                break
    
    if func_name == "download_from_linkinghub_elsevier_com":
        return func(doi, ind, pdf_folder)
    elif func != None:
        return func(pdf_url, ind, pdf_folder)
    else:
        print("The given url is not from a supported website: ", pdf_url)
        raise Exception("Function does not exist for website:", pdf_url)
# --------------------start of test code--------------------
# pdf_url = "https://journals.physiology.org/doi/pdf/10.1152/jn.2001.85.1.219"
# pdf_url = "https://journals.physiology.org/doi/10.1152/jn.2001.85.1.219"
# ind = 10
# pdf_folder = "/home/hou/myProjects/litera_pdfs"
# download_and_rename_pdf(pdf_url, ind, pdf_folder)
# ---------------------end of test code---------------------


# # .pdf
# pdf_download_by_request = [
#     'aspetjournals.org', 'citeseerx.ist.psu.edu', 'www.nature.com', 'karger.com', 'ahuman.org', 'ahuman.org', 'www.researchsquare.com',
#     'link.springer.com', 'www.ijpp.com', 'www.ijpp.com', 'www.cell.com', 'www.bu.edu', 'www.ncbi.nlm.nih.gov', 
#     'www.thieme-connect.de', 'deepblue.lib.umich.edu', 'bpb-us-e1.wpmucdn.com', 'www.researchgate.net', 'ieeexplore.ieee.org',
#     'zsp.com.pk', 'journals.biologists.com', 'journals.aps.org', 'academic.oup.com', 'www.biorxiv.org', 'enpubs.faculty.ucdavis.edu',
#     'n.neurology.org', 'ruor.uottawa.ca', 'www.jstage.jst.go.jp', 'synapse.koreamed.org', 'www.jneurosci.org', 'pubs.asahq.org',
#     'biomedcentral.com', 'direct.mit.edu', 'jnm.snmjournals.org'
#  ]
def download_by_request(url, ind, pdf_folder):
    try:
        file_name = str(ind) + ".pdf"
        time.sleep(2)
        response = requests.get(url, headers=plib.headers)
        
        # download the .pdf file to the pdf_file_path folder
        # write content in pdf file
        pdf_path = os.path.join(pdf_folder, file_name)
        
        if response.status_code == 200:
            with open(pdf_path, 'wb') as pdf_object:
                pdf_object.write(response.content)
            # print(f'Successfully downloaded PDF:', ind)
            return True
        else:
            print(f'Failed downloading PDF:', ind, url)
            print(f'HTTP response status code: {response.status_code}')
            return False
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
# --------------------start of test code--------------------
# # pdf_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6577493/pdf/jneuro_14_5_2485.pdf"
# # pdf_url = "https://pharmrev.aspetjournals.org/content/pharmrev/24/1/31.full.pdf"
# pdf_url = "https://jnm.snmjournals.org/content/jnumed/39/2/281.full.pdf"
# ind = 11
# pdf_folder = fpath.pdf_folder
# download_by_request(pdf_url, ind, pdf_folder)
# ---------------------end of test code---------------------
# # pharmrev.aspetjournals.org
# # jpet.aspetjournals.org
# "https://pharmrev.aspetjournals.org/content/pharmrev/24/1/31.full.pdf"
# "https://jpet.aspetjournals.org/content/jpet/325/2/617.full.pdf"
# "https://jpet.aspetjournals.org/content/jpet/321/1/116.full.pdf"
# # citeseerx.ist.psu.edu
# "https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=086111ccf8db5585f16a54ba754ea75ebac97d6c"
# # www.nature.com
# "https://www.nature.com/articles/s41586-020-2914-4.pdf"
# # karger.com
# "https://karger.com/bbe/article-pdf/6/1-6/409/2259371/000315942.pdf"
# # ahuman.org
# "http://ahuman.org/svn/ahengine/research/articles/Biological/2002-Pathways-for-emotions-and-memory.PDF"
# # www.researchsquare.com
# "https://www.researchsquare.com/article/rs-2921649/v1.pdf?c=1687584387000"
# # link.springer.com
# "https://link.springer.com/content/pdf/10.1007/BF00236173.pdf?pdf=button"
# # www.ijpp.com
# "https://www.ijpp.com/IJPP%20archives/1981_25_3/201-208.pdf"
# # www.cell.com
# "https://www.cell.com/neuron/pdf/S0896-6273(11)00557-5.pdf"
# # www.bu.edu
# "https://www.bu.edu/neural/Final/Publications/2002/Thalamus%20%26%20Related%20Systems%2C%20Volume%202%2C%20Issue%201%2C%20December%202002%2C%20Pages%2021-32.pdf"
# # www.ncbi.nlm.nih.gov
# "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6577493/pdf/jneuro_14_5_2485.pdf"
# # www.thieme-connect.de
# "https://www.thieme-connect.de/products/ejournals/pdf/10.1055/s-2007-973495.pdf"
# # deepblue.lib.umich.edu
# "https://deepblue.lib.umich.edu/bitstream/handle/2027.42/74092/annals.1300.030.pdf?sequence=1"
# # bpb-us-e1.wpmucdn.com
# "https://bpb-us-e1.wpmucdn.com/sites.northwestern.edu/dist/7/2577/files/2018/08/23-Mesulam-2oebbn3.pdf"
# # www.researchgate.net
# "https://www.researchgate.net/profile/James-Augustine-2/publication/20294840_Augustine_JR_The_insular_lobe_in_primates_including_humans_Neurol_Res_7_2-10/links/60651633299bf1252e1cf66d/Augustine-JR-The-insular-lobe-in-primates-including-humans-Neurol-Res-7-2-10.pdf"
# # ieeexplore.ieee.org
# "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5333751"
# # zsp.com.pk
# "http://zsp.com.pk/pdf48/575-581%20(38)%20QPJZ-0063-2015%2017-12-15%20Longitudinal%20Metabolic%20Changes%20in%20the%20Thalamus%20o_.pdf"
# # journals.biologists.com
# "https://journals.biologists.com/dev/article-pdf/117/3/1031/3050703/develop_117_3_1031.pdf"
# # journals.aps.org
# "https://journals.aps.org/pre/pdf/10.1103/PhysRevE.106.054304"
# # academic.oup.com
# "https://academic.oup.com/cercor/article-pdf/10/3/220/9751036/100220.pdf"
# # www.biorxiv.org
# "https://www.biorxiv.org/content/10.1101/2022.02.03.479036v2.full.pdf"
# # enpubs.faculty.ucdavis.edu
# "https://enpubs.faculty.ucdavis.edu/wp-content/uploads/sites/209/2015/03/Disbrow-et-al_2002-Thalamocoretical-connections-of-the-parietal-ventral-area-and-the-second.pdf"
# # n.neurology.org
# "https://n.neurology.org/content/neurology/64/6/1014.full-text.pdf"
# # ruor.uottawa.ca
# "https://ruor.uottawa.ca/bitstream/10393/8164/1/NK25433.PDF"
# # www.jstage.jst.go.jp
# "https://www.jstage.jst.go.jp/article/pjab1945/43/8/43_8_822/_pdf/-char/en"
# # synapse.koreamed.org
# "https://synapse.koreamed.org/upload/synapsedata/pdfdata/0069ymj/ymj-55-709.pdf"
# # www.jneurosci.org
# "https://www.jneurosci.org/content/jneuro/11/8/2383.full.pdf"
# # pubs.asahq.org
# "https://pubs.asahq.org/anesthesiology/article-pdf/98/5/1101/407475/0000542-200305000-00012.pdf"
# # biomedcentral.com
# "https://biomedical-engineering-online.biomedcentral.com/counter/pdf/10.1186/1475-925X-3-13.pdf"
# # direct.mit.edu
# "https://direct.mit.edu/jocn/article-pdf/19/1/13/1936104/jocn.2007.19.1.13.pdf"
# # jnm.snmjournals.org
# "https://jnm.snmjournals.org/content/jnumed/39/2/281.full.pdf"


# linkinghub.elsevier.com
# "://linkinghub.elsevier.com/"
# "10.1016/j.neures.2006.02.006"
# "https://linkinghub.elsevier.com/retrieve/pii/S0168010206000423"
def download_from_linkinghub_elsevier_com(doi, ind, pdf_folder):
    try:
        file_name = str(ind) + ".pdf"
        pdf_path = os.path.join(pdf_folder, file_name)

        url = 'http://api.elsevier.com/content/article/doi:'+doi+'?view=FULL'
        headers = {
            'X-ELS-APIKEY': "63f58b8b10cbc1bc923011c01c6301bb",
            'Accept': 'application/pdf'
        }
        response = requests.get(url, stream=True, headers=headers)

        if response.status_code == 200:
            with open(pdf_path, 'wb') as pdf_object:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    pdf_object.write(chunk)
            pdf_object.close
            # print(f'Successfully downloaded PDF:', ind)
            return True
        else:
            print(f'Failed downloading PDF:', ind, doi)
            print(f'HTTP response status code: {response.status_code}')
            return False
    except:
        print(f'Failed downloading PDF:', ind, doi)
        return False
# --------------------start of test code--------------------
# # doi = "10.1016/0006-8993(95)01338-5"
# # doi = "10.1016/s0079-6123(08)60384-2" # no pdf available
# doi = "10.1016/0304-3940(82)90356-1"
# ind = 2
# pdf_folder = fpath.pdf_folder
# download_from_linkinghub_elsevier_com(doi, ind, pdf_folder)
# ---------------------end of test code---------------------


# 'journals.physiology.org'
def download_from_journals_physiology_org(url, ind, pdf_folder): 
    try:
        # set up the webdriver
        os.environ['WDM_LOG'] = '0'
        options = Options()
        options.add_argument('--headless')
        
        driver1 = webdriver.Firefox(options=options)
        driver1.get(url)
        time.sleep(10)
        url1 = driver1.find_element(By.XPATH, "//a[contains(@class,'navbar-download')]").get_attribute("href")
        driver1.quit()

        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", pdf_folder)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("pdfjs.disabled", True)

        driver2 = webdriver.Firefox(options=options)
        driver2.set_page_load_timeout(10)

        try:
            driver2.get(url1)
            rename_pdf(ind, pdf_folder, time_to_wait=60)
            return True
        except TimeoutException:
            # print("Page load timed out but that's okay!")
            rename_pdf(ind, pdf_folder, time_to_wait=60)
            return True
        except:
            print(f'Failed downloading PDF:', ind, url)
            return False
        finally:
            driver2.quit()
    except:
        print(f'Failed downloading PDF:', ind, url)
        print("Please manually download the pdf file")
        return False
        # # try:
        #     driver3 = webdriver.Firefox(options=options)
        #     driver3.get(url)
        #     time.sleep(10)
        #     button = driver3.find_element(By.XPATH, "//button[contains(@id,'download')]")
        #     button.click()
        #     # driver3.execute_script("arguments[0].click();", button)
        #     time.sleep(10)
        #     rename_pdf(ind, pdf_folder, time_to_wait=60)
        #     driver1.quit()
        #     file_name = str(ind) + ".pdf"
        #     time.sleep(2)
        #     response = requests.get(url, headers=plib.headers)
            
        #     # download the .pdf file to the pdf_file_path folder
        #     # write content in pdf file
        #     pdf_path = os.path.join(pdf_folder, file_name)
            
        #     if response.status_code == 200:
        #         with open(pdf_path, 'wb') as pdf_object:
        #             pdf_object.write(response.content)
        #         # print(f'Successfully downloaded PDF:', ind)
        #         # return True
        #     else:
        #         print(f'Failed downloading PDF:', ind, url)
        #         print(f'HTTP response status code: {response.status_code}')
        #         # return False
        # except:
        #     print(f'Failed downloading PDF:', ind, url)
        #     return False
        # except TimeoutException:
        #     # print("Page load timed out but that's okay!")
        #     rename_pdf(ind, pdf_folder, time_to_wait=60)
        #     # return True
        # except:
        #     print(f'Failed downloading PDF:', ind, url)
        # finally:
            # driver3.quit()
# --------------------start of test code--------------------
# # # journals.physiology.org
# # # pdf_url = "https://journals.physiology.org/doi/epdf/10.1152/jn.2001.85.1.219"
# pdf_url = "https://journals.physiology.org/doi/pdf/10.1152/jn.1977.40.6.1339"
# ind = 100
# pdf_folder = fpath.pdf_folder
# download_from_journals_physiology_org(pdf_url, ind, pdf_folder)
# ---------------------end of test code---------------------        


# # "//a[@class='navbar-download btn btn--cta_roundedColored']"
# ['wiley.com', 'www.science.org', 'tandfonline.com', 'sagepub.com', 'acs.org']
def download_pdf_by_a(url, ind, pdf_folder): 
    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    driver1 = webdriver.Firefox(options=options)
    driver1.get(url)
    time.sleep(10)
    url = driver1.find_element(By.XPATH, "//a[contains(@class,'navbar-download')]").get_attribute("href")
    driver1.quit()

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", pdf_folder)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)

    driver2 = webdriver.Firefox(options=options)
    driver2.set_page_load_timeout(5)

    try:
        driver2.get(url)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        # print("Page load timed out but that's okay!")
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver2.quit()
# --------------------start of test code--------------------
# # 'anatomypubs.onlinelibrary.wiley.com'
# # 'nyaspubs.onlinelibrary.wiley.com'
# # 'physoc.onlinelibrary.wiley.com'
# # 'onlinelibrary.wiley.com'
# # 'analyticalsciencejournals.onlinelibrary.wiley.com'
# # 'movementdisorders.onlinelibrary.wiley.com'
# # pdf_url = "https://physoc.onlinelibrary.wiley.com/doi/epdf/10.1113/JP280844"
# # pdf_url = "https://nyaspubs.onlinelibrary.wiley.com/doi/epdf/10.1196/annals.1284.033"
# # pdf_url = "https://anatomypubs.onlinelibrary.wiley.com/doi/epdf/10.1002/ar.22454"
# # pdf_url = "https://onlinelibrary.wiley.com/doi/epdf/10.1111/ejn.14426"
# # pdf_url = "https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/epdf/10.1002/jemt.10404"
# # pdf_url = "https://movementdisorders.onlinelibrary.wiley.com/doi/epdf/10.1002/mds.870060404"
# # # www.science.org
# # pdf_url = "https://www.science.org/doi/reader/10.1126/science.282.5391.1117"
# # # journals.physiology.org
# # pdf_url = "https://journals.physiology.org/doi/epdf/10.1152/jn.2001.85.1.219"
# # # www.tandfonline.com
# # pdf_url = "https://www.tandfonline.com/doi/epdf/10.3109/08990229109144753?needAccess=true&role=button"
# # # journals.sagepub.com
# # pdf_url = "https://journals.sagepub.com/doi/reader/10.1177/107385840100700408"
# # # pubs.acs.org
# pdf_url = "https://pubs.acs.org/doi/epdf/10.1021/jm030384e"
# ind = 4
# pdf_folder = fpath.pdf_folder
# if download_pdf_by_a(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# www.microbiologyresearch.org
def download_from_www_microbiologyresearch_org(url, ind, pdf_folder):
    os.environ['WDM_LOG'] = '0'
    options1 = Options()
    options1.add_argument('--headless')
    driver1 = webdriver.Firefox(options=options1)
    # driver1.set_page_load_timeout(10)

    driver1.get(url)
    url = driver1.find_element(By.XPATH, "//div[contains(@class,'ft-download-content--pdf')]/form").get_attribute("action")
    # print(url)
    driver1.quit()

    options2 = Options()
    options2.add_argument('--headless')
    options2.set_preference("browser.download.folderList", 2)
    options2.set_preference("browser.download.manager.showWhenStarting", False)
    options2.set_preference("browser.download.dir", pdf_folder)
    options2.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options2.set_preference("pdfjs.disabled", True)
    driver2 = webdriver.Firefox(options=options2)
    driver2.set_page_load_timeout(10)

    try:
        driver2.get(url)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver2.quit()
# --------------------start of test code--------------------
# # "://www.microbiologyresearch.org/"
# pdf_url = "https://www.microbiologyresearch.org/content/journal/jgv/10.1099/vir.0.79883-0"
# ind = 32
# pdf_folder = fpath.pdf_folder
# if download_from_www_microbiologyresearch_org(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# europepmc.org
def download_from_europepmc_org(url, ind, pdf_folder):
    os.environ['WDM_LOG'] = '0'
    options1 = Options()
    options1.add_argument('--headless')
    driver1 = webdriver.Firefox(options=options1)
    driver1.set_page_load_timeout(10)
    try:
        driver1.get(url)
        button = driver1.find_element(By.XPATH, "//span[contains(@id,'open_pdf')]")
        driver1.execute_script("arguments[0].click();", button)
        time.sleep(10)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver1.quit()
# --------------------start of test code--------------------
# # "://europepmc.org/"
# # pdf_url = "https://europepmc.org/article/med/8784824"
# pdf_url = "https://europepmc.org/article/MED/37298594"
# # pdf_url = "https://europepmc.org/article/med/8784824"
# # pdf_url = "https://europepmc.org/article/med/823649"
# # pdf_url = "https://europepmc.org/article/med/4220147"
# ind = 3
# pdf_folder = "/Users/didihou/Downloads"
# if download_from_europepmc_org(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# papers.ssrn.com
def download_from_papers_ssrn_com(url, ind, pdf_folder):
    os.environ['WDM_LOG'] = '0'
    options1 = Options()
    options1.add_argument('--headless')
    driver1 = webdriver.Firefox(options=options1)
    driver1.set_page_load_timeout(10)
    try:
        driver1.get(url)
        button = driver1.find_element(By.XPATH, "//a[contains(@class,'button-link primary')]")
        driver1.execute_script("arguments[0].click();", button)
        time.sleep(10)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver1.quit()
# --------------------start of test code--------------------
# # "://papers.ssrn.com/"
# pdf_url = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3689615"
# ind = 5
# pdf_folder = '/Users/didihou/Downloads'
# if download_from_papers_ssrn_com(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# www.ingentaconnect.com
def download_from_www_ingentaconnect_com(url, ind, pdf_folder):
    file_name = str(ind) + ".pdf"
    pdf_path = os.path.join(pdf_folder, file_name)

    os.environ['WDM_LOG'] = '0'
    options1 = Options()
    options1.add_argument('--headless')
    driver1 = webdriver.Firefox(options=options1)
    # driver1.set_page_load_timeout(10)
    try:
        driver1.get(url)
        url = driver1.find_element(By.XPATH, "//a[contains(@class,'fulltext pdf btn')]").get_attribute("data-popup")
        url = url.split("&host=")[1] + url.split("&host")[0]
        # print(url)

        response = requests.get(url, stream=True, headers=plib.headers)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as pdf_object:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    pdf_object.write(chunk)
            pdf_object.close
            # print(f'Successfully downloaded PDF:', ind, url)
            return True
        else:
            print(f'Failed downloading PDF:', ind, url)
            print(f'HTTP response status code: {response.status_code}')
            return False
    except:
        # print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver1.quit()
# --------------------start of test code--------------------
# # "://www.ingentaconnect.com/"
# pdf_url = "https://www.ingentaconnect.com/content/aalas/cm/2000/00000050/00000002/art00006"
# ind = 6
# pdf_folder = fpath.pdf_folder
# if download_from_www_ingentaconnect_com(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# journals.lww.com
def download_from_journals_lww_com(url, ind, pdf_folder):
    os.environ['WDM_LOG'] = '0'
    options1 = Options()
    options1.add_argument('--headless')
    driver1 = webdriver.Firefox(options=options1)
    driver1.set_page_load_timeout(10)
    try:
        driver1.get(url)
        button = driver1.find_element(By.XPATH, "//button[contains(@class,'ejp-article-tools__dropdown-list-button')]")
        # button.click()
        driver1.execute_script("arguments[0].click();", button)
        time.sleep(10)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver1.quit()
# --------------------start of test code--------------------
# # "://journals.lww.com/"
# pdf_url = "https://journals.lww.com/neuroreport/abstract/1994/10000/further_evidence_for_two_types_of_corticopulvinar.6.aspx"
# ind = 7
# pdf_folder = fpath.pdf_folder
# if download_from_journals_lww_com(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# # "//button[@class='dropdown-trigger btn btn--light btn--cta_roundedColored']"
# ['www.ahajournals.org', 'psychiatryonline.org']
# download pdf to specified folder given pdf_url and ind
def download_pdf_by_button(url, ind, pdf_folder):  
    os.environ['WDM_LOG'] = '0'
    options1 = Options()
    options1.add_argument('--headless')
    driver1 = webdriver.Firefox(options=options1)

    driver1.get(url)
    time.sleep(10)
    button = driver1.find_element(By.CSS_SELECTOR, ".dropdown-trigger.btn.btn--light")
    driver1.execute_script("arguments[0].click();", button)
    time.sleep(10)
    url = driver1.find_element(By.XPATH, "//ul[contains(@class,'base-download-options')]/li[1]/a").get_attribute("href")
    driver1.quit()

    options2 = Options()
    options2.add_argument('--headless')
    options2.set_preference("browser.download.folderList", 2)
    options2.set_preference("browser.download.manager.showWhenStarting", False)
    options2.set_preference("browser.download.dir", pdf_folder)
    options2.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options2.set_preference("pdfjs.disabled", True)
    driver2 = webdriver.Firefox(options=options2)
    driver2.set_page_load_timeout(10)

    try:
        driver2.get(url)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver2.quit()
# --------------------start of test code--------------------
# # 'www.ahajournals.org'
# # pdf_url = "https://www.ahajournals.org/doi/reader/10.1161/01.STR.0000087786.38997.9E"
# # 'neuro.psychiatryonline.org'
# # 'ajp.psychiatryonline.org'
# pdf_url = "https://neuro.psychiatryonline.org/doi/reader/10.1176/jnp.16.2.127"
# # pdf_url = "https://ajp.psychiatryonline.org/doi/reader/10.1176/appi.ajp.158.9.1411"
# ind = 10
# pdf_folder = fpath.pdf_folder
# if pdf_url.split("://")[1].split("/")[0] == 'www.ahajournals.org':
#     url = "https://www.ahajournals.org/doi/epdf/" + pdf_url.split("reader/")[1]
# elif "psychiatryonline.org" in pdf_url.split("://")[1].split("/")[0]:
#     url = pdf_url
# else:
#     raise Exception("pdf_url is not from a supported website: ", pdf_url)

# if download_pdf_by_button(url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------


# driver.get(url)
# ['iovs.arvojournals.org', 'www.imrpress.com', 'www.hifo.uzh.ch', 'ujms.net', 'www.annualreviews.org', 'thejns.org']
def download_pdf_by_driver(url, ind, pdf_folder): 
    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", pdf_folder)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(10)

    try:
        driver.get(url)
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except TimeoutException:
        rename_pdf(ind, pdf_folder, time_to_wait=60)
        return True
    except:
        print(f'Failed downloading PDF:', ind, url)
        return False
    finally:
        driver.quit()
# --------------------start of test code--------------------
# # # iovs.arvojournals.org
# # pdf_url = "https://iovs.arvojournals.org//arvo/content_public/journal/iovs/934840/i1552-5783-57-1-1.pdf"
# # # www.imrpress.com
# # pdf_url = "https://www.imrpress.com/journal/JIN/20/1/10.31083/j.jin.2021.01.334/pdf"
# # # www.hifo.uzh.ch
# # pdf_url = "https://www.hifo.uzh.ch/dam/jcr:00000000-2999-c151-ffff-ffffd9509b89/paper_CorticalArea8.pdf"
# # # ujms.net
# # pdf_url = "https://ujms.net/index.php/ujms/article/download/6812/12603"
# # # www.annualreviews.org
# # pdf_url = "https://www.annualreviews.org/doi/pdf/10.1146/annurev.ne.11.030188.001345"
# # # thejns.org
# pdf_url = "https://thejns.org/downloadpdf/journals/j-neurosurg/86/1/article-p77.xml"
# ind = 10
# pdf_folder = fpath.pdf_folder
# if download_pdf_by_driver(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind, url)
# else:
#     print(f'Failed downloading PDF:', ind, url)
# ---------------------end of test code---------------------

# download_not_possible = ['royalsocietypublishing.org', 'jamanetwork.com']
def download_not_possible(url, ind, pdf_folder):
    # os.environ['WDM_LOG'] = '0'
    # options1 = Options()
    # options1.add_argument('--headless')
    # driver1 = webdriver.Firefox(options=options1)
    # # driver1.set_page_load_timeout(10)

    # driver1.get(url)
    # url = driver1.find_element(By.XPATH, "//i[contains(@class,'icon-pdf')]/..").get_attribute("href")
    # driver1.quit()
    

    # driver1.get(url)
    # url = driver1.find_element(By.XPATH, "//a[contains(@class,'navbar-download')]").get_attribute("href")
    # driver1.quit()
    
    # options2 = Options()
    # options2.add_argument('--headless')
    # options2.set_preference("browser.download.folderList", 2)
    # options2.set_preference("browser.download.manager.showWhenStarting", False)
    # options2.set_preference("browser.download.dir", pdf_folder)
    # options2.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    # options2.set_preference("pdfjs.disabled", True)
    # driver2 = webdriver.Firefox(options=options2)
    # driver2.set_page_load_timeout(10)

    # try:
    #     driver2.get(url)
    #     rename_pdf(ind, pdf_folder, time_to_wait=60)
    #     return True
    # except TimeoutException:
    #     rename_pdf(ind, pdf_folder, time_to_wait=60)
    #     return True
    # except:
    #     return False
    # finally:
    #     driver2.quit()
    print("Download from", url, "is not possible, please download manually! ind is ", ind)
    return False
# --------------------start of test code--------------------
# # "://royalsocietypublishing.org/"
# pdf_url = "https://royalsocietypublishing.org/doi/10.1098/rspb.1953.0054"
# # jamanetwork.com
# "://jamanetwork.com/"
# "https://jamanetwork.com/journals/jamaneurology/article-abstract/565945"
# ind = 3
# pdf_folder = fpath.pdf_folder
# download_not_possible(pdf_url, ind, pdf_folder)
# ---------------------end of test code---------------------


# # test code for download_and_process_pdf.py
# doi = ''
# # pdf_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6577493/pdf/jneuro_14_5_2485.pdf"
# # "https://pharmrev.aspetjournals.org/content/pharmrev/24/1/31.full.pdf"
# # "https://direct.mit.edu/jocn/article-pdf/19/1/13/1936104/jocn.2007.19.1.13.pdf"

# # pdf_url = "https://jnm.snmjournals.org/content/jnumed/39/2/281.full.pdf"
# # pdf_url = "://linkinghub.elsevier.com/"
# # doi = "10.1016/0006-8993(95)01338-5"
# # pdf_url = "https://physoc.onlinelibrary.wiley.com/doi/epdf/10.1113/JP280844"
# # pdf_url = "https://www.microbiologyresearch.org/content/journal/jgv/10.1099/vir.0.79883-0"
# # pdf_url = "https://europepmc.org/article/med/8784824"
# # pdf_url = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3689615"
# # pdf_url = "https://www.ingentaconnect.com/content/aalas/cm/2000/00000050/00000002/art00006"
# # pdf_url = "https://journals.lww.com/neuroreport/abstract/1994/10000/further_evidence_for_two_types_of_corticopulvinar.6.aspx"
# # pdf_url = "https://www.ahajournals.org/doi/reader/10.1161/01.STR.0000087786.38997.9E"
# # pdf_url = "https://iovs.arvojournals.org//arvo/content_public/journal/iovs/934840/i1552-5783-57-1-1.pdf"
# # pdf_url = "https://royalsocietypublishing.org/doi/10.1098/rspb.1953.0054"
# pdf_url = "https://jamanetwork.com/journals/jamaneurology/article-abstract/565945"
# ind = 5
# pdf_folder = fpath.pdf_folder
# dpp.download_and_rename_pdf(pdf_url, doi, ind, pdf_folder)