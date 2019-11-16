import random
import os
import glob
import json
import pandas as pd
from sklearn.model_selection import train_test_split

import warnings

warnings.filterwarnings('ignore')
publication_csv_path = './csv/publication.csv'
pub_subclass_csv_path = {
    'article': './csv/article.csv',
    'inproceedings': './csv/inproceeding.csv',
    'incollection': './csv/incollection.csv',
    'proceedings': './csv/proceeding.csv',
    'book': './csv/book.csv',
    'phdthesis': './csv/phdthesis.csv',
    'masterthesis': './csv/masterthesis.csv',
    'www': './csv/www.csv'
}
person_csv_path = './csv/person.csv'
authorship_csv_path = './csv/authorship.csv'
editorship_csv_path = './csv/editorship.csv'


# read from folders
def read_folder(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("sv"):
                all_files.append(os.path.join(root, file))
    return all_files


publication_df = pd.read_csv(publication_csv_path, sep='|')

publication_df_keep, publication_df_drop = train_test_split(publication_df, test_size=0.63, random_state=0,
                                                            stratify=publication_df['pubType'])
print(publication_df['pubType'].value_counts().sum() / 4)
print(publication_df_keep['pubType'].value_counts().sum())
print(publication_df_keep['pubType'].value_counts())


for df_path, crossref in {pub_subclass_csv_path['article']: 'crossref',
                          pub_subclass_csv_path['inproceedings']: 'crossref',
                          pub_subclass_csv_path['incollection']: 'crossref'
                          }.items():
    pub_df = pd.read_csv(df_path, sep='|')
    pub_df = pub_df.merge(publication_df_keep[['pubkey']], on='pubkey')
    pub_df = pub_df[(pub_df[crossref].isin(list(publication_df_keep['pubkey'])))|(pub_df[crossref].isnull())]
    pub_df.to_csv(df_path.replace('/csv/', '/csv_quarter/'), index=False, line_terminator='\r\n', sep='|')
    print(df_path.replace('/csv/', '/csv_quarter/'))
    print(pub_df.shape)

for df_path in [pub_subclass_csv_path['proceedings'], pub_subclass_csv_path['book'],
                pub_subclass_csv_path['phdthesis'], pub_subclass_csv_path['www'],
                pub_subclass_csv_path['masterthesis']]:
    pub_df = pd.read_csv(df_path, sep='|')
    pub_df = pub_df.merge(publication_df_keep[['pubkey']], on='pubkey')
    pub_df.to_csv(df_path.replace('/csv/', '/csv_quarter/'), index=False, line_terminator='\r\n', sep='|')
    print(df_path.replace('/csv/', '/csv_quarter/'))
    print(pub_df.shape)

pubKey_keep = []
for pub_path in pub_subclass_csv_path.values():
    pub_df = pd.read_csv(pub_path.replace('/csv/', '/csv_quarter/'), sep='|')
    pubKey_keep.append(pub_df[['pubkey']])

pubKey_keep = pd.concat(pubKey_keep)
print(pubKey_keep.shape)
print(publication_df_keep.shape)
publication_df_keep = publication_df_keep.merge(pubKey_keep)
publication_df_keep.to_csv(publication_csv_path.replace('/csv/', '/csv_quarter/'), index=False, line_terminator='\r\n', sep='|')

authorship_df = pd.read_csv(authorship_csv_path)
editorship_df = pd.read_csv(editorship_csv_path)
authorship_df = authorship_df[authorship_df['pubkey'].isin(publication_df_keep['pubkey'])]
authorship_df.to_csv(authorship_csv_path.replace('/csv/', '/csv_quarter/'), index=False, line_terminator='\r\n')
editorship_df = editorship_df[editorship_df['pubkey'].isin(publication_df_keep['pubkey'])]
editorship_df.to_csv(editorship_csv_path.replace('/csv/', '/csv_quarter/'), index=False, line_terminator='\r\n')

personship_df = pd.concat([authorship_df, editorship_df])
# print(personship_df.shape)
# print(personship_df.head())
print(personship_df['pubkey'].value_counts().head())
print(personship_df[['personFullName']].drop_duplicates().shape)

person_df = pd.read_csv(person_csv_path)
person_df.head()
print(person_df.shape)
person_df_keep = person_df.merge(personship_df[['personFullName']].drop_duplicates(), on='personFullName')
print(person_df_keep.shape)

person_df_keep.to_csv(person_csv_path.replace('/csv/', '/csv_quarter/'), index=False, line_terminator='\r\n')