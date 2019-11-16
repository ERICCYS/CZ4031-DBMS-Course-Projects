import csv
import os.path


class CsvWriter:
    # fieldnames_parent = []
    # fileout_parent =''

    # rows_parent = []

    def __init__(self, fieldnames, fieldnames_parent=(), fileout='csv_out.txt', fileout_parent='csv_parent_out.txt', field_delimiter='|'):
        self.fieldnames = fieldnames
        # self.fieldnames_parent = fieldnames_parent
        self.fileout = fileout
        self.rows = []
        self.field_delimiter = field_delimiter
        # self.fileout_parent = fileout_parent

    def add_row(self, row, parent=0):
        # if parent:
        #     self.rows_parent.append(row)
        # else:
        self.rows.append(row)

    def write(self, append=False):
        fileout_is_created = os.path.isfile(self.fileout)
        fopenmode = 'a' if append else 'w'
        with open(self.fileout, fopenmode, encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=self.field_delimiter)

            if not fileout_is_created:
                writer.writeheader()

            for row in self.rows:
                for key, value in row.items():
                    if isinstance(value, list):
                        row[key] = ' | '.join(value)
                writer.writerow(row)
