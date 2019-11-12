from pyconnect import DBConnection

connection = DBConnection()
query = input() 
result = connection.execute(query)
print(result)
connection.close()
