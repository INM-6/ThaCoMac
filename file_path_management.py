from pathlib import Path
import os

pdf_folder = "/media/hou/DIDIHOU/pdfs"
text_folder = "/media/hou/DIDIHOU/texts"
processed_texts_of_length_500_folder = "/media/hou/DIDIHOU/processed_texts_of_length_500"
TT_text_folder = "/media/hou/DIDIHOU/TT_text"
relevant_text_folder = "/media/hou/DIDIHOU/relevant_texts"
not_recog_articles_folder = "/media/hou/DIDIHOU/not_recognizable_articles"
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
poten_litera_testing_set_708 = os.path.join(datasets_folder, "potential_related_literature_testing_set_708.csv")
poten_litera_testing_set_708_read = os.path.join(datasets_folder, "potential_related_literature_testing_set_708_read.csv")
poten_litera_testing_set_1000 = os.path.join(datasets_folder, "potential_related_literature_testing_set_1000.csv")

poten_litera_testing_set_1000_text_extract = os.path.join(datasets_folder, "potential_related_literature_testing_set_1000_text_extract.csv")
poten_litera_testing_set_1000_text_extract_and_count = os.path.join(datasets_folder, "potential_related_literature_testing_set_1000_text_extract_and_count.csv")
poten_litera_testing_set_1000_labeled = os.path.join(datasets_folder, "potential_related_literature_testing_set_1000_labeled.csv")

poten_litera_db = os.path.join(datasets_folder, "potential_related_literature_databse.csv")
poten_litera_db_text_extract = os.path.join(datasets_folder, "potential_related_literature_database_final.csv")
poten_litera_db_kw_count = os.path.join(datasets_folder, "potential_related_literature_database_kw_count.csv")
poten_litera_db_ranked = os.path.join(datasets_folder, "potential_related_literature_database_ranked.csv")

poten_litera_pdf_not_available = os.path.join(datasets_folder, "potential_related_literature_pdf_not_available.csv")
poten_litera_text_not_available = os.path.join(datasets_folder, "potential_related_literature_text_not_available.csv")

related_litera = os.path.join(datasets_folder, "related_literature.csv")


summary_table = os.path.join(datasets_folder, "summary_table_of_related_studies.csv")



