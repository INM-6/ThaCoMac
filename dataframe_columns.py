import parameters as params

keys_list = list(params.ranking_kw_groups.keys())


index = ["INDEX"]
identifier = ["DOI", "PMID", "PMCID"]
url = ["FULL_TEXT_URL", "PDF_URL"]
source = ["FULL_TEXT_SOURCE", "PDF_SOURCE"]
url_and_source = ["FULL_TEXT_URL", "FULL_TEXT_SOURCE", "PDF_URL", "PDF_SOURCE"]
title = ["TITLE"]
tak = ["TITLE", "ABSTRACT", "KEYWORDS"]

relevance_index = ["RELEVANCE_INDEX"]

relevance = ["RELEVANCE"]


# columns storing the sentences containing keywords in full text
text_columns_to_add = []
for key in keys_list:
    text_columns_to_add.append(key + "_TEXT")


# columns storing the counts of keywords for different texts
count_columns_to_add = []
for key in keys_list:
    count_columns_to_add.append(key + "_COUNT_IN_TAK")
    
for key in keys_list:
    count_columns_to_add.append(key + "_COUNT_IN_500")

for key in keys_list:
    count_columns_to_add.append(key + "_COUNT_IN_FULL_TEXT")


# columns storing the transformed counts of keywords for different texts
# trans_count_columns_to_add = []
# for key in keys:
#     trans_count_columns_to_add.append(key + "_TRANS_COUNT_IN_TAK")
    
# for key in keys:
#     trans_count_columns_to_add.append(key + "_TRANS_COUNT_IN_500")

# for key in keys:
#     trans_count_columns_to_add.append(key + "_TRANS_COUNT_IN_FULL_TEXT")

columns_to_fill_0 = ['TT?(Y/N/MB/NA)', 'MACAQUE?(Y/N/MB/NA)', 'TC_OR_CT?(Y/N/MB/NA)', 'RELEVANT?(Y/N/MB/NA)', 'READ_BY(A/D/R)', 'COMMENT']

columns_to_fill = ['TT?(Y/N/MB/NA)', 'MACAQUE?(Y/N/MB/NA)', 'TC_OR_CT?(Y/N/MB/NA)', 'RELEVANT?(Y/N/MB/NA)', 'REVIEW(Y/N)', 'READ_BY(A/D/R)', 'COMMENT']
# ==========================================================================================================
db_columns = index + identifier + url_and_source + tak

train_test_1000_path_columns = index + identifier + url_and_source + tak

db_count_columns = index + count_columns_to_add

# db_count_trans_columns = db_count_columns + trans_count_columns_to_add

db_ranked_columns = db_count_columns + relevance_index

final_manually_read_df_columns = index + columns_to_fill + identifier  + url + tak + text_columns_to_add