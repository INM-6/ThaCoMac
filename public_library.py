# self-written public library
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