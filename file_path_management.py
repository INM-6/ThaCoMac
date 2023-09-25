from pathlib import Path
import os

# file folder storing the pdfs of the potential relevant literature
# it's stored in a external SSD of 500GB
pdf_folder = "/media/hou/DIDIHOU/pdfs"
# pdf_folder = "/Users/didihou/Downloads/"
# it's stored in a external SSD of 500GB
# file folder storing the extracted texts of the potential relevant literature
text_folder = "/media/hou/DIDIHOU/texts"
relevant_pdf_folder = "/media/hou/DIDIHOU/relevant_pdfs"
not_relevant_pdf_folder = "/media/hou/DIDIHOU/not_relevant_pdfs"


# project folder and the root folder of the repository
project_folder = Path.cwd()
# path to the datasets
datasets_folder = os.path.join(project_folder, "datasets")


seed_paper_list = os.path.join(datasets_folder, "seed_literature_list.txt")
cocomac_paper_list = os.path.join(datasets_folder, "cocomac_literature_list.txt")


# search results from the academic databases and the processed results
poten_litera_gs = os.path.join(datasets_folder, "potential_literature_google_scholar.csv")
poten_litera_gs_test = os.path.join(datasets_folder, "potential_literature_google_scholar_test.csv")
poten_litera_gs_processed_step1 = os.path.join(datasets_folder, "potential_literature_google_scholar_processed_step1.csv")
poten_litera_gs_processed_step2 = os.path.join(datasets_folder, "potential_literature_google_scholar_processed_step2.csv")
poten_litera_wos_1 = os.path.join(datasets_folder, "potential_literature_webofscience_1.csv")
poten_litera_wos_2 = os.path.join(datasets_folder, "potential_literature_webofscience_2.csv")
poten_litera_wos = os.path.join(datasets_folder, "potential_literature_webofscience.csv")
poten_litera_wos_processed = os.path.join(datasets_folder, "potential_literature_webofscience_processed.csv")
poten_litera_pubmed = os.path.join(datasets_folder, "potential_literature_pubmed.csv")
poten_litera_pubmed_processed = os.path.join(datasets_folder, "potential_literature_pubmed_processed.csv")
poten_litera_eupmc = os.path.join(datasets_folder, "potential_literature_europepmc.csv")
poten_litera_eupmc_processed = os.path.join(datasets_folder, "potential_literature_europepmc_processed.csv")


poten_litera_combined = os.path.join(datasets_folder, "potential_related_literature_combined.csv")
poten_litera_filled = os.path.join(datasets_folder, "potential_related_literature_filled.csv")
poten_litera_ids_filled = os.path.join(datasets_folder, "potential_related_literature_ids_filled.csv")
poten_litra_filtered = os.path.join(datasets_folder, "potential_related_literature_filtered.csv")
poten_litera_ids_ftl_filled = os.path.join(datasets_folder, "potential_related_literature_ids_ftl_filled.csv")
poten_litera_ids_ftl_filled_filtered = os.path.join(datasets_folder, "potential_related_literature_ids_ftl_filled_filtered.csv")
poten_litera_testing_set_300 = os.path.join(datasets_folder, "potential_related_literature_testing_set_300.csv")
poten_litera_testing_set_300_read = os.path.join(datasets_folder, "potential_related_literature_testing_set_300_read.csv")
poten_litera_testing_set_300_read_index_corrected = os.path.join(datasets_folder, "potential_related_literature_testing_set_300_read_index_corrected.csv")
poten_litera_db = os.path.join(datasets_folder, "potential_related_literature_databse.csv")
poten_litera_db_ranked = os.path.join(datasets_folder, "potential_related_literature_database_ranked.csv")

poten_litera_pdf_not_available = os.path.join(datasets_folder, "potential_related_literature_pdf_not_available.csv")

related_litera = os.path.join(datasets_folder, "related_literature.csv")


summary_table = os.path.join(datasets_folder, "summary_table_of_related_studies.csv")



