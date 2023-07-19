# import required packages
import pandas as pd

# write the information of a literature as a row to .csv file 'summary_table_of_related_studies.csv'
def add_rows_to_df(df_liter, i, doi, pub_link, authors, title):
    new_row = {'order': i,
               'DOI':doi,
               'Publication_link':pub_link,
               'Autours':authors,
               'Title':title}
    df_liter = pd.concat([df_liter, pd.DataFrame([new_row])], ignore_index=False)
    # df_liter = df_liter.append(new_row, ignore_index=False)
    # df_lite = pd.DataFrame(lite, columns = headers, index = None)
    # print(df_liter)
    return df_liter

# file path
path = '/Users/didihou/myProjects/didihou_master_project/summary_table_of_related_studies.csv'
# clear the .csv file
with open(path, 'w') as f:
    f.truncate()
    f.close()

# i is the index of the rows in .csv file and also the index of the literature
columns = {'order':[],
           'DOI':[],
           'Publication_link':[],
           'Autours':[],
           'Title':[]}
df_liter = pd.DataFrame(columns)

for i in range(10):
    doi = '10.1016/j.neuroscience.2007.02.033'
    pub_link = 'https://pubmed.ncbi.nlm.nih.gov/17395383/'
    authors = 'Cappe et al.'
    title = 'Thalamocortical and the dual pattern of corticothalamic projections of the posterior parietal cortex in macaque monkeys'
    df_liter = add_rows_to_df(df_liter, i, doi, pub_link, authors, title)

df_liter.to_csv(path, mode='a', sep=',', index=False)


# read a cell value from a .csv file
df = pd.read_csv(path)
# print(df.columns.tolist())
col = 'DOI'
index = 1
print(df[col].iloc[index])
# when trying to read a cell from the .csv file, specify the cell using [column name][index]