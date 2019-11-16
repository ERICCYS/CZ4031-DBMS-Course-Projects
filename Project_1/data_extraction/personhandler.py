from xml.sax.handler import ContentHandler
from CsvWriter import CsvWriter


class Personhandler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        person_csv_path = './csv/person.csv'
        authorship_csv_path = './csv/authorship.csv'
        editorship_csv_path = './csv/editorship.csv'

        self.is_publication = False
        self.person_new_row = {}
        self.author_new_row = {}
        self.editor_new_row = {}
        self.person_csv_writer = CsvWriter(fieldnames=('personId', 'personFullName'), fileout=person_csv_path, field_delimiter=',')
        self.author_csv_writer = CsvWriter(fieldnames=('pubkey', 'personFullName'), fileout=authorship_csv_path, field_delimiter=',')
        self.editor_csv_writer = CsvWriter(fieldnames=('pubkey', 'personFullName'), fileout=editorship_csv_path, field_delimiter=',')
        self.is_title = False
        self.key = None
        self.person_count = 1
        self.pub_count = 1
        self.person_id = None
        self.content = ''
        self.author_name_list = []
        self.editor_name_list = []
        self.person_list = []
        self.person_field = {}
        self.is_homepage = False
        self.pub_type = ['article', 'inproceedings', 'proceedings', 'book',
                         'incollection', 'phdthesis', 'mastersthesis', 'www']

    def startElement(self, name, attrs):
        if name in self.pub_type:
            self.pub_count += 1
            if self.pub_count % 100000 == 0:
                print('Current count: {}'.format(self.pub_count))

            if name == 'www' and ('homepages' in attrs.getValue('key')):
                self.is_homepage = True
                self.person_list = []

            else:
                self.is_publication = True
                self.key = attrs.getValue('key')
                self.person_field['pubkey'] = self.key

    def endElement(self, name):
        if self.content != '':
            self.content = self.content.strip()

        if self.is_homepage:
            if name == 'author':
                # print(self.content)
                self.person_list.append(self.content)

            elif name == 'www' and len(self.person_list) != 0:
                self.person_new_row['personId'] = self.person_count
                self.person_new_row['personFullName'] = self.person_list
                self.person_count += 1
                self.person_csv_writer.add_row(self.person_new_row)
                # print(self.person_new_row)
                self.person_new_row = {}

                self.is_homepage = False

        elif self.is_publication:
            if name == 'author':
                # print('isauthor:' + self.content)
                # self.author_name_list.append(self.content)
                self.author_new_row['pubkey'] = self.key
                self.author_new_row['personFullName'] = self.content
                self.author_csv_writer.add_row(self.author_new_row)
                self.author_new_row = {}
                # self.author_name_list = []

            elif name == 'editor':
                # print('iseditor:' + self.content)
                # self.editor_name_list.append(self.content)
                self.editor_new_row['pubkey'] = self.key
                self.editor_new_row['personFullName'] = self.content
                self.editor_csv_writer.add_row(self.editor_new_row)
                self.editor_new_row = {}
                # self.editor_name_list = []

            elif name in self.pub_type:
                self.is_publication = False

        self.content = ''

    def characters(self, content):
        self.content += content

    def endDocument(self):
        self.person_csv_writer.write()
        del self.person_csv_writer
        self.author_csv_writer.write()
        del self.author_csv_writer
        self.editor_csv_writer.write()
        del self.editor_csv_writer
