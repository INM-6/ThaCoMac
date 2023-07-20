# self-written public library


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
            
'''
# test code: ask_ChatGPT(context, queries)
context = ['', '']
queries = ['', '']
answers = ask_ChatGPT(context, queries)
for answer in answers:
    print(answers, '\n')
'''