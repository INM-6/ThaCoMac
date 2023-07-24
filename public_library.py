# self-written public library
import csv
import pandas as pd

# setting headers and proxies
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
http_proxy  = "http://103.148.39.50:83"
https_proxy = "https://47.254.158.115:20201"
proxy = {
    "http": http_proxy, 
    "https": https_proxy
}
# end of setting header and proxies

def clear_file(file_path):
    with open(file_path, 'w') as f:
        f.truncate()
        f.close()

'''
# test code: clear_file(file_path)
file_path = ''
clear_file(file_path)
'''

def ask_ChatGPT(context, queries):
    answers =  []
    # code
    return answers
            

# # test code: ask_ChatGPT(context, queries)
# context = ['', '']
# queries = ['', '']
# answers = ask_ChatGPT(context, queries)
# for answer in answers:
#     print(answers, '\n')

def add_row_to_csv(csv_path, new_row, columns):
    df_new_row = pd.DataFrame(data = new_row, columns = columns)
    with open(csv_path, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            df_new_row.to_csv(csv_path, index = False, header = True)
        else:
            df_new_row.to_csv(csv_path, mode = 'a', index = False, header = False, encoding='utf-8-sig', sep = ",")


# test code: add_rows_to_csv(path_potential, info_json, columns)
# add_rows_to_csv(path_potential, info_json, columns)