# CZ4031-Project-1

1. Convert XML to CSV files

    _python extract_data.py_
    
    * directory _csv_ should exist
    * writeheader() will only be run when file is not created
      Hence, for example, if _publication.csv_ is created and you run _python extract_data.py_ again.
      The previous _publication.csv_ will be overwritten, and header will disappear. 
    

2. Half data in publication.csv

    _python half_all_csv.py_
    
    * directory _csv_half_ should exist
    

3. cut 3/4 of data in publication.csv
    
    _python quarter_all_csv.py_
    
    * directory _csv_quarter_ should exist
    

useful link for sax parser:
http://python.zirael.org/e-sax1.html
