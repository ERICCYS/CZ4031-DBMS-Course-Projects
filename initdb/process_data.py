files = {
    "customer.csv" : "customer-processed.csv",
    "lineitem.csv" : "lineitem-processed.csv",
    "nation.csv" : "nation-processed.csv",
    "orders.csv" : "orders-processed.csv",
    "part.csv" : "part-processed.csv",
    "partsupp.csv" : "partsupp-processed.csv",
    "region.csv" : "region-processed.csv",
    "supplier.csv" : "supplier-processed.csv",
}

# remove the last "\\|" in every row
for key, value in files.items():
    with open(key, 'r') as r, open(value, 'w') as w:    
        for num, line in enumerate(r):  
            newline = line[:-2] + "\n" if "\n" in line else line[:-1]             
            w.write(newline)