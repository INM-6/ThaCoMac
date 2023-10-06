import parameters as params

identifier = ["INDEX", "DOI", "PMID", "PMCID"]
url = ["FULL_TEXT_URL", "PDF_URL"]
source = ["FULL_TEXT_SOURCE", "PDF_SOURCE"]
url_and_source = ["FULL_TEXT_URL", "FULL_TEXT_SOURCE", "PDF_URL", "PDF_SOURCE"]
title = ["TITLE"]
tak = ["TITLE", "ABSTRACT", "KEYWORDS"]

relevance_index = ["RELEVANCE_INDEX"]

text_column_to_add = ["MACAQUE", "OTHER_SPIECIES", "TC_CT", "THALAM", "INJECT", "METHOD"]

count_columns_to_add = [key+"_COUNT" for key in params.ranking_kw_groups.keys()]
# ==========================================================================================================
db_columns = identifier + url_and_source + tak

train_test_1000_path_columns = identifier + url_and_source + tak + relevance_index

db_ranked_columns = identifier + title +  count_columns_to_add + relevance_index