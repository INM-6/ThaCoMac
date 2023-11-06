import parameters as params

identifier = ["INDEX", "DOI", "PMID", "PMCID"]
url = ["FULL_TEXT_URL", "PDF_URL"]
source = ["FULL_TEXT_SOURCE", "PDF_SOURCE"]
url_and_source = ["FULL_TEXT_URL", "FULL_TEXT_SOURCE", "PDF_URL", "PDF_SOURCE"]
title = ["TITLE"]
tak = ["TITLE", "ABSTRACT", "KEYWORDS"]

relevance_index = ["RELEVANCE_INDEX"]

relevance = ["RELEVANCE"]

keys = list(params.ranking_kw_groups.keys())

text_columns_to_add = []
for key in keys:
    text_columns_to_add.append(key + "_TEXT")

count_columns_to_add = []
for key in keys:
    count_columns_to_add.append(key + "_COUNT_IN_500")

for key in keys:
    count_columns_to_add.append(key + "_COUNT_IN_FULL_TEXT")
# ==========================================================================================================
db_columns = identifier + url_and_source + tak

train_test_1000_path_columns = identifier + url_and_source + tak + relevance

db_ranked_columns = ["INDEX"] +  count_columns_to_add