from pathlib import Path
import os
from typing import final

from scipy import datasets

# device = "/Volumes/DIDIHOU/"
device = "/media/hou/DIDIHOU/"

pdf_folder = device + "pdfs"
text_folder = device + "texts"
processed_texts_of_length_500_folder = device + "processed_texts_of_length_500"
TT_text_folder = device + "TT_text"
# relevant_text_folder = device + "relevant_texts"
# not_recog_articles_folder = device + "not_recognizable_articles"
# relevant_pdf_folder = device + "relevant_pdfs"
# not_relevant_pdf_folder = device + "not_relevant_pdfs"



# project folder and the root folder of the repository
project_folder = Path.cwd()
# path to the datasets
datasets_folder = os.path.join(project_folder, "datasets")
literature_search_results_folder = os.path.join(project_folder, "datasets", "01_literature_search_results")
data_processing_folder = os.path.join(project_folder, "datasets", "02_data_processing")
potential_literature_database_folder = os.path.join(project_folder, "datasets", "03_potential_literature_database")
embedding_and_pca_folder = os.path.join(project_folder, "datasets", "04_embedding_and_pca")
manually_read_and_confirm_folder = os.path.join(project_folder, "datasets", "05_manually_read_and_confirm")



# literature_search_results_folder
cocomac_literature_list = os.path.join(literature_search_results_folder, "cocomac_literature_list.csv")
poten_litera_gs = os.path.join(literature_search_results_folder, "potential_literature_google_scholar.csv")
poten_litera_wos_1 = os.path.join(literature_search_results_folder, "potential_literature_webofscience_1.csv")
poten_litera_wos_2 = os.path.join(literature_search_results_folder, "potential_literature_webofscience_2.csv")
poten_litera_wos = os.path.join(literature_search_results_folder, "potential_literature_webofscience.csv")
poten_litera_pubmed = os.path.join(literature_search_results_folder, "potential_literature_pubmed.csv")
poten_litera_eupmc = os.path.join(literature_search_results_folder, "potential_literature_europepmc.csv")



# data_processing_folder
poten_litera_gs_processed_step1 = os.path.join(data_processing_folder, "potential_literature_google_scholar_processed_step1.csv")
poten_litera_gs_processed_step2 = os.path.join(data_processing_folder, "potential_literature_google_scholar_processed_step2.csv")
poten_litera_wos_processed = os.path.join(data_processing_folder, "potential_literature_webofscience_processed.csv")
poten_litera_pubmed_processed = os.path.join(data_processing_folder, "potential_literature_pubmed_processed.csv")
poten_litera_eupmc_processed = os.path.join(data_processing_folder, "potential_literature_europepmc_processed.csv")
poten_litera_combined = os.path.join(data_processing_folder, "potential_related_literature_combined.csv")
poten_litera_filled = os.path.join(data_processing_folder, "potential_related_literature_filled.csv")
poten_litera_ids_filled = os.path.join(data_processing_folder, "potential_related_literature_ids_filled.csv")
poten_litra_filtered = os.path.join(data_processing_folder, "potential_related_literature_filtered.csv")
poten_litera_ids_ftl_filled = os.path.join(data_processing_folder, "potential_related_literature_ids_ftl_filled.csv")
poten_litera_ids_ftl_filled_filtered = os.path.join(data_processing_folder, "potential_related_literature_ids_ftl_filled_filtered.csv")



# potential_literature_database_folder
poten_litera_db = os.path.join(potential_literature_database_folder, "potential_related_literature_databse.csv")
# poten_litera_db_text_extract = os.path.join(literature_datasets_folder, "potential_related_literature_database_final.csv")

poten_litera_pdf_not_available = os.path.join(potential_literature_database_folder, "potential_related_literature_pdf_not_available.csv")
poten_litera_ta_not_available = os.path.join(potential_literature_database_folder, "poten_litera_ta_not_available.csv")

poten_litera_testing_set_300 = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_300.csv")
poten_litera_testing_set_300_read = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_300_read.csv")
poten_litera_testing_set_300_read_index_corrected = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_300_read_index_corrected.csv")
poten_litera_testing_set_708 = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_708.csv")
poten_litera_testing_set_708_read = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_708_read.csv")
poten_litera_testing_set_1000 = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_1000.csv")

poten_litera_testing_set_1000_text_extract = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_1000_text_extract.csv")
poten_litera_testing_set_1000_text_extract_and_count = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_1000_text_extract_and_count.csv")
poten_litera_testing_set_1000_labeled = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_1000_labeled.csv")
poten_litera_testing_set_1000_labeled_complete = os.path.join(potential_literature_database_folder, "potential_related_literature_testing_set_1000_labeled_complete.csv")

poten_litera_db_kw_count = os.path.join(potential_literature_database_folder, "potential_related_literature_database_kw_count.csv")
poten_litera_db_kw_count_with_2_new_columns = os.path.join(potential_literature_database_folder, "potential_related_literature_database_kw_count_with_2_new_columns.csv")
poten_litera_db_relevance_index = os.path.join(potential_literature_database_folder, "potential_related_literature_database_relevance_index.csv")
poten_litera_db_ranked_by_ta = os.path.join(potential_literature_database_folder, "potential_related_literature_database_ranked_by_ta.csv")
poten_litera_db_ranked_by_500 = os.path.join(potential_literature_database_folder, "potential_related_literature_database_ranked_by_500.csv")
poten_litera_db_ranked_by_full_text = os.path.join(potential_literature_database_folder, "potential_related_literature_database_ranked_by_full_text.csv")



# manually_read_and_confirm_folder
article_list_to_manually_read = os.path.join(manually_read_and_confirm_folder, "article_list_to_manually_read.txt")
relevant_article_and_is_review = os.path.join(manually_read_and_confirm_folder, "relevant_article_and_is_review.txt")

final_manually_read_csv = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv.csv")
final_manually_read_csv_1 = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_1.csv")
final_manually_read_csv_2 = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_2.csv")
final_manually_read_csv_3 = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_3.csv")
final_manually_read_csv_4 = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_4.csv")
# final_manually_read_csv_abstract_full_text_not_available = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_abstract_full_text_not_available.csv")

final_manually_read_csv_1_labeled = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_1_labeled.csv")
final_manually_read_csv_2_labeled = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_2_labeled.csv")
final_manually_read_csv_3_labeled = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_3_labeled.csv")
final_manually_read_csv_4_labeled = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_4_labeled.csv")
# final_manually_read_csv_abstract_full_text_not_available_labeled = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_abstract_full_text_not_available_labeled.csv")

final_manually_read_csv_1_aitor = os.path.join(manually_read_and_confirm_folder, "final_manually_read_csv_1_aitor.csv")



# final_confirm_article_list
final_confirm_article_list = os.path.join(manually_read_and_confirm_folder, "final_confirm_article_list.csv")
relevant_reviews_and_ta_not_avaialble = os.path.join(manually_read_and_confirm_folder, "relevant_reviews_and_ta_not_avaialble.csv")
final_confirm_article_list_labeled = os.path.join(manually_read_and_confirm_folder, "final_confirm_article_list_labeled.csv")
relevant_article_and_is_review_labeled = os.path.join(manually_read_and_confirm_folder, "relevant_reviews_and_ta_not_avaialble_labeled.csv")

# relevant_articles_YESES = os.path.join(manually_read_and_confirm_folder, "relevant_articles_YESES.csv")
relevant_articles_YESES = os.path.join(datasets_folder, "relevant_articles_YESES.csv")
relevant_articles_YESES_corrected = os.path.join(datasets_folder, "relevant_articles_YESES_corrected.csv")

