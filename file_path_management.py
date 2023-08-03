from pathlib import Path
import os


# annoucing all file paths
project_folder = Path.cwd()
litera_pdf_folder = os.path.join(project_folder, "litera_pdfs")
datasets_folder = os.path.join(project_folder, "datasets")


proxy_list = os.path.join(project_folder, "list_proxyseller.txt")


seed_paper_list = os.path.join(datasets_folder, "seed_literature_list.txt")
cocomac_paper_list = os.path.join(datasets_folder, "cocomac_literature_list.txt")


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


poten_litera = os.path.join(datasets_folder, "potential_related_literature.csv")
filtered_poten_litra = os.path.join(datasets_folder, "potential_related_literature_filtered.csv")
ranked_poten_litera = os.path.join(datasets_folder, "potential_related_literature_ranked.csv")


related_litera = os.path.join(datasets_folder, "related_literature.csv")


summary_table = os.path.join(datasets_folder, "summary_table_of_related_studies.csv")



