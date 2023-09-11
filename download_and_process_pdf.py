# import internal modules
import file_path_management as fpath
import public_library as plib
import extract_info
import parameters as params

# import external modules
import requests
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
    filename = max([f for f in os.listdir(pdf_folder)], key=lambda xa :   os.path.getctime(os.path.join(pdf_folder,xa)))
    while '.part' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Waited too long for file to download')
    filename = max([f for f in os.listdir(pdf_folder)], key=lambda xa :   os.path.getctime(os.path.join(pdf_folder,xa)))
    os.rename(os.path.join(pdf_folder, filename), os.path.join(pdf_folder, newname))

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
        response = requests.get(url, headers=plib.headers)
        
        # download the .pdf file to the pdf_file_path folder
        # write content in pdf file
        pdf_path = os.path.join(pdf_folder, file_name)
        
        if response.status_code == 200:
            with open(pdf_path, 'wb') as pdf_object:
                pdf_object.write(response.content)
            print(f'Successfully downloaded PDF:', ind)
            return True
        else:
            print(f'Failed downloading PDF:' + 'pdf_url')
            print(f'HTTP response status code: {response.status_code}')
            return False
    except:
        print(f'Failed downloading PDF:' + 'pdf_url')
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
def download_from_ELSEVIER(doi, ind, pdf_folder):
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
            print(f'Successfully downloaded PDF:', ind)
        else:
            print(f'Failed downloading PDF:' + 'doi')
            print(f'HTTP response status code: {response.status_code}')
        return True
    except:
        print(f'Failed downloading PDF:' + 'doi')
        return False
# --------------------start of test code--------------------
# # doi = "10.1016/0006-8993(95)01338-5"
# # doi = "10.1016/s0079-6123(08)60384-2" # no pdf available
# doi = "10.1016/0304-3940(82)90356-1"
# ind = 2
# pdf_folder = fpath.pdf_folder
# download_from_ELSEVIER(doi, ind, pdf_folder)
# ---------------------end of test code---------------------


# # "//a[@class='navbar-download btn btn--cta_roundedColored']"
# ['wiley.com', 'www.science.org', 'physiology.org', 'tandfonline.com', 'sagepub.com', 'acs.org']
def download_pdf_by_a(url, ind, pdf_folder): 
    # set up the webdriver
    os.environ['WDM_LOG'] = '0'
    options = Options()
    options.add_argument('--headless')
    
    driver1 = webdriver.Firefox(options=options)
    driver1.get(url)
    time.sleep(10)
    url = driver1.find_element(By.XPATH, "//a[contains(@class,'navbar-download')]").get_attribute("href")

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
#     print(f'Successfully downloaded PDF:', ind)
# else:
#     print(f'Failed downloading PDF:', ind)
# ---------------------end of test code---------------------


# www.microbiologyresearch.org
def downalod_from_www_microbiologyresearch_org(url, ind, pdf_folder):
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
        return False
    finally:
        driver2.quit()
# --------------------start of test code--------------------
# # "://www.microbiologyresearch.org/"
# pdf_url = "https://www.microbiologyresearch.org/content/journal/jgv/10.1099/vir.0.79883-0"
# ind = 32
# pdf_folder = fpath.pdf_folder
# if downalod_from_www_microbiologyresearch_org(pdf_url, ind, pdf_folder):
#     print(f'Successfully downloaded PDF:', ind)
# else:
#     print(f'Failed downloading PDF:', ind)
# ---------------------end of test code---------------------