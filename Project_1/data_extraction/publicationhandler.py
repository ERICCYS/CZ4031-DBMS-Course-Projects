from xml.sax.handler import ContentHandler
from CsvWriter import CsvWriter


class PublicationHandler(ContentHandler):
    def __init__(self, fieldnames):
        ContentHandler.__init__(self)

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

        self.pub_subclass_attributes = {
            'article': ['pubkey', 'journal', 'volume', 'number', 'pages', 'url', 'booktitle', 'crossref'],
            'inproceedings': ['pubkey', 'booktitle', 'pages', 'url', 'crossref'],
            'proceedings': ['pubkey', 'booktitle', 'volume', 'series', 'pages', 'url', 'crossref'],
            'book': ['pubkey', 'booktitle', 'volume', 'series', 'pages', 'publisher'],
            'incollection' : ['pubkey', 'booktitle', 'number', 'pages', 'url', 'crossref'],
            'www': ['pubkey', 'booktitle', 'url'],
            'mastersthesis':  ['pubkey', 'school'],
            'phdthesis': ['pubkey', 'volume', 'series', 'pages', 'school']
            }
 
        self.is_publication = False
        self.key = None
        self.date = None
        self.publication_csv_writer = CsvWriter(
            fieldnames=('pub_id', 'mdate', 'pubkey', 'title', 'year', 'ee', 'pubType', 'type'),
            fileout=publication_csv_path)
        self.pub_subclass_csv_writers = {
            'article': CsvWriter(fieldnames=self.pub_subclass_attributes['article'], fileout=pub_subclass_csv_path['article']),
            'inproceedings': CsvWriter(fieldnames=self.pub_subclass_attributes['inproceedings'], fileout=pub_subclass_csv_path['inproceedings']),
            'proceedings': CsvWriter(fieldnames=self.pub_subclass_attributes['proceedings'], fileout=pub_subclass_csv_path['proceedings']),
            'book': CsvWriter(fieldnames=self.pub_subclass_attributes['book'], fileout=pub_subclass_csv_path['book']),
            'incollection': CsvWriter(fieldnames=self.pub_subclass_attributes['incollection'], fileout=pub_subclass_csv_path['incollection']),
            'www': CsvWriter(fieldnames=self.pub_subclass_attributes['www'], fileout=pub_subclass_csv_path['www']),
            'mastersthesis': CsvWriter(fieldnames=self.pub_subclass_attributes['mastersthesis'], fileout=pub_subclass_csv_path['masterthesis']),
            'phdthesis': CsvWriter(fieldnames=self.pub_subclass_attributes['phdthesis'], fileout=pub_subclass_csv_path['phdthesis'])
        }

        self.fieldnames = fieldnames
        self.pub_count = 0
        self.content = ''
        self.pub_type = ['article', 'inproceedings', 'proceedings', 'book',
                         'incollection', 'phdthesis', 'mastersthesis', 'www']
        self.current_pub_type = None
        self.pub_new_row = {}
        self.subclass_new_row = {}

    def startElement(self, name, attrs):
        if name in self.pub_type:
            self.pub_count += 1
            if self.pub_count % 100000 == 0:
                print('Current count: {}'.format(self.pub_count))

            if 'homepages' not in attrs.getValue('key'):
                self.is_publication = True
                self.key = attrs.getValue('key')
                self.date = attrs.getValue('mdate')
                self.current_pub_type = name
                self.subclass_new_row = {attr: None for attr in self.pub_subclass_attributes[self.current_pub_type]}

    def endElement(self, name):
        if self.content != '':
            self.content = self.content.strip().replace('|', '-')

        if self.is_publication:
            self.pub_new_row['pub_id'] = self.pub_count
            self.pub_new_row['mdate'] = self.date
            self.pub_new_row['pubkey'] = self.key
            self.pub_new_row['pubType'] = self.current_pub_type
            self.pub_new_row['type'] = self.key.split('/')[0]
            # self.pub_new_row['conf_name'] = self.key.split('/')[1] if self.pub_new_row['type'] == 'conf' else None
            # if self.pub_new_row['conf_name'] is not None:
            #     print(self.pub_new_row['conf_name'])
            self.subclass_new_row['pubkey'] = self.key

            if name == 'title':
                self.pub_new_row['title'] = self.content
                # if self.pub_new_row['type'] == 'conf':
                #     for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                #         if month in self.content:
                #             self.pub_new_row['month'] = month
                #             print('current pub type:', self.content)
                #             print("month:", self.pub_new_row['month'])

            elif name == 'year':
                self.pub_new_row['year'] = self.content

            elif name == 'ee':
                self.pub_new_row['ee'] = self.content

            elif name in self.pub_subclass_attributes[self.current_pub_type]:
                # this if-condition might be removed, you can print the attribute to see
                if self.subclass_new_row[name] is not None:
                    self.subclass_new_row[name] = self.subclass_new_row[name] + ';' + self.content
                    # print(self.subclass_new_row[name])
                else:
                    self.subclass_new_row[name] = self.content

            elif name in self.pub_type:
                self.is_publication = False
                # print(self.pub_new_row)
                self.publication_csv_writer.add_row(self.pub_new_row)
                self.pub_subclass_csv_writers[name].add_row(self.subclass_new_row)
                self.pub_new_row = {}
                self.subclass_new_row = {}

        self.content = ''

    def characters(self, content):
        self.content += content

    def endDocument(self):
        self.publication_csv_writer.write()
        del self.publication_csv_writer
        for subclass in self.pub_type:
            self.pub_subclass_csv_writers[subclass].write()
            del self.pub_subclass_csv_writers[subclass]
